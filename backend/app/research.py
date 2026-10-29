"""Evidence-preserving extraction. No model-generated facts or fabricated summaries."""
import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse
import httpx
import trafilatura
from bs4 import BeautifulSoup

MAX_BYTES = 2_000_000


def canonical_url(url):
    if not url:
        return None
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Use a public HTTP(S) URL without credentials.")
    if parsed.port and parsed.port not in (80, 443):
        raise ValueError("Only standard web ports are supported.")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip("/") or "/", "", parsed.query, ""))


def validate_public_url(url):
    canonical_url(url)
    host = urlparse(url).hostname
    try:
        addresses = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    except OSError as exc:
        raise ValueError("The source hostname could not be resolved.") from exc
    if not addresses or any(not ipaddress.ip_address(item[4][0]).is_global for item in addresses):
        raise ValueError("Local, private and reserved network addresses are blocked.")


def fetch_article(url):
    """Reject redirects, private hosts, oversized responses and non-HTML bodies."""
    validate_public_url(url)
    try:
        with httpx.Client(timeout=12, follow_redirects=False, trust_env=False) as client:
            with client.stream("GET", url, headers={"User-Agent": "EditorialWorkspace/1.0"}) as response:
                if 300 <= response.status_code < 400:
                    raise ValueError("Redirects are disabled. Paste the final article URL or its text.")
                response.raise_for_status()
                if not any(x in response.headers.get("content-type", "") for x in ("text/html", "text/plain")):
                    raise ValueError("Only HTML or plain-text sources can be imported.")
                data = bytearray()
                for chunk in response.iter_bytes():
                    data.extend(chunk)
                    if len(data) > MAX_BYTES:
                        raise ValueError("Source exceeds the 2 MB import limit.")
    except httpx.HTTPError as exc:
        raise ValueError("Source could not be imported. Paste the article text instead.") from exc
    html = data.decode("utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    content = trafilatura.extract(html) or soup.get_text(" ", strip=True)
    title = soup.title.get_text(strip=True) if soup.title else urlparse(url).hostname
    if len(content.strip()) < 40:
        raise ValueError("Not enough readable content. Paste the source text instead.")
    return {"title": title[:240], "content": content[:50000]}


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]


def editorial_prompts(content):
    lower = content.lower()
    if any(word in lower for word in ("privacy", "local", "on-device", "laptop")):
        return ("Analysis: local execution may change data handling and deployment choices; these sources do not by themselves establish privacy or production suitability.", "Builders and security teams considering local inference; verify the data flow and hardware requirements.", "Test one local workflow against a baseline and document its limits before recommending adoption.")
    if any(word in lower for word in ("price", "cost", "pricing", "budget")):
        return ("Analysis: reported pricing may change a team's operating budget; compare full workload cost rather than one headline number.", "Engineering and procurement teams making a cost-sensitive choice.", "Compare like-for-like cost, quality and latency using the same workload.")
    if any(word in lower for word in ("license", "open-weight", "open source")):
        return ("Analysis: availability and licensing can affect deployment options; inspect the actual terms and operational requirements.", "Developers and teams evaluating distribution, customization or commercial use.", "Explain what the release permits, what it requires, and which claims still need evaluation.")
    return ("Analysis: assess whether this changes capability, access or risk. The excerpts alone do not establish impact.", "Readers working in the area described by this source; narrow the audience after reviewing the full text.", "Identify one practical reader decision and the evidence still missing.")


def build_brief(sources):
    if len(sources) < 3:
        raise ValueError("Add at least three distinct sources before building a brief.")
    items = []
    for source in sources:
        candidates = sentences(source.content)
        ranked = sorted(enumerate(candidates), key=lambda pair: (len(pair[1].split()) >= 8, bool(re.search(r"\b(released|reports?|tested|requires?|supports?|announced)\b", pair[1], re.I)), min(len(pair[1].split()), 35)), reverse=True)[:3]
        excerpts = [value for _, value in sorted(ranked)]
        why, who, angle = editorial_prompts(source.content)
        evidence = [{"source_id": source.id, "source_title": source.title, "url": source.url,
                     "excerpt": excerpt, "type": "speculation" if re.search(r"\b(may|might|could|expects?|plans?|predicts?|potentially)\b", excerpt, re.I) else "source_claim", "verified": False} for excerpt in excerpts]
        items.append({"source_id": source.id, "title": source.title, "what_happened": evidence,
                      "reliability": source.reliability,
                      "reliability_note": "Editor-supplied classification; independently verify claims and dates.",
                      "why_it_matters": {"type": "analysis", "text": why},
                      "who_should_care": {"type": "analysis", "text": who},
                      "angle": {"type": "analysis", "text": angle}})
    return {"method": "extractive", "items": items,
            "angle": "Compare stated capabilities with available evidence, then explain one practical decision for readers.",
            "limitations": "Selected excerpts may omit key details. Source claims are not verified facts. Implications are editorial prompts, not model conclusions."}

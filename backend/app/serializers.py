from .writing import metrics


def draft_json(draft):
    if draft is None:
        return None
    return {"id": draft.id, "original": draft.original, "current": draft.current, "version": draft.version,
            "suggestions": draft.suggestions, "revisions": draft.revisions,
            "original_metrics": metrics(draft.original), "metrics": metrics(draft.current)}


def project_json(project):
    return {"id": project.id, "title": project.title, "created_at": project.created_at.isoformat(),
            "sources": [{"id": s.id, "title": s.title, "url": s.url, "content": s.content, "kind": s.kind, "reliability": s.reliability} for s in project.sources],
            "brief": project.brief, "draft": draft_json(project.draft)}



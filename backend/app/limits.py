from datetime import datetime, timezone
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from .database import RequestQuota
from .gemini import AIError


def day_key():
    return "ai:" + datetime.now(timezone.utc).strftime("%Y-%m-%d")


def reserve_request(db, key, limit):
    insert = sqlite_insert if db.bind.dialect.name == "sqlite" else postgres_insert
    statement = insert(RequestQuota).values(key=key, requests=1)
    statement = statement.on_conflict_do_update(index_elements=[RequestQuota.key],
        set_={"requests": RequestQuota.requests + 1}, where=RequestQuota.requests < limit)
    result = db.execute(statement)
    if result.rowcount == 0:
        db.rollback()
        raise AIError("request_limit", "The workspace request limit was reached. Try again after the limit resets.", 429)


def used_requests(db):
    row = db.get(RequestQuota, day_key())
    return row.requests if row else 0

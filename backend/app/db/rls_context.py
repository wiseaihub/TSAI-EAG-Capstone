"""Supabase Postgres session variables for Row Level Security.

Policies use auth.uid(), which reads JWT claims from the DB session. SQLAlchemy
connections do not send Supabase JWT automatically — set request.jwt.claim.*
before inserts/selects on RLS-protected tables so auth.uid() matches the user.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session


def apply_supabase_jwt_claims(db: Session, jwt_sub: str) -> None:
    """Align session with Supabase RLS (auth.uid()::text = user_id policies).

    Use session-scoped settings (is_local=false). Transaction-scoped (true) is cleared on
    every commit(), so after case_tracking helpers commit, later inserts (finalize, run_cbc,
    agent_runs on the request connection) would run with no JWT and RLS would block them.
    Each HTTP request should call this once at the start; pooled connections are overwritten
    per request with the current user's sub.
    """
    if not jwt_sub:
        return
    dialect = getattr(getattr(db, "bind", None), "dialect", None)
    if not dialect or getattr(dialect, "name", "") != "postgresql":
        return
    sub = str(jwt_sub).strip()
    if not sub:
        return
    db.execute(text("SELECT set_config('request.jwt.claim.sub', :sub, false)"), {"sub": sub})
    db.execute(text("SELECT set_config('request.jwt.claim.role', 'authenticated', false)"))

"""Add RLS policies for runtime tables.

Revision ID: 003_runtime_rls
Revises: 002_minimal_runtime_schema
Create Date: 2026-03-30
"""

from typing import Sequence, Union

from alembic import op

revision: str = "003_runtime_rls"
down_revision: Union[str, None] = "002_minimal_runtime_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # cases
    op.execute("ALTER TABLE cases ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY cases_owner_select ON cases
        FOR SELECT
        USING (auth.uid()::text = user_id)
        """
    )
    op.execute(
        """
        CREATE POLICY cases_owner_insert ON cases
        FOR INSERT
        WITH CHECK (auth.uid()::text = user_id)
        """
    )
    op.execute(
        """
        CREATE POLICY cases_owner_update ON cases
        FOR UPDATE
        USING (auth.uid()::text = user_id)
        WITH CHECK (auth.uid()::text = user_id)
        """
    )

    # agent_runs
    op.execute("ALTER TABLE agent_runs ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY agent_runs_owner_select ON agent_runs
        FOR SELECT
        USING (
          EXISTS (
            SELECT 1 FROM cases c
            WHERE c.id = agent_runs.case_id
              AND c.user_id = auth.uid()::text
          )
        )
        """
    )
    op.execute(
        """
        CREATE POLICY agent_runs_owner_insert ON agent_runs
        FOR INSERT
        WITH CHECK (
          EXISTS (
            SELECT 1 FROM cases c
            WHERE c.id = agent_runs.case_id
              AND c.user_id = auth.uid()::text
          )
        )
        """
    )
    op.execute(
        """
        CREATE POLICY agent_runs_owner_update ON agent_runs
        FOR UPDATE
        USING (
          EXISTS (
            SELECT 1 FROM cases c
            WHERE c.id = agent_runs.case_id
              AND c.user_id = auth.uid()::text
          )
        )
        WITH CHECK (
          EXISTS (
            SELECT 1 FROM cases c
            WHERE c.id = agent_runs.case_id
              AND c.user_id = auth.uid()::text
          )
        )
        """
    )

    # agent_messages
    op.execute("ALTER TABLE agent_messages ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY agent_messages_owner_select ON agent_messages
        FOR SELECT
        USING (
          EXISTS (
            SELECT 1 FROM cases c
            WHERE c.id = agent_messages.case_id
              AND c.user_id = auth.uid()::text
          )
        )
        """
    )
    op.execute(
        """
        CREATE POLICY agent_messages_owner_insert ON agent_messages
        FOR INSERT
        WITH CHECK (
          EXISTS (
            SELECT 1 FROM cases c
            WHERE c.id = agent_messages.case_id
              AND c.user_id = auth.uid()::text
          )
        )
        """
    )

    # run_artifacts
    op.execute("ALTER TABLE run_artifacts ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY run_artifacts_owner_select ON run_artifacts
        FOR SELECT
        USING (
          EXISTS (
            SELECT 1
            FROM agent_runs ar
            JOIN cases c ON c.id = ar.case_id
            WHERE ar.id = run_artifacts.run_id
              AND c.user_id = auth.uid()::text
          )
        )
        """
    )
    op.execute(
        """
        CREATE POLICY run_artifacts_owner_insert ON run_artifacts
        FOR INSERT
        WITH CHECK (
          EXISTS (
            SELECT 1
            FROM agent_runs ar
            JOIN cases c ON c.id = ar.case_id
            WHERE ar.id = run_artifacts.run_id
              AND c.user_id = auth.uid()::text
          )
        )
        """
    )

    # audit_events
    op.execute("ALTER TABLE audit_events ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY audit_events_owner_select ON audit_events
        FOR SELECT
        USING (user_id IS NULL OR user_id = auth.uid()::text)
        """
    )
    op.execute(
        """
        CREATE POLICY audit_events_owner_insert ON audit_events
        FOR INSERT
        WITH CHECK (user_id IS NULL OR user_id = auth.uid()::text)
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS audit_events_owner_insert ON audit_events")
    op.execute("DROP POLICY IF EXISTS audit_events_owner_select ON audit_events")
    op.execute("ALTER TABLE audit_events DISABLE ROW LEVEL SECURITY")

    op.execute("DROP POLICY IF EXISTS run_artifacts_owner_insert ON run_artifacts")
    op.execute("DROP POLICY IF EXISTS run_artifacts_owner_select ON run_artifacts")
    op.execute("ALTER TABLE run_artifacts DISABLE ROW LEVEL SECURITY")

    op.execute("DROP POLICY IF EXISTS agent_messages_owner_insert ON agent_messages")
    op.execute("DROP POLICY IF EXISTS agent_messages_owner_select ON agent_messages")
    op.execute("ALTER TABLE agent_messages DISABLE ROW LEVEL SECURITY")

    op.execute("DROP POLICY IF EXISTS agent_runs_owner_update ON agent_runs")
    op.execute("DROP POLICY IF EXISTS agent_runs_owner_insert ON agent_runs")
    op.execute("DROP POLICY IF EXISTS agent_runs_owner_select ON agent_runs")
    op.execute("ALTER TABLE agent_runs DISABLE ROW LEVEL SECURITY")

    op.execute("DROP POLICY IF EXISTS cases_owner_update ON cases")
    op.execute("DROP POLICY IF EXISTS cases_owner_insert ON cases")
    op.execute("DROP POLICY IF EXISTS cases_owner_select ON cases")
    op.execute("ALTER TABLE cases DISABLE ROW LEVEL SECURITY")

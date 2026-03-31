"""Add minimal runtime schema for wise-ai + S18.

Revision ID: 002_minimal_runtime_schema
Revises: fd1914927d78
Create Date: 2026-03-30
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002_minimal_runtime_schema"
down_revision: Union[str, None] = "fd1914927d78"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cases",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("input_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_cases_user_id_created_at", "cases", ["user_id", "created_at"], unique=False)
    op.create_index("ix_cases_status_created_at", "cases", ["status", "created_at"], unique=False)

    op.create_table(
        "agent_runs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("case_id", sa.String(), nullable=False),
        sa.Column("session_id", sa.String(), nullable=True),
        sa.Column("s18_run_id", sa.String(), nullable=True),
        sa.Column("agent_name", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("error_text", sa.Text(), nullable=True),
        sa.Column("metrics", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["case_id"], ["cases.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_agent_runs_case_id_created_at", "agent_runs", ["case_id", "created_at"], unique=False)
    op.create_index("ix_agent_runs_session_id", "agent_runs", ["session_id"], unique=False)
    op.create_index("uq_agent_runs_s18_run_id", "agent_runs", ["s18_run_id"], unique=True)
    op.create_index(
        "ix_agent_runs_active_status",
        "agent_runs",
        ["status", "created_at"],
        unique=False,
        postgresql_where=sa.text("status IN ('queued', 'running')"),
    )

    op.create_table(
        "agent_messages",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("case_id", sa.String(), nullable=False),
        sa.Column("run_id", sa.String(), nullable=True),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("meta", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["case_id"], ["cases.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["run_id"], ["agent_runs.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_agent_messages_case_id_created_at", "agent_messages", ["case_id", "created_at"], unique=False)
    op.create_index("ix_agent_messages_run_id_created_at", "agent_messages", ["run_id", "created_at"], unique=False)

    op.create_table(
        "run_artifacts",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("run_id", sa.String(), nullable=False),
        sa.Column("artifact_type", sa.String(), nullable=False),
        sa.Column("storage_path", sa.String(), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["run_id"], ["agent_runs.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_run_artifacts_run_id_created_at", "run_artifacts", ["run_id", "created_at"], unique=False)
    op.create_index("ix_run_artifacts_type_created_at", "run_artifacts", ["artifact_type", "created_at"], unique=False)

    op.create_table(
        "audit_events",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("entity_type", sa.String(), nullable=False),
        sa.Column("entity_id", sa.String(), nullable=False),
        sa.Column("event_type", sa.String(), nullable=False),
        sa.Column("event_payload", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_audit_events_entity_created_at", "audit_events", ["entity_type", "entity_id", "created_at"], unique=False)
    op.create_index("ix_audit_events_created_at", "audit_events", ["created_at"], unique=False)



def downgrade() -> None:
    op.drop_index("ix_audit_events_created_at", table_name="audit_events")
    op.drop_index("ix_audit_events_entity_created_at", table_name="audit_events")
    op.drop_table("audit_events")

    op.drop_index("ix_run_artifacts_type_created_at", table_name="run_artifacts")
    op.drop_index("ix_run_artifacts_run_id_created_at", table_name="run_artifacts")
    op.drop_table("run_artifacts")

    op.drop_index("ix_agent_messages_run_id_created_at", table_name="agent_messages")
    op.drop_index("ix_agent_messages_case_id_created_at", table_name="agent_messages")
    op.drop_table("agent_messages")

    op.drop_index("ix_agent_runs_active_status", table_name="agent_runs")
    op.drop_index("uq_agent_runs_s18_run_id", table_name="agent_runs")
    op.drop_index("ix_agent_runs_session_id", table_name="agent_runs")
    op.drop_index("ix_agent_runs_case_id_created_at", table_name="agent_runs")
    op.drop_table("agent_runs")

    op.drop_index("ix_cases_status_created_at", table_name="cases")
    op.drop_index("ix_cases_user_id_created_at", table_name="cases")
    op.drop_table("cases")

"""Add knowledge bank tables.

Revision ID: 004_add_kb_schema
Revises: 003_runtime_rls
Create Date: 2026-04-01
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "004_add_kb_schema"
down_revision: Union[str, None] = "003_runtime_rls"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "kb_entries",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("owner_user_id", sa.String(), nullable=True),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("layer", sa.String(), nullable=False),
        sa.Column("patient_id", sa.String(), nullable=True),
        sa.Column("doctor_id", sa.String(), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("source_type", sa.String(), nullable=True),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("source_domain", sa.String(), nullable=True),
        sa.Column("source_ref", sa.JSON(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("is_shared", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("base_confidence", sa.Float(), nullable=False, server_default=sa.text("0.5")),
        sa.Column("feedback_score", sa.Float(), nullable=False, server_default=sa.text("0")),
        sa.Column("confidence", sa.Float(), nullable=False, server_default=sa.text("0.5")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint(
            "role IN ('patient','doctor','system')",
            name="ck_kb_entries_role",
        ),
        sa.CheckConstraint(
            "layer IN ('web_research','product_kb','doctor_context','patient_context')",
            name="ck_kb_entries_layer",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_kb_entries_owner_user_id_created_at", "kb_entries", ["owner_user_id", "created_at"], unique=False)
    op.create_index("ix_kb_entries_layer_created_at", "kb_entries", ["layer", "created_at"], unique=False)
    op.create_index("ix_kb_entries_patient_id_created_at", "kb_entries", ["patient_id", "created_at"], unique=False)
    op.create_index("ix_kb_entries_doctor_id_created_at", "kb_entries", ["doctor_id", "created_at"], unique=False)

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_kb_entries_fts ON kb_entries USING GIN (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,'')))"
    )

    op.create_table(
        "kb_feedback",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("entry_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("confidence_before", sa.Float(), nullable=True),
        sa.Column("confidence_after", sa.Float(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("correction", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint(
            "role IN ('patient','doctor','system')",
            name="ck_kb_feedback_role",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["entry_id"], ["kb_entries.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_kb_feedback_entry_id_created_at", "kb_feedback", ["entry_id", "created_at"], unique=False)
    op.create_index("ix_kb_feedback_user_id_created_at", "kb_feedback", ["user_id", "created_at"], unique=False)

    op.create_table(
        "kb_query_logs",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("query_text", sa.Text(), nullable=False),
        sa.Column("layer_order", sa.JSON(), nullable=True),
        sa.Column("filters", sa.JSON(), nullable=True),
        sa.Column("result_entry_ids", sa.JSON(), nullable=True),
        sa.Column("response_confidence", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint(
            "role IN ('patient','doctor','system')",
            name="ck_kb_query_logs_role",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_kb_query_logs_user_id_created_at", "kb_query_logs", ["user_id", "created_at"], unique=False)

    op.execute("ALTER TABLE kb_entries ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY kb_entries_owner_select ON kb_entries
        FOR SELECT
        USING (
          owner_user_id = auth.uid()::text
          OR (is_shared = true AND layer = 'product_kb')
          OR (layer = 'patient_context' AND patient_id = auth.uid()::text)
          OR (layer = 'doctor_context' AND doctor_id = auth.uid()::text)
        )
        """
    )
    op.execute(
        """
        CREATE POLICY kb_entries_owner_insert ON kb_entries
        FOR INSERT
        WITH CHECK (
          owner_user_id = auth.uid()::text
          AND (
            layer = 'product_kb'
            OR layer = 'web_research'
            OR (layer = 'patient_context' AND patient_id = auth.uid()::text)
            OR (layer = 'doctor_context' AND doctor_id = auth.uid()::text)
          )
        )
        """
    )
    op.execute(
        """
        CREATE POLICY kb_entries_owner_update ON kb_entries
        FOR UPDATE
        USING (owner_user_id = auth.uid()::text)
        WITH CHECK (owner_user_id = auth.uid()::text)
        """
    )
    op.execute(
        """
        CREATE POLICY kb_entries_owner_delete ON kb_entries
        FOR DELETE
        USING (owner_user_id = auth.uid()::text)
        """
    )

    op.execute("ALTER TABLE kb_feedback ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY kb_feedback_owner_select ON kb_feedback
        FOR SELECT
        USING (user_id = auth.uid()::text)
        """
    )
    op.execute(
        """
        CREATE POLICY kb_feedback_owner_insert ON kb_feedback
        FOR INSERT
        WITH CHECK (user_id = auth.uid()::text)
        """
    )

    op.execute("ALTER TABLE kb_query_logs ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY kb_query_logs_owner_select ON kb_query_logs
        FOR SELECT
        USING (user_id = auth.uid()::text)
        """
    )
    op.execute(
        """
        CREATE POLICY kb_query_logs_owner_insert ON kb_query_logs
        FOR INSERT
        WITH CHECK (user_id = auth.uid()::text)
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS kb_query_logs_owner_insert ON kb_query_logs")
    op.execute("DROP POLICY IF EXISTS kb_query_logs_owner_select ON kb_query_logs")
    op.execute("ALTER TABLE kb_query_logs DISABLE ROW LEVEL SECURITY")

    op.execute("DROP POLICY IF EXISTS kb_feedback_owner_insert ON kb_feedback")
    op.execute("DROP POLICY IF EXISTS kb_feedback_owner_select ON kb_feedback")
    op.execute("ALTER TABLE kb_feedback DISABLE ROW LEVEL SECURITY")

    op.execute("DROP POLICY IF EXISTS kb_entries_owner_delete ON kb_entries")
    op.execute("DROP POLICY IF EXISTS kb_entries_owner_update ON kb_entries")
    op.execute("DROP POLICY IF EXISTS kb_entries_owner_insert ON kb_entries")
    op.execute("DROP POLICY IF EXISTS kb_entries_owner_select ON kb_entries")
    op.execute("ALTER TABLE kb_entries DISABLE ROW LEVEL SECURITY")

    op.drop_index("ix_kb_query_logs_user_id_created_at", table_name="kb_query_logs")
    op.drop_table("kb_query_logs")

    op.drop_index("ix_kb_feedback_user_id_created_at", table_name="kb_feedback")
    op.drop_index("ix_kb_feedback_entry_id_created_at", table_name="kb_feedback")
    op.drop_table("kb_feedback")

    op.execute("DROP INDEX IF EXISTS ix_kb_entries_fts")
    op.drop_index("ix_kb_entries_doctor_id_created_at", table_name="kb_entries")
    op.drop_index("ix_kb_entries_patient_id_created_at", table_name="kb_entries")
    op.drop_index("ix_kb_entries_layer_created_at", table_name="kb_entries")
    op.drop_index("ix_kb_entries_owner_user_id_created_at", table_name="kb_entries")
    op.drop_table("kb_entries")

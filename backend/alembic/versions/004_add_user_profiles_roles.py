"""Add user_profiles table for application RBAC roles.

Revision ID: 004_user_profiles_roles
Revises: 003_runtime_rls
Create Date: 2026-04-01
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "004_user_profiles_roles"
down_revision: Union[str, None] = "003_runtime_rls"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_profiles",
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_index("ix_user_profiles_role", "user_profiles", ["role"], unique=False)
    op.create_index("ix_user_profiles_created_at", "user_profiles", ["created_at"], unique=False)

    op.execute("ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY user_profiles_owner_select ON user_profiles
        FOR SELECT
        USING (auth.uid()::text = user_id)
        """
    )
    op.execute(
        """
        CREATE POLICY user_profiles_owner_insert ON user_profiles
        FOR INSERT
        WITH CHECK (auth.uid()::text = user_id)
        """
    )
    op.execute(
        """
        CREATE POLICY user_profiles_owner_update ON user_profiles
        FOR UPDATE
        USING (auth.uid()::text = user_id)
        WITH CHECK (auth.uid()::text = user_id)
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS user_profiles_owner_update ON user_profiles")
    op.execute("DROP POLICY IF EXISTS user_profiles_owner_insert ON user_profiles")
    op.execute("DROP POLICY IF EXISTS user_profiles_owner_select ON user_profiles")
    op.execute("ALTER TABLE user_profiles DISABLE ROW LEVEL SECURITY")

    op.drop_index("ix_user_profiles_created_at", table_name="user_profiles")
    op.drop_index("ix_user_profiles_role", table_name="user_profiles")
    op.drop_table("user_profiles")

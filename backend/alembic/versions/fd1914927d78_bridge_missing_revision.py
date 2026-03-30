"""Bridge missing historical revision present in deployed DB.

Revision ID: fd1914927d78
Revises: 001_patient_encounter
Create Date: 2026-03-30
"""

from typing import Sequence, Union

revision: str = "fd1914927d78"
down_revision: Union[str, None] = "001_patient_encounter"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """No-op bridge revision."""
    return None


def downgrade() -> None:
    """No-op bridge revision."""
    return None

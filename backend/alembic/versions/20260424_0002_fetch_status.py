"""add fetch status fields

Revision ID: 20260424_0002
Revises: 20260424_0001
Create Date: 2026-04-24
"""
from alembic import op
import sqlalchemy as sa

revision = "20260424_0002"
down_revision = "20260424_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("series", sa.Column("last_successful_fetch", sa.DateTime(timezone=True), nullable=True))
    op.add_column("series", sa.Column("last_fetch_attempt", sa.DateTime(timezone=True), nullable=True))
    op.add_column(
        "series",
        sa.Column("fetch_status", sa.String(length=32), nullable=False, server_default="not_fetched"),
    )
    op.add_column("series", sa.Column("fetch_error", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("series", "fetch_error")
    op.drop_column("series", "fetch_status")
    op.drop_column("series", "last_fetch_attempt")
    op.drop_column("series", "last_successful_fetch")


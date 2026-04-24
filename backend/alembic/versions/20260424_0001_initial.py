"""initial schema

Revision ID: 20260424_0001
Revises:
Create Date: 2026-04-24
"""
from alembic import op
import sqlalchemy as sa

revision = "20260424_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "series",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("evds_code", sa.String(length=160), nullable=False),
        sa.Column("name", sa.String(length=220), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("source", sa.String(length=120), nullable=False),
        sa.Column("frequency", sa.String(length=32), nullable=False),
        sa.Column("unit", sa.String(length=64), nullable=False),
        sa.Column("category", sa.String(length=96), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("last_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_series_id"), "series", ["id"], unique=False)
    op.create_index(op.f("ix_series_code"), "series", ["code"], unique=True)
    op.create_index(op.f("ix_series_evds_code"), "series", ["evds_code"], unique=True)
    op.create_index(op.f("ix_series_category"), "series", ["category"], unique=False)

    op.create_table(
        "observations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("series_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("value", sa.Numeric(precision=20, scale=6), nullable=False),
        sa.Column("source", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["series_id"], ["series.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("series_id", "date", name="uq_observations_series_date"),
    )
    op.create_index(op.f("ix_observations_id"), "observations", ["id"], unique=False)
    op.create_index(op.f("ix_observations_date"), "observations", ["date"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_observations_date"), table_name="observations")
    op.drop_index(op.f("ix_observations_id"), table_name="observations")
    op.drop_table("observations")
    op.drop_index(op.f("ix_series_category"), table_name="series")
    op.drop_index(op.f("ix_series_evds_code"), table_name="series")
    op.drop_index(op.f("ix_series_code"), table_name="series")
    op.drop_index(op.f("ix_series_id"), table_name="series")
    op.drop_table("series")

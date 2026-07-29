"""create vehicles table

Revision ID: 002_create_vehicles
Revises: 001_create_users
Create Date: 2026-07-29

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002_create_vehicles"
down_revision: Union[str, None] = "001_create_users"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "vehicles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("make", sa.String(length=100), nullable=False),
        sa.Column("model", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("quantity_in_stock", sa.Integer(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_vehicles_id"), "vehicles", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_vehicles_id"), table_name="vehicles")
    op.drop_table("vehicles")

"""add otp_attempts

Revision ID: c3f1a9d2b7e4
Revises: 2bd88629931e
"""
from alembic import op
import sqlalchemy as sa

revision = "c3f1a9d2b7e4"
down_revision = "2bd88629931e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("otp_attempts", sa.Integer(), server_default="0", nullable=False))


def downgrade():
    op.drop_column("users", "otp_attempts")
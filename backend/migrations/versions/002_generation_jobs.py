"""Persist AI generation results and cross-instance request quotas."""
from alembic import op
import sqlalchemy as sa
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("generation_jobs", sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("kind", sa.String(20), nullable=False), sa.Column("status", sa.String(20), nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=False), sa.Column("source_fingerprint", sa.String(64), nullable=False),
        sa.Column("draft_version", sa.Integer(), nullable=True), sa.Column("provider", sa.String(20), nullable=False),
        sa.Column("model", sa.String(100), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True), sa.Column("usage", sa.JSON(), nullable=False),
        sa.Column("result", sa.JSON(), nullable=True), sa.Column("error_code", sa.String(50), nullable=True))
    op.create_index("ix_generation_jobs_project_id", "generation_jobs", ["project_id"])
    op.create_index("ix_generation_jobs_created_at", "generation_jobs", ["created_at"])
    op.create_table("request_quotas", sa.Column("key", sa.String(100), primary_key=True), sa.Column("requests", sa.Integer(), nullable=False))


def downgrade():
    op.drop_table("request_quotas")
    op.drop_index("ix_generation_jobs_created_at", table_name="generation_jobs")
    op.drop_index("ix_generation_jobs_project_id", table_name="generation_jobs")
    op.drop_table("generation_jobs")

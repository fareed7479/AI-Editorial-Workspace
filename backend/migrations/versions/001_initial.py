"""Initial editorial schema."""
from alembic import op
import sqlalchemy as sa
revision = "001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("projects", sa.Column("id", sa.String(36), primary_key=True), sa.Column("title", sa.String(160), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("brief", sa.JSON(), nullable=True))
    op.create_table("sources", sa.Column("id", sa.String(36), primary_key=True), sa.Column("project_id", sa.String(36), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False), sa.Column("title", sa.String(240), nullable=False), sa.Column("url", sa.Text(), nullable=True), sa.Column("content", sa.Text(), nullable=False), sa.Column("kind", sa.String(20), nullable=False), sa.Column("reliability", sa.String(30), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_sources_project_id", "sources", ["project_id"])
    op.create_table("drafts", sa.Column("id", sa.String(36), primary_key=True), sa.Column("project_id", sa.String(36), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True), sa.Column("original", sa.Text(), nullable=False), sa.Column("current", sa.Text(), nullable=False), sa.Column("version", sa.Integer(), nullable=False), sa.Column("suggestions", sa.JSON(), nullable=False), sa.Column("revisions", sa.JSON(), nullable=False))

def downgrade():
    op.drop_table("drafts")
    op.drop_index("ix_sources_project_id", table_name="sources")
    op.drop_table("sources")
    op.drop_table("projects")

"""init

Revision ID: 4a6defb4af2a
Revises: 
Create Date: 2023-03-09 10:43:31.325545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a6defb4af2a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contests',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_full', sa.BOOLEAN(), nullable=False, server_default='False'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('problems',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('count_decided', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('number', sa.String(), nullable=False, unique=True),
    sa.Column('complexity', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contests_problems',
    sa.Column('contest_id', sa.Integer(), nullable=False),
    sa.Column('problem_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['contest_id'], ['contests.id'], ),
    sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], ),
    sa.PrimaryKeyConstraint('contest_id', 'problem_id'),
    sa.UniqueConstraint('problem_id')
    )
    op.create_table('topics',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('problem_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('topics')
    op.drop_table('contests_problems')
    op.drop_table('problems')
    op.drop_table('contests')
    # ### end Alembic commands ###

"""empty message

Revision ID: 0e87eb8f342c
Revises: 9f08874bb748
Create Date: 2020-09-15 20:00:54.736034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e87eb8f342c'
down_revision = '9f08874bb748'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todolists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('listName', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('to_do_list')
    op.add_column('todos', sa.Column('listID', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'todos', 'todolists', ['listID'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.drop_column('todos', 'listID')
    op.create_table('to_do_list',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('listName', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='to_do_list_pkey')
    )
    op.drop_table('todolists')
    # ### end Alembic commands ###

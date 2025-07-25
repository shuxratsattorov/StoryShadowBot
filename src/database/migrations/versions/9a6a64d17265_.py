"""empty message

Revision ID: 9a6a64d17265
Revises: cca682cb9886
Create Date: 2025-07-17 19:11:31.662781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9a6a64d17265'
down_revision: Union[str, None] = 'cca682cb9886'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instagram_accounts',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_instagram_accounts_id'), 'instagram_accounts', ['id'], unique=False)
    op.create_table('instagram_sessions',
    sa.Column('account', sa.String(), nullable=False),
    sa.Column('session', sa.LargeBinary(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_instagram_sessions_id'), 'instagram_sessions', ['id'], unique=False)
    op.drop_index(op.f('ix_referrals_id'), table_name='referrals')
    op.drop_table('referrals')
    op.alter_column('auto_fetch_stories', 'last_time',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Date(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('auto_fetch_stories', 'last_time',
               existing_type=sa.Date(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.create_table('referrals',
    sa.Column('referred_user', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('flag', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.tg_id'], name=op.f('referrals_user_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('referrals_pkey')),
    sa.UniqueConstraint('referred_user', name=op.f('referrals_referred_user_key'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    op.create_index(op.f('ix_referrals_id'), 'referrals', ['id'], unique=False)
    op.drop_index(op.f('ix_instagram_sessions_id'), table_name='instagram_sessions')
    op.drop_table('instagram_sessions')
    op.drop_index(op.f('ix_instagram_accounts_id'), table_name='instagram_accounts')
    op.drop_table('instagram_accounts')
    # ### end Alembic commands ###

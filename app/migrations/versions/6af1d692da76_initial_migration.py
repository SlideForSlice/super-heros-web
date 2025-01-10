"""initial migration

Revision ID: 6af1d692da76
Revises: 
Create Date: 2025-01-07 11:54:12.712844

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6af1d692da76'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем таблицы в правильном порядке
    op.drop_table('chat_messages')  # Сначала удаляем зависимую таблицу
    op.drop_table('support')         # Затем удаляем родительскую таблицу
    op.drop_table('articles')        # И только потом удаляем таблицу articles

    # Изменяем тип столбца hashed_pass в таблице users
    op.alter_column('users', 'hashed_pass',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=False)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_pass',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.create_table('chat_messages',
    sa.Column('message_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('message', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['support.chat_id'], name='chat_messages_chat_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='chat_messages_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('message_id', name='chat_messages_pkey')
    )
    op.create_table('support',
    sa.Column('chat_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('chat_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('solved', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='support_user_id_fkey'),
    sa.PrimaryKeyConstraint('chat_id', name='support_pkey')
    )
    op.create_table('articles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name_of_hero', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('article_body', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('super_powers', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('solo', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('image', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], name='articles_author_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='articles_pkey'),
    sa.UniqueConstraint('name_of_hero', name='articles_name_of_hero_key')
    )
    # ### end Alembic commands ###

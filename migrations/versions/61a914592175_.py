"""empty message

Revision ID: 61a914592175
Revises: 
Create Date: 2021-06-06 16:48:39.574930

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '61a914592175'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('endpoint',
    sa.Column('service_id', postgresql.UUID(), nullable=False),
    sa.Column('prefix', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['service_id'], ['service.id'], ondelete='SET NULL', use_alter=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('service_id', 'prefix', name='uix_endpoint_service_id_prefix')
    )
    op.create_table('groups',
    sa.Column('name', postgresql.ENUM('ADMINS', 'USERS', 'MODERATORS', 'SUPPORTS', 'SUPERADMINS', name='user_types'), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_groups_name'), 'groups', ['name'], unique=True)
    op.create_table('method',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_method_name'), 'method', ['name'], unique=True)
    op.create_table('permission',
    sa.Column('entity', sa.String(), nullable=True),
    sa.Column('entity_type', sa.String(), nullable=True),
    sa.Column('method_id', postgresql.UUID(), nullable=False),
    sa.Column('endpoint_id', postgresql.UUID(), nullable=False),
    sa.Column('service_id', postgresql.UUID(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['endpoint_id'], ['endpoint.id'], ondelete='SET NULL', use_alter=True),
    sa.ForeignKeyConstraint(['method_id'], ['method.id'], ondelete='SET NULL', use_alter=True),
    sa.ForeignKeyConstraint(['service_id'], ['service.id'], ondelete='SET NULL', use_alter=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('entity', 'entity_type', 'method_id', 'endpoint_id', name='uix_permission_entity_entity_type_method_id_endpoint_id')
    )
    op.create_table('service',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_service_name'), 'service', ['name'], unique=True)
    op.create_table('user_groups',
    sa.Column('user_id', postgresql.UUID(), nullable=False),
    sa.Column('group_id', postgresql.UUID(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='SET NULL', use_alter=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL', use_alter=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('users',
    sa.Column('identity', sa.String(), nullable=False),
    sa.Column('claim', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_identity'), 'users', ['identity'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_identity'), table_name='users')
    op.drop_table('users')
    op.drop_table('user_groups')
    op.drop_index(op.f('ix_service_name'), table_name='service')
    op.drop_table('service')
    op.drop_table('permission')
    op.drop_index(op.f('ix_method_name'), table_name='method')
    op.drop_table('method')
    op.drop_index(op.f('ix_groups_name'), table_name='groups')
    op.drop_table('groups')
    op.drop_table('endpoint')
    # ### end Alembic commands ###

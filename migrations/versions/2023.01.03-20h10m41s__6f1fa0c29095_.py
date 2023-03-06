"""empty message

Revision ID: 6f1fa0c29095
Revises: df9668ba2a42
Create Date: 2023-01-03 20:10:41.391998

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from project.models import User
from project.database import db

# revision identifiers, used by Alembic.
revision = '6f1fa0c29095'
down_revision = 'df9668ba2a42'
branch_labels = None
depends_on = None


def copy_password_upgrade():
    class TransferUser(db.Model):
        __tablename__ = 'users'
        __table_args__ = {'extend_existing': True}
        password = sa.Column(sa.String)
        password_ = sa.Column(sa.LargeBinary(), nullable=True)

    connection = op.get_bind()
    session = Session(bind=connection)
    session.execute(sa.update(TransferUser).values(
        password_=func.decode(TransferUser.password, 'escape')
    ))
    session.commit()


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('password_', sa.LargeBinary(), nullable=True)
        )
    copy_password_upgrade()
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password')
        batch_op.alter_column('password_',
                              new_column_name='password',
                              existing_type=sa.LargeBinary(),
                              nullable=False)


def downgrade():
    raise NotImplementedError('Реверс не возможен')

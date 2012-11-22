"""create index on NodeState

Revision ID: 1887cafdea2c
Revises: 4a90237e5674
Create Date: 2012-11-22 15:42:05.458548

"""

# revision identifiers, used by Alembic.
revision = '1887cafdea2c'
down_revision = '4a90237e5674'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('ns_1', 'NodeState', ['time',
                                          'nodeId',
                                          'localtime'])
    pass

def downgrade():
    op.drop_index('ns_1')
    pass

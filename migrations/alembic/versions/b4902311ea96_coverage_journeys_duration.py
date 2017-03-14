"""coverage_journeys_duration

Revision ID: b4902311ea96
Revises: 51007d933cba
Create Date: 2017-03-14 10:28:57.825187

"""

# revision identifiers, used by Alembic.
revision = 'b4902311ea96'
down_revision = '51007d933cba'

from alembic import op
import sqlalchemy as sa
import config
from migrations.utils import get_create_partition_sql_func, get_drop_partition_sql_func, \
    get_create_trigger_sql, get_drop_table_cascade_sql


table = "coverage_journeys_duration"
schema = config.db['schema']


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(table,
                    sa.Column('request_date', sa.DateTime(), nullable=False),
                    sa.Column('region_id', sa.Text(), nullable=False),
                    sa.Column('is_internal_call', sa.SmallInteger(), nullable=False),
                    sa.Column('duration', sa.Integer(), nullable=False),
                    sa.Column('nb', sa.BigInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('region_id', 'is_internal_call', 'request_date', 'duration'),
                    schema=schema
                    )

    op.execute(get_create_partition_sql_func(schema, table))
    op.execute(get_create_trigger_sql(schema, table))


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(get_drop_table_cascade_sql(schema, 'coverage_journeys_duration'))
    op.execute(get_drop_partition_sql_func(table))
    # ### end Alembic commands ###

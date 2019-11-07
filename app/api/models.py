import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression

meta = sa.MetaData()

shelter = sa.Table(
    'shelter',
    meta,
    sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
    sa.Column('shelter_name', sa.String(200), nullable=False),
    sa.Column('full_address', sa.Text(), nullable=True),
    sa.Column('city', sa.String(200), nullable=True),
)

pet = sa.Table(
    'pet',
    meta,
    sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
    sa.Column('pet_name', sa.String(200), nullable=False),
    sa.Column('pet_type', sa.String(200), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=False, server_default=expression.true()),
    sa.Column('added_at', sa.DateTime(), nullable=False, server_default=func.now()),
    sa.Column('adopted_at', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('shelter_id', UUID(as_uuid=True), sa.ForeignKey('shelter.id', ondelete='CASCADE'), nullable=False)
)

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


meta = sa.MetaData()

shelter = sa.Table(
    'shelter', meta,
    sa.Column('id', UUID(as_uuid=True), primary_key=True),
    sa.Column('name', sa.String(200), nullable=False),
    sa.Column('full_address', sa.Text(), nullable=True),
    sa.Column('city', sa.String(200), nullable=True),
    sa.Column('pets_available', sa.Integer(), server_default="0", nullable=True)
)

pet = sa.Table(
    'pet', meta,
    sa.Column('id', UUID(as_uuid=True), primary_key=True),
    sa.Column('name', sa.String(200), nullable=False),
    sa.Column('type', sa.String(200), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=False),
    sa.Column('added_at', sa.DateTime(), nullable=False),
    sa.Column('adopted_at', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('shelter_id', UUID(as_uuid=True), sa.ForeignKey('shelter.id', ondelete='CASCADE'))
)

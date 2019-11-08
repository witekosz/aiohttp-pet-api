from marshmallow import Schema, fields


class ShelterSerializer(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(attribute='shelter_name')
    fullAddress = fields.Str(attribute='full_address')
    city = fields.Str()
    petsAvailable = fields.Int(attribute='pets_available')


class PetSerializer(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(attribute='pet_name')
    type = fields.Str(attribute='pet_type')
    available = fields.Str()
    addedAt = fields.Str(dump_only=True, attribute='added_at')
    adoptedAt = fields.Str(attribute='adoptedAt')
    description = fields.Str()
    shelterId = fields.UUID(dump_only=True, attribute='shelter_id')

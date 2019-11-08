from marshmallow import Schema, fields


class ShelterSerializer(Schema):
    id = fields.UUID(dump_only=True)
    shelter_name = fields.Str()
    full_address = fields.Str()
    city = fields.Str()


class PetSerializer(Schema):
    id = fields.UUID(dump_only=True)
    pet_name = fields.Str()
    pet_type = fields.Str()
    available = fields.Str()
    added_at = fields.Str(dump_only=True)
    adopted_at = fields.Str()
    description = fields.Str()
    shelter_id = fields.UUID(dump_only=True)

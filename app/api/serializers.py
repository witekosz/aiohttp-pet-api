from marshmallow import Schema, fields


class ShelterSerializer(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(attribute='shelter_name', data_key='name')
    fullAddress = fields.Str(attribute='full_address', data_key='fullAddress')
    city = fields.Str()
    petsAvailable = fields.Int(attribute='pets_available', data_key='petsAvailable')

    class Meta:
        fields = ("id", "name", "fullAddress", "city", "petsAvailable")
        ordered = True


class PetSerializer(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(attribute='pet_name', data_key='name')
    type = fields.Str(attribute='pet_type', data_key='type')
    available = fields.Bool()
    addedAt = fields.DateTime(dump_only=True, attribute='added_at', data_key='addedAt')
    adoptedAt = fields.DateTime(attribute='adoptedAt', data_key='adoptedAt')
    description = fields.Str()
    shelterId = fields.UUID(dump_only=True, attribute='shelter_id', data_key='shelter_id')

    class Meta:
        fields = ("id", "name", "type", "available", "addedAt", "adoptedAt", "description", "shelterId")
        ordered = True

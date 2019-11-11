from uuid import UUID


async def validate_uuid4(uuid_string):
    """Custom UUID validator"""
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return None
    return uuid_string

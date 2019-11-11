from api.utils import validate_uuid4


async def test_correct_validate_uuid4_(loop):
    uuid_string = '069cefc7-13d2-4dd2-9269-0df8c9d686c9'

    validation = await validate_uuid4(uuid_string)

    assert validation


async def test_error_validate_uuid4_(loop):
    uuid_string = '069cefc7-1-0dfsomeerrorstring9d686c9'

    validation = await validate_uuid4(uuid_string)

    assert not validation
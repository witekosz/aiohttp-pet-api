

async def test_index_view(aiohttp_client, test_app, loop):
    client = await aiohttp_client(test_app)

    resp = await client.get('/')
    text = await resp.text()

    assert resp.status == 200
    assert 'REST SHELTER API' in text


async def test_get_pets_view(aiohttp_client, test_app, loop):
    client = await aiohttp_client(test_app)

    resp = await client.get('/pets')

    assert resp.status == 200


async def test_post_pets_view_no_data(aiohttp_client, test_app, loop):
    client = await aiohttp_client(test_app)

    resp = await client.post('/pets')
    text = await resp.text()

    assert resp.status == 200
    assert "error" in text
    assert "Send required post form data(shelter-name, full-address, city)" in text


async def test_get_pets_detail_view_dummy_id(aiohttp_client, test_app, loop):
    client = await aiohttp_client(test_app)

    resp = await client.get('/pets/lashfslhdsahsflafdslhsad')
    text = await resp.text()

    assert resp.status == 200
    assert "error" in text
    assert "Invalid UUID format" in text


async def test_delete_pets_view(aiohttp_client, test_app, loop):
    client = await aiohttp_client(test_app)

    resp = await client.delete('/pets/sfdfadssfsda')
    text = await resp.text()

    assert resp.status == 200
    assert "error" in text
    assert "Invalid UUID format" in text



async def test_index_view(aiohttp_client, test_app, loop):
    client = await aiohttp_client(test_app)

    resp = await client.get('/')
    text = await resp.text()

    assert resp.status == 200
    assert 'REST SHELTER API' in text


async def test_get_pets_view(aiohttp_client, test_app, loop):
    client = await aiohttp_client(test_app)

    resp = await client.get('/pets')
    text = await resp.text()

    assert resp.status == 200
    assert 'REST SHELTER API' in text


async def test_post_pets_view(aiohttp_client, test_app, loop):
    client = await aiohttp_client(test_app)

    resp = await client.post('/pets')
    text = await resp.text()

    assert resp.status == 200
    assert 'REST SHELTER API' in text


async def test_get_pets_detail_view(aiohttp_client, test_app, loop):
    client = await aiohttp_client(test_app)

    resp = await client.get('/pets/lashfslhdsahsf')
    text = await resp.text()

    assert resp.status == 200
    assert 'REST SHELTER API' in text


async def test_delete_pets_view(aiohttp_client, test_app, loop):
    client = await aiohttp_client(test_app)

    resp = await client.delete('/pets')
    text = await resp.text()

    assert resp.status == 200
    assert 'REST SHELTER API' in text

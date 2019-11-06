from aiohttp import web


async def index(request):
    """Index view"""
    text = "REST SHELTER API"
    return web.Response(text=text)


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = f"Hello, {name}"
    return web.Response(text=text)


async def test(request):
    data = {'some': 'data'}
    return web.json_response(data)

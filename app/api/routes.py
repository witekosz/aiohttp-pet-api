from api import views


def setup_routes(app):
    """Handles app routing"""
    app.router.add_get('/', views.index)
    app.router.add_get('/test', views.test)
    app.router.add_get('/name/{name}', views.handle)
    app.router.add_get('/pet', views.pets_view)
    app.router.add_get('/shelter', views.shelters_view)

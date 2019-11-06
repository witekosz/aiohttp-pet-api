from api import views


def setup_routes(app):
    """Handles app routing"""
    app.router.add_get('/', views.index)
    app.router.add_get('/test', views.test)
    app.router.add_get('/name/{name}', views.handle)

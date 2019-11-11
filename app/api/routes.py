from api import views


def setup_routes(app):
    """Handles app routing"""
    app.router.add_get('/', views.index)
    app.router.add_view('/pets', views.PetsView)
    app.router.add_view('/pets/{uuid}', views.PetDetailView)
    app.router.add_view('/shelters', views.SheltersView)
    app.router.add_view('/shelters/{uuid}', views.ShelterDetailView)
    app.router.add_view('/shelters/{uuid}/pets', views.ShelterPetsView)

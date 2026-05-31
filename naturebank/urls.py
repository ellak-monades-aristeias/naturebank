from django.urls import path

from naturebank import views
from naturebank.models import Biotope, Species

biotope_list = {
    "queryset": Biotope.objects.all(),
    "allow_empty": True,
    "extra_context": {},
}

species_list = {
    "queryset": Species.objects.all(),
    "allow_empty": True,
    "extra_context": {},
}

urlpatterns = [
    path("biotopes/", views.BiotopeListView.as_view(), name="biotope_list"),
    path(
        "biotopes/d/<int:pk>/",
        views.BiotopeDetailView.as_view(),
        name="biotope_detail",
    ),
    path(
        "biotopes/c/<str:site_code>/",
        views.BiotopeDetailView.as_view(),
        name="biotope_detail",
    ),
    path(
        "biotopes/b/<int:pk>/",
        views.BiotopeDetailBriefView.as_view(),
        name="biotope_brief",
    ),
    path("biotope_list_filter/<str:filter_name>/", views.biotope_list_filter),
    path("species/", views.SpeciesListView.as_view(), name="species_list"),
    path(
        "species/d/<int:pk>/",
        views.SpeciesDetailView.as_view(),
        name="species_detail",
    ),
    path("<str:layer>/kml/", views.kml, {}),
    path("bound/", views.bound, {}),
    path("settlements/", views.settlements_kml, {}),
]

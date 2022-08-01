from django.urls import path
from .views.appviews import *

app_name = "transport"

urlpatterns = [
    path("routes/<int:pk>/", RouteItemView.as_view(), name="routes_item"),
    path("routes/", RouteListView.as_view(), name="routes_list"),
    path("riders/", RiderListView.as_view(), name="riders_list"),
]

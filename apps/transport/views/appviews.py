from django.views.generic import ListView, DetailView

from ..models import BusRoute, BusRider


class RouteListView(ListView):
    template_name = "routes/list.html"
    model = BusRoute


class RouteItemView(DetailView):
    template_name = "routes/route_item.html"
    queryset = BusRoute.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["riders"] = BusRider.objects.filter(
            route_id=self.kwargs.get("pk", None)
        )
        return context


class RiderListView(ListView):
    template_name = "riders/list.html"
    model = BusRider
    queryset = BusRider.objects.all()

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(route_id=self.kwargs.get("pk", None))

        print(queryset)

        return queryset

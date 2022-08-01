from django.views.generic import TemplateView, DetailView, ListView

from ..models import BusRoute, BusRider


class RouteListView(TemplateView):
    template_name = "routes/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = [x.as_dict() for x in BusRoute.objects.all()]
        return context


class RouteItemView(DetailView):
    template_name = "routes/item.html"
    queryset = BusRoute.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["riders"] = BusRider.objects.filter(
            route_id=self.kwargs.get("pk", None)
        ).order_by("route__route", "time", "rider__last_name")

        return context


class RiderListView(ListView):
    template_name = "riders/list.html"
    queryset = BusRider.objects.all()

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        if "pk" in self.kwargs:
            queryset = queryset.filter(route_id=self.kwargs["pk"])

        grade = self.request.GET.get("grade", None)
        if grade:
            if grade == "F":
                queryset = queryset.filter(rider__category="faculty")
            else:
                queryset = queryset.filter(rider__grade=grade)
        if "category" in self.request.GET:
            queryset = queryset.filter(rider__category=self.request.GET["category"])

        queryset = queryset.order_by("route__route", "time", "rider__last_name")

        return queryset

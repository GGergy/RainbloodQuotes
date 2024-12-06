from typing import Any

from django.views.generic import ListView

from quotes.models import Quote, Video, simplify


class Overview(ListView):
    model = Quote
    template_name = "search/overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["videos"] = Video.objects.all().only("id", "title")
        context["text_val"] = ""
        context["order_by_val"] = ""
        context["video_val"] = 0
        return context


class SearchView(Overview):

    def param(self, key: str, default: Any = ""):
        res = self.request.GET.get(key)
        return res if res else default

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by(self.param("order_by", "-created_at"))
        if self.param("video").isdigit():
            queryset = queryset.filter(video__id=int(self.param("video")))
        if self.param("text"):
            queryset = queryset.filter(search_string__contains=simplify(self.param("text")))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text_val"] = self.param("text", "")
        context["order_by_val"] = self.param("order_by", "")
        context["video_val"] = self.param("video", 0)
        return context
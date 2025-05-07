from django.views.generic import TemplateView

from quotes.models import Quote


class HomepageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quotes"] = Quote.objects.order_by("?")[:5]
        return context

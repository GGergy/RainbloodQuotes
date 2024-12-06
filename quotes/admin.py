from django.contrib import admin

from quotes.models import Video, Quote, Rate

class RatingInline(admin.StackedInline):
    model = Rate


class QuoteAdmin(admin.ModelAdmin):
    inlines = (RatingInline,)
    readonly_fields = ("created_at", "search_string")


admin.site.register(Video)
admin.site.register(Quote, QuoteAdmin)

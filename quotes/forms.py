from django.forms import ModelForm, TimeField, TimeInput
from django.utils.translation import gettext

from quotes.models import Quote


class QuoteForm(ModelForm):
    time = TimeField(label=gettext("time"), widget=TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Quote
        exclude = ['author', 'time', 'search_string']

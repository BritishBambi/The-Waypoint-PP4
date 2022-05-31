from django import forms
from game.models import Review, RATE_CHOICES


class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'materialize-textarea text-white'}), required=False)
    rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(
        attrs={'class': 'form-display'}), required=True)

    class Meta:
        model = Review
        fields = ('text', 'rate')

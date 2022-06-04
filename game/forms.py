from django import forms
from game.models import Review, RATE_CHOICES


class RateForm(forms.ModelForm):
    """
    Form used to submit a game review. Takes a text area for inputing the
    written review as well as a choice field of scores from 1-10
    """
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'materialize-textarea text-white'}), required=False)
    rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(
        attrs={'class': 'form-display'}), required=True)

    class Meta:
        """ Gives the text and rate form fields to the Review model """
        model = Review
        fields = ('text', 'rate')

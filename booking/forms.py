from django import forms


class BookingForm(forms.Form):
    """
    This form allows users to select a class by its ID for booking.

    """
    selected_class_id = forms.IntegerField(widget=forms.HiddenInput)
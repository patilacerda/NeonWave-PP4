from django import forms

class BookingForm(forms.Form):
    selected_class_id = forms.IntegerField(widget=forms.HiddenInput)
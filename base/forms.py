from django import forms
from .models import Room
from django.contrib.auth.models import User

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ["host", "participants    "]

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)

        # Add Tailwind CSS classes to form fields and labels
        self.fields['name'].widget.attrs.update({
            'class': 'bg-white p-2 rounded-md mx-2'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'bg-white p-2 rounded-md mx-2'
        })
        self.fields['name'].label = 'Name:'
        self.fields['description'].label = 'Description:'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
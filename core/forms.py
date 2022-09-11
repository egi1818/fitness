from django import forms
from core.models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class ProfileForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    email = forms.EmailField()

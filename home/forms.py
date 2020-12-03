from django import forms
from . models import ContactMessage

class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactMessage
        fields = ['name','email','subject','message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Name & surename'}),
            'subject': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'email': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'message': forms.Textarea(attrs={'class': 'input', 'placeholder': 'your message', 'roww': '5'})
        }
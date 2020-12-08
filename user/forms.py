from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import EmailInput, FileInput, Select, TextInput
from .models import Profile

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, label='User Name')
    email = forms.EmailField(max_length=60, required=True, label="Email")
    first_name = forms.CharField(max_length= 50, required=False, label="First Name")
    last_name = forms.CharField(max_length=50, required=False, label="Last Name")

    class Meta:
        model = User 
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class UserUpdateForm(UserChangeForm):
    
    class Meta:
        model = User 
        fields = ('username','email', 'first_name', 'last_name')
        widgets = {
            'username':     TextInput(attrs={'class': 'input', 'placeholder':'put your username'}),
            'email':        EmailInput(attrs={'class': 'input', 'placeholder': 'put your Email'}),
            'first_name':   TextInput(attrs={'class': 'input', 'placeholder': 'put your first Name'}),
            'last_name':    TextInput(attrs={'class': 'input', 'placeholder': 'put your Last Name'})
        }


CITY = [
    ('Kabul','Kabul'),
    ('Daykundi','Daykundi'),
    ('Mazar','Mazar'),
    ('Herat','Herat'),
    ('Qandahar','Qandahar'),
]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ('phone','address','city','country','image')
        widgets = {
            'phone':    TextInput(attrs={'class': 'input', 'placeholder': 'phone'}),
            'address':  TextInput(attrs={'class': 'input', 'placeholder': 'address'}),
            'country':  TextInput(attrs={'class': 'input', 'placeholder': 'country'}),
            'city':     Select(attrs={'class': 'input', 'placeholder': 'City'}, choices=CITY),
            'image':    FileInput(attrs={'class': 'input', 'placeholder': 'Image'})
        }

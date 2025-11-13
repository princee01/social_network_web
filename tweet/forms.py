from django import forms
from .models import post, Reaction, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['text', 'photo']
    

class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['reaction_type']

class UserRegForm(UserCreationForm):
    profilePicture=forms.ImageField(required=True)
    email=forms.EmailField(required=True)  
    dateOfBirth=forms.DateField(
        widget=forms.DateInput()
    ) 

    class Meta:
        model=User
        fields=['username','email','password1','password2',]

class Login(forms.Form):
    email=forms.EmailField(required=True)
    password=forms.CharField(widget=forms.PasswordInput(), required=True)

class profileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profilePicture','dateOfBirth']
        exclude=['user']
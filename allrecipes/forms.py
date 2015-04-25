from django import forms
from models import UserProfile
from models import Recipe
from models import Image
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class ContactForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class':'contact-name', 'placeholder': 'Name'}), max_length=20, label='')
    user_email= forms.EmailField(widget=forms.TextInput(attrs={'class':'contact-email','placeholder': 'Email'}), max_length=30,label='')
    user_message=forms.CharField(widget=forms.Textarea(attrs={'class':'contact-message','placeholder': 'Message'}),max_length=100, label='')
    
class UserForm(forms.ModelForm):

    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'reg_fname', 'placeholder': 'First Name'}), max_length=50, label='First Name')    
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'reg_lname', 'placeholder': 'Last Name'}), max_length=50, label='Last Name')
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'reg_uname', 'placeholder': 'UserName'}), max_length=50, label='User Name')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'reg_mail', 'placeholder': 'Email'}), max_length=50, label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}),label='Your Password')
    cpassword = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Rewrite your password'}),label='Confirm Password')
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password')
        
    def clean_cpassword(self):
        password = self.cleaned_data.get("password")
        cpassword = self.cleaned_data.get("cpassword")
        if not cpassword:
            raise forms.ValidationError("You must confirm your password")
        
        if password != cpassword:
            raise forms.ValidationError("Passwords don't match")
        return cpassword
        
class LoginForm(forms.ModelForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'reg_uname', 'placeholder': 'UserName'}), max_length=50, label='User Name')
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'password')
        
 
        
class UserProfileForm(forms.ModelForm):
    website = forms.URLField(widget=forms.TextInput(attrs={'class':'reg_website', 'placeholder': 'Website'}), max_length=50, label='Website')
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
        
class SubmitRecipeForm(forms.ModelForm):
    class Meta:
        model= Recipe
        fields=('name','ingredients','steps')
        
class SubmitRimageForm(forms.ModelForm):
    class Meta:
        model= Image
        fields = ('image',)  

    
class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)
    
class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2

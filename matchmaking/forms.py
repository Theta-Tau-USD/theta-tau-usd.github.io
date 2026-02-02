from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import BrotherProfile, PNMProfile, CustomUser, Badge


class CustomLoginForm(AuthenticationForm):
    """Custom login form with styled fields"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class AdminCreateUserForm(forms.Form):
    """Form for admin to create Brother or PNM accounts"""
    ROLE_CHOICES = [
        ('BROTHER', 'Brother'),
        ('PNM', 'PNM'),
    ]
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'user@example.com'
        })
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email


class BrotherProfileForm(forms.ModelForm):
    """Form for brothers to create their profile"""
    badges = forms.ModelMultipleChoiceField(
        queryset=Badge.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select badges that represent your interests (optional)"
    )
    
    class Meta:
        model = BrotherProfile
        fields = ['name', 'year', 'major', 'photo', 'description', 'badges']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'year': forms.Select(attrs={
                'class': 'form-control'
            }),
            'major': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mechanical Engineering'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Tell PNMs about yourself! Share your interests, hobbies, what you love about Theta Tau, career goals, favorite activities, etc. (minimum 20 characters)'
            }),
        }


class PNMProfileForm(forms.ModelForm):
    """Form for PNMs to create their profile"""
    class Meta:
        model = PNMProfile
        fields = ['name', 'year', 'major', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'year': forms.Select(attrs={
                'class': 'form-control'
            }),
            'major': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Computer Science'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Tell us about yourself! Share your interests, hobbies, career goals, what you\'re looking for in a brother connection, etc. (minimum 20 characters)'
            }),
        }


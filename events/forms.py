from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Event, Registration, Category, UserProfile

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = (
        ('ATTENDEE', 'Attendee (Browse & Register for Tickets)'),
        ('ORGANIZER', 'Organizer (Host & Manage Events)'),
    )

    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        initial='ATTENDEE',
        widget=forms.RadioSelect(attrs={'class': 'role-radio-input'}),
        help_text="Choose account type. Organizers can host events."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            role = self.cleaned_data.get('role', 'ATTENDEE')
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()
        return user


class EventForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Event
        fields = ['title', 'category', 'description', 'location', 'start_time', 'end_time', 'capacity', 'image_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Tech Summit 2026'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Describe the event goals, schedule, and speakers...'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Grand Convention Center or Zoom Link'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'image_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://images.unsplash.com/...'})
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end and end <= start:
            self.add_error('end_time', "End time must be after start time.")
        return cleaned_data


class RegistrationForm(forms.ModelForm):
    tickets_count = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 10})
    )

    class Meta:
        model = Registration
        fields = ['tickets_count']

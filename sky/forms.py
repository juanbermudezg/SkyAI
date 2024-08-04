from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Flight, Airliner, LocationAirport, Flight_AI
from datetime import date

class CreateNewUserForm(UserCreationForm):
    email = forms.CharField(max_length=50, required=True, help_text='Required. Add a valid phone number.')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1']) 
        if commit:
            user.save()
        return user

class ExtendedUserForm(forms.ModelForm):

    name = forms.CharField(max_length=15, required=False)
    lastname = forms.CharField(max_length=15, required=False)
    email = forms.EmailField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('name', 'lastname', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class FlightForm(forms.ModelForm):
    airliner = forms.ModelChoiceField(
        queryset=Airliner.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione una aerolínea"
    )
    from_airport = forms.ModelChoiceField(
        queryset=LocationAirport.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione aeropuerto de salida"
    )
    to_airport = forms.ModelChoiceField(
        queryset=LocationAirport.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione aeropuerto de llegada"
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    std_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    sta_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    
    class Meta:
        model = Flight
        fields = ['flight_number', 'airliner', 'date', 'std_time', 'sta_time', 'from_airport', 'to_airport']
        widgets = {
            'flight_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe el número de vuelo:'}),
        }

class FlightDetailForm(forms.ModelForm):
    airliner = forms.ModelChoiceField(
        queryset=Airliner.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione una aerolínea"
    )
    from_airport = forms.ModelChoiceField(
        queryset=LocationAirport.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione aeropuerto de salida"
    )
    to_airport = forms.ModelChoiceField(
        queryset=LocationAirport.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione aeropuerto de llegada"
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    std_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    sta_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    
    class Meta:
        model = Flight
        fields = ['flight_number', 'airliner', 'date', 'std_time', 'sta_time', 'from_airport', 'to_airport']
        widgets = {
            'flight_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe el número de vuelo:'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
        if self.instance and self.instance.pk:
            self.fields['std_time'].initial = self.instance.hourSTD * 3600 + self.instance.minuteSTD * 60
            self.fields['sta_time'].initial = self.instance.hourSTA * 3600 + self.instance.minuteSTA * 60
            self.fields['date'].initial = date(self.instance.year, self.instance.month, self.instance.day)

class FlightAIDetailForm(forms.ModelForm):
    class Meta:
        model = Flight_AI
        fields = ['status_text', 'hourATD', 'minuteATD', 'hourATA', 'minuteATA']
        widgets = {
            'status_text': forms.TextInput(attrs={'class': 'form-control'}),
            'hourATD': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'HH'}),
            'minuteATD': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'MM'}),
            'hourATA': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'HH'}),
            'minuteATA': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'MM'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.hourATD is not None and self.instance.minuteATD is not None:
                self.fields['hourATD'].initial = self.instance.hourATD
                self.fields['minuteATD'].initial = self.instance.minuteATD
            if self.instance.hourATA is not None and self.instance.minuteATA is not None:
                self.fields['hourATA'].initial = self.instance.hourATA
                self.fields['minuteATA'].initial = self.instance.minuteATA
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
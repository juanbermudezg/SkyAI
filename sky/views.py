from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CreateNewUserForm, FlightAIDetailForm, FlightDetailForm, FlightForm, ExtendedUserForm
from .utils.verification import userVerification, passVerification, emailVerification
from django.contrib.auth import login, authenticate, logout
from .models import User, Flight, Flight_AI
from django.contrib.auth.decorators import login_required
from .utils.functionAI import finalDef
from django.http import Http404

def helloworld(request):
    return render(request, 'construction.html')

def sign_up(request):
    if request.method == 'GET':
        return render(request, 'users/sign_up.html', {
            'form': CreateNewUserForm,
            "error": ''
        })
    else:
        try:

            userTemp, passTemp, emailTemp = userVerification(request.POST["username"]), passVerification(
                request.POST["password1"]), emailVerification(request.POST["email"])
            if len(userTemp+passTemp+emailTemp) == 0 and request.POST["password1"] == request.POST["password2"]:

                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"], email=request.POST["email"])
                user.save()
                login(request, user)
                return redirect('home_page')
            else:
                return render(request, 'users/sign_up.html', {
                    'form': CreateNewUserForm,
                    "error": userTemp+"\n"+passTemp+"\n"+emailTemp
                })
        except:
            return render(request, 'users/sign_up.html', {
                'form': CreateNewUserForm,
                "error": 'Usuario o correo ya existe'
            })


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'users/sign_in.html', {
            'form': AuthenticationForm
        })
    else:
        try:
            user = authenticate(
                request, username=request.POST.get('username'), password=request.POST.get('password'))
            if user is None:
                return render(request, 'users/sign_in.html', {
                    'form': AuthenticationForm,
                    'error': 'Usuario y/o contraseña incorrectas'
                })
            else:
                login(request, user)
                return redirect('home_page')
        except:
            return render(request, 'users/sign_in.html', {
                    'form': AuthenticationForm,
                    'error': 'Usuario y/o contraseña incorrectas'
                })
@login_required
def sign_out(request):
    logout(request)
    return redirect('home_page')

@login_required
def flights(request):
    flights = Flight.objects.filter(user=request.user)
    return render(request, 'vuelos.html', {
        'flights': flights
    })

@login_required
def create_flight(request):
    if request.method == 'GET':
        return render(request, 'create_vuelo.html', {
            'form': FlightForm()
        })
    else:
        try:
            form = FlightForm(request.POST)
            if form.is_valid():
                new_flight = form.save(commit=False)
                date = form.cleaned_data['date']
                std_time = form.cleaned_data['std_time']
                sta_time = form.cleaned_data['sta_time']
                new_flight.year = date.year
                new_flight.month = date.month
                new_flight.day = date.day
                new_flight.hourSTD = std_time.hour
                new_flight.minuteSTD = std_time.minute
                new_flight.hourSTA = sta_time.hour
                new_flight.minuteSTA = sta_time.minute
                new_flight.user = request.user
                new_flight.save()
                return redirect('flights')
            else:
                return render(request, 'create_vuelo.html', {
                    'form': form,
                    'error': 'Ingresa datos válidos'
                })
        except ValueError:
            return render(request, 'create_vuelo.html', {
                'form': FlightForm(),
                'error': 'Ingresa datos válidos'
            })

@login_required
def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    flight_ai, created = Flight_AI.objects.get_or_create(original_flight=flight)
    if request.method == 'POST':
        if 'calculate_flight_ai' in request.POST:
            flight_ai_data = finalDef(flight.calculateAI())
            flight_ai.status_text = flight_ai_data.get('status_text', '')
            flight_ai.hourATD = flight_ai_data.get('hourATD', None)
            flight_ai.minuteATD = flight_ai_data.get('minuteATD', None)
            flight_ai.hourATA = flight_ai_data.get('hourATA', None)
            flight_ai.minuteATA = flight_ai_data.get('minuteATA', None)
            if flight_ai.minuteATD<10:
                flight_ai.minuteATD = '0'+str(flight_ai.minuteATD)
            if flight_ai.minuteATA<10:
                flight_ai.minuteATA = '0'+str(flight_ai.minuteATA)
            flight_ai.save()
            message = flight_ai_data.get('message', 'Datos actualizados correctamente.')
            flight_ai_form = FlightAIDetailForm(instance=flight_ai)
            flight_form = FlightDetailForm(instance=flight)  
            if flight.minuteSTD<10:
                flight.minuteSTD = '0'+str(flight.minuteSTD)
            if flight.minuteSTA<10:
                flight.minuteSTA = '0'+str(flight.minuteSTA)
            return render(request, 'flight_detail.html', {
                'flight_form': flight_form,
                'flight_ai_form': flight_ai_form,
                'flight': flight,
                'message': message,
                'flight_ai': flight_ai,
            })
        else:
            flight_form = FlightDetailForm(request.POST, instance=flight)
            flight_ai_form = FlightAIDetailForm(request.POST, instance=flight_ai)
            
            if flight_form.is_valid() and flight_ai_form.is_valid():
                flight_form.save()
                flight_ai_form.save()
                return redirect('flight_detail', flight_id=flight.id)
    else:
        flight_form = FlightDetailForm(instance=flight)
        flight_ai_form = FlightAIDetailForm(instance=flight_ai)
        if flight.minuteSTD<10:
                flight.minuteSTD = '0'+str(flight.minuteSTD)
        if flight.minuteSTA<10:
            flight.minuteSTA = '0'+str(flight.minuteSTA)
    return render(request, 'flight_detail.html', {
        'flight_form': flight_form,
        'flight_ai_form': flight_ai_form,
        'flight': flight,
        'flight_ai': flight_ai,
    })
    
@login_required
def delete_flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id, user=request.user)
    if request.method == 'POST':
        flight.delete()
        return redirect('flights')
    
@login_required
def profile_detail(request, profile_id):
    user_temp = get_object_or_404(User, id = profile_id)
    if request.user != user_temp:
        raise Http404("No tienes permiso para ver este perfil.")
    return render(request, 'users/profile_detail.html', {
        'profile': user_temp
    })

@login_required
def delete_profile(request, profile_id):
    user_temp = get_object_or_404(User, id = profile_id)
    if request.user != user_temp:
        raise Http404("No tienes permiso para ver este perfil.")
    if request.method == 'POST':
        user_temp.delete()
        return redirect('home_page') 
    return render(request, 'users/user_confirm_delete.html', {'user': user_temp})

@login_required
def update_profile(request, profile_id):
    user_temp = get_object_or_404(User, id = profile_id)
    if request.user != user_temp:
        raise Http404("No tienes permiso para ver este perfil.")
    if request.method == 'POST':
        form = ExtendedUserForm(request.POST, instance=user_temp)
        try:
            emailTemp = emailVerification(request.POST["email"])

            if len(emailTemp) == 0:
                
                if form.is_valid():

                    form.save()

                    return redirect('home_page') 
            else:
                return render(request, 'users/user_form.html', {
                    'form': form,
                    "error": emailTemp
                })
        except:
            return render(request, 'users/user_form.html', {
                'form': form,
                "error": 'Correo ya existe'
            })
        
    else:
        form = ExtendedUserForm(instance=user_temp)
    
    return render(request, 'users/user_form.html', {'form': form})
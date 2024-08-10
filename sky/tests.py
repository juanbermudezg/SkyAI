from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from .models import Flight, Airliner, LocationCountry, LocationAirport, Flight_AI
from .forms import CreateNewUserForm, ExtendedUserForm, FlightForm, FlightDetailForm, FlightAIDetailForm
from django.contrib.auth import get_user_model
from django.utils import timezone
import logging
from sky import views

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
User = get_user_model()

# Pruebas de modelo
'''
class UserModelTestCase(TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)

    def test_create_user(self):
        logger.info("====================================")
        logger.info("Iniciando test_create_user")

        try:
            logger.info("Creando un usuario con username='testuser', email='test@example.com', password='pass1234'")
            user = User.objects.create_user(username='testuser', email='test@example.com', password='pass1234')
            logger.info(f"Usuario creado: {user.username}, {user.email}")

            self.assertEqual(user.email, 'test@example.com')
            self.assertTrue(user.check_password('pass1234'))
            logger.info("test_create_user ejecutado correctamente")

        except Exception as e:
            logger.error(f"Error en test_create_user: {e}")
            raise e

    def test_create_superuser(self):
        logger.info("====================================")
        logger.info("Iniciando test_create_superuser")

        try:
            logger.info("Creando un superusuario con username='admin', email='admin@example.com', password='pass1234'")
            user = User.objects.create_superuser(username='admin', email='admin@example.com', password='pass1234')
            logger.info(f"Superusuario creado: {user.username}, {user.email}, is_staff={user.is_staff}, is_superuser={user.is_superuser}")

            self.assertTrue(user.is_staff)
            self.assertTrue(user.is_superuser)
            logger.info("test_create_superuser ejecutado correctamente")

        except Exception as e:
            logger.error(f"Error en test_create_superuser: {e}")
            raise e

    def test_email_required(self):
        logger.info("====================================")
        logger.info("Iniciando test_email_required")

        try:
            logger.info("Intentando crear un usuario sin email, esto debería lanzar una excepción")
            with self.assertRaises(ValueError):
                User.objects.create_user(username='testuser', email=None)
            logger.info("test_email_required ejecutado correctamente")

        except Exception as e:
            logger.error(f"Error en test_email_required: {e}")
            raise e

class AirlinerModelTestCase(TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)

    def test_create_airliner(self):
        logger.info("====================================")
        logger.info("Iniciando test_create_airliner")

        try:
            logger.info("Creando una aerolínea con name='Test Airliner', path2image='/path/to/image', id2ai=1'")
            airliner = Airliner.objects.create(name='Test Airliner', path2image='/path/to/image', id2ai=1)
            logger.info(f"Aerolínea creada: {airliner.name}, {airliner.path2image}, {airliner.id2ai}")

            self.assertEqual(airliner.name, 'Test Airliner')
            logger.info("test_create_airliner ejecutado correctamente")

        except Exception as e:
            logger.error(f"Error en test_create_airliner: {e}")
            raise e

class LocationCountryModelTestCase(TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)

    def test_create_country(self):
        logger.info("====================================")
        logger.info("Iniciando test_create_country")

        try:
            logger.info("Creando un país con name='Colombia'")
            country = LocationCountry.objects.create(name='Colombia')
            logger.info(f"País creado: {country.name}")

            self.assertEqual(country.name, 'Colombia')
            logger.info("test_create_country ejecutado correctamente")

        except Exception as e:
            logger.error(f"Error en test_create_country: {e}")
            raise e

class LocationAirportModelTestCase(TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)

    def test_create_airport(self):
        logger.info("====================================")
        logger.info("Iniciando test_create_airport")

        try:
            logger.info("Creando un país con name='Colombia'")
            country = LocationCountry.objects.create(name='Colombia')
            logger.info("Creando un aeropuerto con nameAirport='El Dorado', nameCity='Bogotá', nameCountry=Colombia, IATA_Code='BOG'")
            airport = LocationAirport.objects.create(nameAirport='El Dorado', nameCity='Bogotá', nameCountry=country, IATA_Code='BOG')
            logger.info(f"Aeropuerto creado: {airport.nameAirport}, {airport.nameCity}, {airport.IATA_Code}, {airport.nameCountry.name}")

            self.assertEqual(airport.nameCity, 'Bogotá')
            logger.info("test_create_airport ejecutado correctamente")

        except Exception as e:
            logger.error(f"Error en test_create_airport: {e}")
            raise e

    def test_airport_str(self):
        logger.info("====================================")
        logger.info("Iniciando test_airport_str")

        try:
            logger.info("Creando un país con name='Colombia'")
            country = LocationCountry.objects.create(name='Colombia')
            logger.info("Creando un aeropuerto con nameAirport='El Dorado', nameCity='Bogotá', nameCountry=Colombia, IATA_Code='BOG'")
            airport = LocationAirport.objects.create(nameAirport='El Dorado', nameCity='Bogotá', nameCountry=country, IATA_Code='BOG')
            logger.info(f"Prueba de la representación en cadena del aeropuerto: {str(airport)}")

            self.assertEqual(str(airport), 'Bogotá, BOG - Colombia')
            logger.info("test_airport_str ejecutado correctamente")

        except Exception as e:
            logger.error(f"Error en test_airport_str: {e}")
            raise e

class FlightModelTestCase(TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)

    def test_create_flight(self):
        logger.info("====================================")
        logger.info("Iniciando test_create_flight")

        try:
            logger.info("Creando un país con name='Colombia'")
            country = LocationCountry.objects.create(name='Colombia')

            logger.info("Creando una aerolínea con name='Test Airliner', path2image='/path/to/image', id2ai=1'")
            airliner = Airliner.objects.create(name='Test Airliner', path2image='/path/to/image', id2ai=1)

            logger.info("Creando aeropuerto de salida con nameAirport='El Dorado', nameCity='Bogotá', nameCountry=Colombia, IATA_Code='BOG'")
            from_airport = LocationAirport.objects.create(nameAirport='El Dorado', nameCity='Bogotá', nameCountry=country, IATA_Code='BOG')

            logger.info("Creando aeropuerto de llegada con nameAirport='JFK', nameCity='New York', nameCountry=Colombia, IATA_Code='JFK'")
            to_airport = LocationAirport.objects.create(nameAirport='JFK', nameCity='New York', nameCountry=country, IATA_Code='JFK')

            logger.info("Creando un usuario con username='testuser', email='test@example.com', password='pass1234'")
            user = User.objects.create_user(username='testuser', email='test@example.com', password='pass1234')

            logger.info("Creando un vuelo con flight_number='AV123', airliner='Test Airliner', from='El Dorado', to='JFK'")
            flight = Flight.objects.create(flight_number='AV123', airliner=airliner, year=2024, month=8, day=10,
                                           hourSTD=14, minuteSTD=30, hourSTA=18, minuteSTA=45,
                                           from_airport=from_airport, to_airport=to_airport, user=user)
            logger.info(f"Vuelo creado: {flight.flight_number}, {flight.airliner.name}, {flight.from_airport.nameAirport} -> {flight.to_airport.nameAirport}")

            self.assertEqual(flight.flight_number, 'AV123')
            logger.info("test_create_flight ejecutado correctamente")

        except Exception as e:
            logger.error(f"Error en test_create_flight: {e}")
            raise e
'''
#Prueba de vistas
'''
class ViewsTestCase(TestCase):
    def setUp(self):
        # Configurar datos iniciales para las pruebas
        self.client = Client()

        # Crear un usuario
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='securepassword'
        )

        # Crear instancias necesarias para las pruebas
        self.country = LocationCountry.objects.create(name='Colombia')
        self.airport_from = LocationAirport.objects.create(
            nameAirport='El Dorado',
            nameCity='Bogotá',
            nameCountry=self.country,
            IATA_Code='BOG'
        )
        self.airport_to = LocationAirport.objects.create(
            nameAirport='Simón Bolívar',
            nameCity='Santa Marta',
            nameCountry=self.country,
            IATA_Code='SMR'
        )
        self.airliner = Airliner.objects.create(name='Avianca', path2image='path/to/image', id2ai=1)
        self.flight = Flight.objects.create(
            flight_number='AV123',
            airliner=self.airliner,
            year=2024,
            month=8,
            day=9,
            hourSTD=14,
            minuteSTD=30,
            hourSTA=16,
            minuteSTA=45,
            from_airport=self.airport_from,
            to_airport=self.airport_to,
            user=self.user
        )
        self.flight_ai = Flight_AI.objects.create(original_flight=self.flight)

    def test_sign_in_view_post_valid(self):
        logger.info("Running test_sign_in_view_post_valid with username='testuser'")
        response = self.client.post(reverse('sign_in'), {
            'username': 'testuser',
            'password': 'securepassword'
        })
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response content: {response.content}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home_page'))

    def test_create_flight_view_post_valid(self):
        logger.info("Running test_create_flight_view_post_valid with flight details")
        logger.info(f"Airliner ID: {self.airliner.id}")
        logger.info(f"From Airport ID: {self.airport_from.id}")
        logger.info(f"To Airport ID: {self.airport_to.id}")
        self.client.login(username='testuser', password='securepassword')
        response = self.client.post(reverse('create_flight'), {
            'flight_number': 'AV124',
            'airliner': self.airliner.id,
            'date': '2024-08-10',
            'std_time': '15:00',
            'sta_time': '17:00',
            'from_airport': self.airport_from.id,
            'to_airport': self.airport_to.id
        })
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response content: {response.content}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('flights'))
        self.assertTrue(Flight.objects.filter(flight_number='AV124').exists())

    def test_update_profile_view_post_valid(self):
        logger.info("Running test_update_profile_view_post_valid with user ID")
        logger.info(f"User ID: {self.user.id}")
        self.client.login(username='testuser', password='securepassword')
        response = self.client.post(reverse('update_profile', args=[self.user.id]), {
            'username': 'testuser',
            'email': 'newemail@example.com'
        })
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response content: {response.content}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home_page'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_create_user_view_post_valid(self):
        logger.info("Running test_create_user_view_post_valid with new user details")
        response = self.client.post(reverse('sign_up'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response content: {response.content}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home_page'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

'''
#Prueba de formularios
'''
class FormsTestCase(TestCase):
    def setUp(self):
        # Configurar datos iniciales para las pruebas
        self.client = Client()

        # Crear un usuario
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='securepassword'
        )

        # Crear instancias necesarias para las pruebas
        self.country = LocationCountry.objects.create(name='Colombia')
        self.airport_from = LocationAirport.objects.create(
            nameAirport='El Dorado',
            nameCity='Bogotá',
            nameCountry=self.country,
            IATA_Code='BOG'
        )
        self.airport_to = LocationAirport.objects.create(
            nameAirport='Simón Bolívar',
            nameCity='Santa Marta',
            nameCountry=self.country,
            IATA_Code='SMR'
        )
        self.airliner = Airliner.objects.create(name='Avianca', path2image='path/to/image', id2ai=1)
        self.flight = Flight.objects.create(
            flight_number='AV123',
            airliner=self.airliner,
            year=2024,
            month=8,
            day=9,
            hourSTD=14,
            minuteSTD=30,
            hourSTA=16,
            minuteSTA=45,
            from_airport=self.airport_from,
            to_airport=self.airport_to,
            user=self.user
        )
        self.flight_ai = Flight_AI.objects.create(original_flight=self.flight)

    def test_create_new_user_form_valid(self):
        logger.info("Testing CreateNewUserForm with valid data")
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword'
        }
        form = CreateNewUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        logger.info(f"User created with username: {user.username}")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')

    def test_create_new_user_form_invalid(self):
        logger.info("Testing CreateNewUserForm with invalid data")
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'differentpassword'
        }
        form = CreateNewUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        logger.info(f"Form errors: {form.errors}")

    def test_extended_user_form_valid(self):
        logger.info("Testing ExtendedUserForm with valid data")
        form_data = {
            'name': 'John',
            'lastname': 'Doe',
            'email': 'newemail@example.com'
        }
        form = ExtendedUserForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        logger.info(f"User updated with email: {self.user.email}")
        self.assertEqual(self.user.name, 'John')
        self.assertEqual(self.user.lastname, 'Doe')
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_extended_user_form_invalid(self):
        logger.info("Testing ExtendedUserForm with invalid data")
        form_data = {
            'name': 'John',
            'lastname': 'Doe',
            'email': 'invalidemail'
        }
        form = ExtendedUserForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        logger.info(f"Form errors: {form.errors}")

    def test_flight_form_valid(self):
        logger.info("Testing FlightForm with valid data")
        form_data = {
            'flight_number': 'AV124',
            'airliner': self.airliner.id,
            'date': '2024-08-10',
            'std_time': '15:00',
            'sta_time': '17:00',
            'from_airport': self.airport_from.id,
            'to_airport': self.airport_to.id
        }
        form = FlightForm(data=form_data)
        self.assertTrue(form.is_valid())
        flight = form.save()
        logger.info(f"Flight created with number: {flight.flight_number}")
        self.assertEqual(Flight.objects.count(), 1)
        self.assertEqual(flight.flight_number, 'AV124')

    def test_flight_form_invalid(self):
        logger.info("Testing FlightForm with invalid data")
        form_data = {
            'flight_number': 'AV124',
            'airliner': '',  # Invalid data
            'date': '2024-08-10',
            'std_time': '15:00',
            'sta_time': '17:00',
            'from_airport': self.airport_from.id,
            'to_airport': self.airport_to.id
        }
        form = FlightForm(data=form_data)
        self.assertFalse(form.is_valid())
        logger.info(f"Form errors: {form.errors}")

    def test_flight_detail_form_initial(self):
        logger.info("Testing FlightDetailForm initial data")
        form = FlightDetailForm(instance=self.flight)
        self.assertEqual(form.initial['flight_number'], 'AV123')
        self.assertEqual(form.initial['airliner'], self.airliner.id)
        self.assertEqual(form.initial['from_airport'], self.airport_from.id)
        self.assertEqual(form.initial['to_airport'], self.airport_to.id)
        self.assertEqual(form.initial['date'], date(2024, 8, 9))
        self.assertEqual(form.initial['std_time'], 14 * 3600 + 30 * 60)
        self.assertEqual(form.initial['sta_time'], 16 * 3600 + 45 * 60)

    def test_flight_detail_form_disabling(self):
        logger.info("Testing FlightDetailForm disabling of fields")
        form = FlightDetailForm(instance=self.flight)
        for field in form.fields.values():
            self.assertTrue(field.widget.attrs.get('disabled'))

    def test_flight_ai_detail_form_initial(self):
        logger.info("Testing FlightAIDetailForm initial data")
        form = FlightAIDetailForm(instance=self.flight_ai)
        self.assertEqual(form.initial['status_text'], 'On Time')
        self.assertEqual(form.initial['hourATD'], 14)
        self.assertEqual(form.initial['minuteATD'], 30)
        self.assertEqual(form.initial['hourATA'], 16)
        self.assertEqual(form.initial['minuteATA'], 45)

    def test_flight_ai_detail_form_disabling(self):
        logger.info("Testing FlightAIDetailForm disabling of fields")
        form = FlightAIDetailForm(instance=self.flight_ai)
        for field in form.fields.values():
            self.assertTrue(field.widget.attrs.get('disabled')
'''
#Pruebas de URLs
'''
class URLTests(SimpleTestCase):
    def test_home_page_url_resolves(self):
        url = reverse('home_page')
        logger.debug(f'Testing URL: {url}')
        self.assertEqual(resolve(url).func, views.helloworld)
        logger.info(f'URL {url} resolves to {views.helloworld.__name__}')

    def test_sign_up_url_resolves(self):
        url = reverse('sign_up')
        logger.debug(f'Testing URL: {url}')
        self.assertEqual(resolve(url).func, views.sign_up)
        logger.info(f'URL {url} resolves to {views.sign_up.__name__}')

    def test_sign_in_url_resolves(self):
        url = reverse('sign_in')
        logger.debug(f'Testing URL: {url}')
        self.assertEqual(resolve(url).func, views.sign_in)
        logger.info(f'URL {url} resolves to {views.sign_in.__name__}')

    def test_sign_out_url_resolves(self):
        url = reverse('sign_out')
        logger.debug(f'Testing URL: {url}')
        self.assertEqual(resolve(url).func, views.sign_out)
        logger.info(f'URL {url} resolves to {views.sign_out.__name__}')

    def test_flights_url_resolves(self):
        url = reverse('flights')
        logger.debug(f'Testing URL: {url}')
        self.assertEqual(resolve(url).func, views.flights)
        logger.info(f'URL {url} resolves to {views.flights.__name__}')

    def test_flight_detail_url_resolves(self):
        url = reverse('flight_detail', args=[1])
        logger.debug(f'Testing URL: {url} with args [1]')
        self.assertEqual(resolve(url).func, views.flight_detail)
        logger.info(f'URL {url} resolves to {views.flight_detail.__name__}')

    def test_delete_flight_url_resolves(self):
        url = reverse('delete_flight', args=[1])
        logger.debug(f'Testing URL: {url} with args [1]')
        self.assertEqual(resolve(url).func, views.delete_flight)
        logger.info(f'URL {url} resolves to {views.delete_flight.__name__}')

    def test_create_flight_url_resolves(self):
        url = reverse('create_flight')
        logger.debug(f'Testing URL: {url}')
        self.assertEqual(resolve(url).func, views.create_flight)
        logger.info(f'URL {url} resolves to {views.create_flight.__name__}')

    def test_profile_detail_url_resolves(self):
        url = reverse('profile_detail', args=[1])
        logger.debug(f'Testing URL: {url} with args [1]')
        self.assertEqual(resolve(url).func, views.profile_detail)
        logger.info(f'URL {url} resolves to {views.profile_detail.__name__}')

    def test_delete_profile_url_resolves(self):
        url = reverse('delete_profile', args=[1])
        logger.debug(f'Testing URL: {url} with args [1]')
        self.assertEqual(resolve(url).func, views.delete_profile)
        logger.info(f'URL {url} resolves to {views.delete_profile.__name__}')

    def test_update_profile_url_resolves(self):
        url = reverse('update_profile', args=[1])
        logger.debug(f'Testing URL: {url} with args [1]')
        self.assertEqual(resolve(url).func, views.update_profile)
        logger.info(f'URL {url} resolves to {views.update_profile.__name__}')
'''
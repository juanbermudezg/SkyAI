from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import date, time


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=35, unique=True)
    name = models.CharField(max_length=15, null=True)
    lastname = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
class Airliner(models.Model):
    name = models.CharField(max_length=25)
    path2image= models.TextField(max_length=30)
    id2ai=models.IntegerField()
    def __str__(self):
        return self.name
class LocationCountry(models.Model):
    name = models.TextField(max_length=30)
class LocationAirport(models.Model):
    nameAirport = models.TextField(max_length=100)
    nameCity = models.TextField(max_length=50)
    nameCountry = models.ForeignKey(LocationCountry, on_delete=models.CASCADE)
    IATA_Code = models.CharField(max_length=3)
    def __str__(self) -> str:
        return self.nameCity + ', ' + self.IATA_Code + ' - ' + self.nameCountry.name
class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    airliner = models.ForeignKey(Airliner, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    hourSTD = models.IntegerField()
    minuteSTD = models.IntegerField()
    hourSTA = models.IntegerField()
    minuteSTA = models.IntegerField()
    from_airport = models.ForeignKey(LocationAirport,related_name='flights_departing', on_delete=models.CASCADE)
    to_airport = models.ForeignKey(LocationAirport, related_name='flights_arriving', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def calculateAI(self):
        return {
            'airliner': self.airliner.id2ai,
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'hourSTD': self.hourSTD,
            'minuteSTD': self.minuteSTD,
            'hourSTA': self.hourSTA,
            'minuteSTA': self.minuteSTA,
            'from_location': self.from_airport.IATA_Code,
            'to_location': self.to_airport.IATA_Code,
            'airlinerName': self.airliner.name
        }
    @property
    def flight_date(self):
        try:
            return date(self.year, self.month, self.day)
        except ValueError:
            return None
class Flight_AI(models.Model):
    original_flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    status_text = models.CharField(max_length=10, null=True, blank=True)
    hourATD = models.IntegerField(null=True, blank=True)
    minuteATD = models.IntegerField(null=True, blank=True)
    hourATA = models.IntegerField(null=True, blank=True)
    minuteATA = models.IntegerField(null=True, blank=True)
    
    @property
    def atd_time(self):
        if self.hourATD is not None and self.minuteATD is not None:
            return time(self.hourATD, self.minuteATD)
        return None
    
    @property
    def ata_time(self):
        if self.hourATA is not None and self.minuteATA is not None:
            return time(self.hourATA, self.minuteATA)
        return None

from django.db import models
from django.urls import reverse
from datetime import date, timedelta

# Import the User
from django.contrib.auth.models import User

TYPES = (
   ('F', 'FERTILIZER'),
   ('S', 'SOAK'),
   ('M', 'MIST')
)

# Create your models here.
class Vessel(models.Model):
   name = models.CharField(max_length=50)
   color = models.CharField(max_length=50)
   description = models.TextField(max_length=250)

   def __str__(self):
      return self.name

   def get_absolute_url(self):
       return reverse("vessels_detail", kwargs={"pk": self.id})
   

class Plant(models.Model):
   name = models.CharField(max_length=100)
   species = models.CharField(max_length=100)
   description = models.TextField(max_length=250)
   age = models.IntegerField()
   vessels = models.ManyToManyField(Vessel)
   owner = models.ForeignKey(User, on_delete=models.CASCADE)

   def __str__(self):
      return self.name

   def get_absolute_url(self):
       return reverse("detail", kwargs={"plant_id": self.id})

   def watered_for_week(self):
      today = date.today()
      week_ago = today - timedelta(days=7)
      print(week_ago)
      return self.watering_set.filter(date__range=(week_ago , today)).count()

# Watering Model
class Watering(models.Model):
   date = models.DateField('watering date')
   type = models.CharField(
      max_length=1,
      choices=TYPES,
      default=TYPES[2][0]
   )
   #Foreign key of Plant
   plant = models.ForeignKey(Plant, on_delete=models.CASCADE, null=True)

   def __str__(self):
      return f"{self.get_type_display()} on {self.date}"

   class Meta:
      ordering = ['-date']

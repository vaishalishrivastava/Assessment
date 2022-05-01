from django.db import models

# Create your models here.

class HouseData(models.Model):
    date = models.DateTimeField()
    price = models.FloatField()
    bedrooms = models.IntegerField()
    bathrooms = models.FloatField()
    sqft_living = models.FloatField()
    sqft_lot = models.FloatField()
    floors = models.FloatField()
    waterfront = models.BooleanField()
    view = models.IntegerField()
    condition = models.IntegerField()
    sqft_above = models.FloatField()
    sqft_basement = models.FloatField()
    yr_built = models.IntegerField()
    yr_renovated = models.IntegerField()
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    statezip = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    class Meta:
        db_table = 'house_data'

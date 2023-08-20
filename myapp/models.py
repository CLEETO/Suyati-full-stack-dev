from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import pickle
import os

'''class MLModel(models.Model):
    def load_model(self):
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SavedModels', 'modelsrandom_forest_regressor.pkl')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model

    def predict(self, input_data):
        model = self.load_model()
        prediction = model.predict(input_data)   
        return prediction'''

        
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)


    def __str__(self):
        return self.user.username



class Listing(models.Model):
    listing_id = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=100,blank=True, null=True)
    estimated_price = models.DecimalField(max_digits=20, decimal_places=2)
    address = models.CharField(max_length=100,blank=True, null=True)
    location= models.CharField(max_length=100,blank=True, null=True)
    description = models.CharField(max_length=100,blank=True, null=True)
    feature = models.IntegerField(blank=True, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    garage_space = models.IntegerField(blank=True, null=True)
    parking_space = models.IntegerField(blank=True, null=True)
    spa = models.CharField(max_length=10,blank=True, null=True)
    association = models.CharField(max_length=10,blank=True, null=True)
    heating = models.CharField(max_length=10,blank=True, null=True)
    cooling = models.CharField(max_length=10,blank=True, null=True)
    bedrooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    floors = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='',default='static/images/listing1.png')
    def __str__(self):
        return f'{self.listing_id}: {self.property_name} ({self.user.username})'
    


class userwishlist(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   listingid = models.CharField(max_length=10)
   def __str__(self):
        return f'{self.listingid}: ({self.user.username})'



from django.db import models

class modeldata(models.Model):
    livingAreaSqFt = models.FloatField()
    numOfBathrooms = models.FloatField()
    lotSizeSqFt = models.FloatField()
    numOfBedrooms = models.IntegerField()
    numOfStories = models.IntegerField()
    numOfPhotos = models.IntegerField()
    hasSpa = models.BooleanField()
    hasView = models.BooleanField()
    numOfPatioAndPorchFeatures = models.IntegerField()
    numOfParkingFeatures = models.IntegerField()
    latest_saleyear = models.IntegerField()
    numOfSecurityFeatures = models.IntegerField()
    latestPrice = models.DecimalField(max_digits=10, decimal_places=2)

    


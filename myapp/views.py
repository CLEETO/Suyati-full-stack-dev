from django.shortcuts import render
from django.contrib.auth.models import User
from myapp.models import UserProfile
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import pickle
import os
from .models import Listing,userwishlist,modeldata
import random
from django.db import models
#from .models import MLModel



model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SavedModels', 'modelsrandom_forest_regressor.pkl')

def deleteproperty(request):
  if request.user.is_authenticated: 
   listings = Listing.objects.filter(listing_id=request.GET.get('id'))
   listings.delete()
   listings2 = userwishlist.objects.filter(listingid=request.GET.get('id'))
   listings2.delete()
   return redirect('/listings')
  else:
   return redirect('/login') 


def start(request):
    return  redirect('/home1')

def wishlistproperty(request):
 if request.user.is_authenticated:
   user = request.user
   listing_id = request.GET.get('id')
   if userwishlist.objects.filter(user=user, listingid=listing_id).exists():
       listings = userwishlist.objects.filter(listingid=listing_id)
       listings.delete()
       return redirect(f'/property/?id={listing_id}')
   else:
      wishlist=userwishlist(user=user,listingid=listing_id)
      wishlist.save()
   return redirect(f'/property/?id={listing_id}')
 else:
   return redirect('/loginpage') 





global k
def predicted(request):
   property_name = request.POST.get('property_name')
   price = request.POST.get('price')
   description = request.POST.get('description')
   latitude = request.POST.get('latitude')
   longitude = request.POST.get('longitude')
   address = request.POST.get('address')
   area = request.POST.get('area')
   garage_space = request.POST.get('garage_space')
   parking_space = request.POST.get('parking_space')
   spa = request.POST.get('spa')
   association = request.POST.get('association')
   heating=request.POST.get('heating')
   cooling=request.POST.get('cooling')
   bedrooms=request.POST.get('bedrooms')
   bathrooms=request.POST.get('bathrooms')
   floors=request.POST.get('floors')
   image=request.FILES.get('image')
   context= {
'property_name': property_name ,
'price': price ,
'description': description ,
'latitude': latitude ,
'longitude': longitude ,
'address': address ,
'area': area ,
'garage_space': garage_space ,
'parking_space': parking_space ,
'spa': spa ,
'association': association ,
'heating': heating ,
'cooling': cooling ,
'bedrooms': bedrooms ,
'bathrooms': bathrooms ,
'floors': floors 
}
   choose={'Yes':1,'No':0}
   spa=choose[spa]
   association=choose[association]
   with open(model_path, 'rb') as f:
    model = pickle.load(f)
   global k
   k=random.randint(5,50)
   data = [longitude,bathrooms,area,bedrooms,floors,k,spa,association,parking_space,garage_space,cooling,heating]
   new_data=[data,data]
   #model=MLModel()
   predictions = model.predict(new_data)
   context['EstimatedPrice']= predictions[0]
   
   return render(request, 'listform.html',context)






def generate_listing_id():
    while True:
        listing_id = random.randint(10000, 99999)

        if not Listing.objects.filter(listing_id=listing_id).exists():
            return listing_id
        



def submit(request):
   if request.method == 'POST':
        listing_id = generate_listing_id() 
        user = request.user
        property_name = request.POST.get('property_name')
        estimated_price = request.POST.get('EstimatedPrice')
        price = request.POST.get('price')
        description = request.POST.get('description')
        location = request.POST.get('latitude')
        feature = request.POST.get('longitude')
        address = request.POST.get('address')
        area = request.POST.get('area')
        garage_space = request.POST.get('garage_space')
        parking_space = request.POST.get('parking_space')
        spa = request.POST.get('spa')
        association = request.POST.get('association')
        heating=request.POST.get('heating')
        cooling=request.POST.get('cooling')
        bedrooms=request.POST.get('bedrooms')
        bathrooms=request.POST.get('bathrooms')
        floors=request.POST.get('floors')
        image=request.FILES.get('image')
        listing = Listing(listing_id=listing_id, user=user, property_name=property_name, estimated_price=estimated_price,price=price,
                          description=description,location=location,feature=feature,address=address,area=area,garage_space=garage_space,
                          parking_space=parking_space,spa=spa,association=association,heating=heating,cooling=cooling,bedrooms=bedrooms,
                          bathrooms=bathrooms,floors=floors,image=image)
        listing.save()
        choose={'Yes':1,'No':0}
        spa=choose[spa]
        association=choose[association]
        choose=[False,True]
        listing = modeldata(livingAreaSqFt =float(feature),numOfBathrooms=float(bathrooms),lotSizeSqFt =float(area), numOfBedrooms =int(bedrooms),numOfStories =int(floors),
                          numOfPhotos =int(k),hasSpa =bool(choose[spa]),hasView =bool(choose[association]),numOfPatioAndPorchFeatures =int(parking_space),numOfParkingFeatures =int(garage_space),latest_saleyear =int(cooling),
                          numOfSecurityFeatures =int(heating),latestPrice =price)
        listing.save()
        return redirect('/listings')  
   return redirect('/info')





def aboutus(request):
   return render(request, 'aboutus.html')





def home1(request):
  listings = Listing.objects.all()
  # Create a list of dictionaries containing the property name and estimated price for each listing
  data = [{'image': listing.image.url,'property_name': listing.property_name, 'price': listing.price ,'id': listing.listing_id} for listing in listings]
  data=data[-4:]
  context = {'data': data}
  if request.user.is_authenticated:
     context['authenticated']=1
     return render(request,'home1.html',context)
  else:
     return render(request,'home1.html',context)





def blog(request):
   return render(request,'blog.html')


def loginpage(request):
 if request.user.is_authenticated:
  return redirect('/info')
 else:
  return render(request, 'login.html')






def buypage(request):
  
  if request.method == 'POST':
     location=request.POST.get('location')
     price=request.POST.get('price')
     area=request.POST.get('area')
     if location:
        listings = Listing.objects.filter(location=location)
     else:
        listings = Listing.objects.all()
     if price:
        if int(price)==1:
           listings = listings.order_by('-price')
        else:
           listings = listings.order_by('price')
     if area:
        if int(area)==1:
           listings = listings.order_by('-area')
        else:
           listings = listings.order_by('area')
  else:
        listings = Listing.objects.all()
  data = [{'property_name': listing.property_name, 'price': listing.price ,'id': listing.listing_id,'image':listing.image.url} for listing in listings]
  context = {'data': data}
  if request.user.is_authenticated:
     context['authenticated']=1
  if len(context) > 0:
    return render(request, 'buypage.html',context)
  else:
    return render(request, 'buypage.html')
  





def signuppage(request):
 if request.user.is_authenticated:
  return redirect('/info')
 else:
  return render(request, 'signuppage.html')






def property(request):
  id=request.GET.get('id')
  listing= Listing.objects.filter(listing_id=id)
  context={'data':listing[0]}
  if request.user.is_authenticated:
     context['authenticated']=1
     user_profile = context['data'].user.userprofile
     context['no']=user_profile.phone_number
     wishlistings = userwishlist.objects.filter(user=request.user)
     if wishlistings:
        listing_ids = [wishlist.listingid for wishlist in wishlistings]
        if id in listing_ids:
           context['wishlisted']=1
     
  if request.user==listing[0].user:
     context['usersame']=1
  
        
  #print(listing[0].image)
  return render(request, 'property.html',context)






def listform(request):
  if request.user.is_authenticated:
    return render(request, 'listform.html')
  else:
        return redirect('/loginpage')






def wishlist(request):
  if request.user.is_authenticated:
    wishlistings = userwishlist.objects.filter(user=request.user)
    listing_ids = [wishlist.listingid for wishlist in wishlistings]
    listings = Listing.objects.filter(listing_id__in=listing_ids)
    data = [{'property_name': listing.property_name, 'price': listing.price ,'id': listing.listing_id,'image': listing.image.url} for listing in listings]
    data.append({'image': '/static/images/add.jpg'})
    context = {'data': data}
    context['wishlist']=1
    if len(context) > 0:
      return render(request, 'wishlist.html',context)
    else:
      return render(request, 'wishlist.html')
  else:
        return redirect('/loginpage')






def listings(request):
    if request.user.is_authenticated:
        listings = Listing.objects.filter(user=request.user)

        # Create a list of dictionaries containing the property name and estimated price for each listing
        data = [{'image': listing.image.url,'property_name': listing.property_name, 'price': listing.price ,'id': listing.listing_id} for listing in listings]
        data.append({'image': '/static/images/add.jpg'})
        context = {'data': data}
        if len(context) > 0:
          return render(request, 'listings.html',context)
        else:
          return render(request, 'listings.html')
           
    else:
        return redirect('/loginpage')
  





def logoutuser(request):
  logout(request)
  return redirect('/loginpage')





def info(request):
  if request.user.is_authenticated:
        user_profile = request.user.userprofile
        first_name = user_profile.first_name
        last_name = user_profile.last_name
        phone_number = user_profile.phone_number
        email = request.user.email
        context = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number
    }
        return render(request, 'info.html',context)
  else:
        return redirect('/loginpage')






def signin(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
    
            return redirect('/home1')
        else:
            return redirect('/loginpage')
    else:
        return HttpResponse(request.method)







def updatenumber(request):
   new_phone_number=request.POST['new_phone_number']
   confirm_phone_number=request.POST['confirm_phone_number']
   if new_phone_number!=confirm_phone_number:
      return redirect('/info')
   else:
      user_profile = request.user.userprofile
      user_profile.phone_number=new_phone_number
      user_profile.save()
      return redirect('/info')
   





def updateemail(request):
   new_email_address=request.POST['new_email_address']
   confirm_email_address=request.POST['confirm_email_address']
   if new_email_address!=confirm_email_address:
      return redirect('/info')
   else:
        user = request.user
        user.email = new_email_address
        user.username = new_email_address
        user.save()
        return redirect('/logoutuser')
   





def updatepassword(request):
   new_password=request.POST['new_password']
   confirm_password=request.POST['confirm_password']
   if new_password!=confirm_password:
      return redirect('/info')
   else:
        user = request.user
        user.set_password(new_password)
        user.save()
        return redirect('/logoutuser')
   




def signup(request):
    
    if request.method == 'POST':
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirm_password']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        phonenumber = request.POST['phone_number']
        if confirmpassword == password:
          user = User.objects.create_user(username=username, email=email, password=password)
          profile = UserProfile.objects.create(user=user, first_name=firstname, last_name=lastname, phone_number=phonenumber)
          return redirect('/loginpage')
        else:
          return redirect('/signup')
    
    return redirect('/signup')
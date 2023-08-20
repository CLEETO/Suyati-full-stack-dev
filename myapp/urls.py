from django.urls import path
from . import views

urlpatterns = [
    path('',views.start, name='start'),
    path('home1/', views.home1, name='home1'),
    #path('home2/', views.home2, name='home2'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('signin/', views.signin, name='signin'),
    path('signuppage/', views.signuppage, name='signuppage'),
    path('signup/', views.signup, name='signup'),
    path('info/', views.info, name='info'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('updatenumber/', views.updatenumber, name='updatenumber'),
    path('updateemail/', views.updateemail, name='updateemail'),
    path('updatepassword/', views.updatepassword, name='updatepassword'),
    path('listform/', views.listform, name='listform'),
    path('predicted/', views.predicted, name='predicted'),
    path('listings/', views.listings, name='listings'),
    path('submit/', views.submit, name='submit'),
    path('wishlist/',views.wishlist, name='wishlist'),
    path('property/', views.property, name='property'),
    path('buypage/', views.buypage, name='buypage'),
    path('deleteproperty/', views.deleteproperty, name='deleteproperty'),
    path('wishlistproperty/', views.wishlistproperty, name='wishlistproperty'),
    path('blog/', views.blog, name='blog'),
    path('aboutus/', views.aboutus, name='aboutus'),
]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
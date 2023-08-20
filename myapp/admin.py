from django.contrib import admin
from .models import Listing,UserProfile,userwishlist,modeldata

admin.site.register(UserProfile)
admin.site.register(Listing)
admin.site.register(userwishlist)
admin.site.register(modeldata)

# Register your models here.

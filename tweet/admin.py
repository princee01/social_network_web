from django.contrib import admin
from .models import post, Reaction,Profile  

# Register your models here.
admin.site.register(post)
admin.site.register(Reaction)
admin.site.register(Profile)
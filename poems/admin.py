from django.contrib import admin

# importing models

from .models import User,User_profile,Poem

admin.site.register(User)
admin.site.register(User_profile)
admin.site.register(Poem)



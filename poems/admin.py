from django.contrib import admin

# importing models

from .models import User,User_profile,Poem,Comment,Library

admin.site.register(User)
admin.site.register(User_profile)
admin.site.register(Poem)
admin.site.register(Comment)

admin.site.register(Library)




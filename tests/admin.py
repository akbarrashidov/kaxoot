from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Questions)
admin.site.register(User)
admin.site.register(Answer)
admin.site.register(Group)
admin.site.register(Level)
admin.site.register(Category)


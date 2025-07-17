from django.contrib import admin
from .models import blogmodel,commentmodel,profilemodel,likemodel
# Register your models here.

admin.site.register(blogmodel)
admin.site.register(commentmodel)
admin.site.register(profilemodel)
admin.site.register(likemodel)

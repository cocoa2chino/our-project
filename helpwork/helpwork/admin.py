from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(TaskType)
admin.site.register(Contact)
admin.site.register(Task)
admin.site.register(Cancel_reason)


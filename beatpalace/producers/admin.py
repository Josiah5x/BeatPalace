from django.contrib import admin
from .models import (
    ProducerProfile,
    ProducerProject,
    ProducerSkill,
)

# Register your models here.
admin.site.register(ProducerProfile)
admin.site.register(ProducerProject)
admin.site.register(ProducerSkill)
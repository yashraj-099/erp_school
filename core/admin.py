from django.contrib import admin
from .models import Role, User, School, Subject, Teacher, Student, FeeRecord, Event
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
class UserAdmin(BaseUserAdmin):
    pass
admin.site.register(Role)
# admin.site.register(User, UserAdmin)
admin.site.register(School)
admin.site.register(Subject)
# admin.site.register(Teacher)
# admin.site.register(Student)
admin.site.register(FeeRecord)
admin.site.register(Event)

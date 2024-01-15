from django.contrib import admin

from .models import Staff, Salary, Attendance


admin.site.register(Staff)
admin.site.register(Salary)
admin.site.register(Attendance)

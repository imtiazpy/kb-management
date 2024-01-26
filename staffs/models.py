from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from datetime import datetime

USER = get_user_model()


designation = (
    ('MANAGER', 'Manager'),
    ('SALESMAN', 'Salesman'),
    ('FARMER', 'Farmer')
)


class Salary(models.Model):
    amount = models.FloatField(_("Amount"), max_length=6)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount}"


class Staff(models.Model):
    user = models.OneToOneField(USER, on_delete=models.CASCADE, related_name='user_staff')
    designation = models.CharField(_("Designation"), max_length=20, choices=designation, blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=11, blank=True, null=True)
    nid = models.CharField(_("NID"), max_length=10, unique=True, blank=True, null=True)
    address = models.TextField(_("Address"), max_length=500, blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    salary = models.ForeignKey(
        Salary, 
        on_delete=models.SET_NULL,
        blank=True, 
        null=True, 
        related_name='salary_staffs'
    )
    created_at = models.DateTimeField(auto_now=True)

    def attendance(self):
        is_attending = Attendance.objects.get(user=self.user, date__date=datetime.now().date())
        if is_attending:
            return True
        return False

    def __str__(self):
        return f"{self.user.username}-designation: {self.designation}"



class Attendance(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='user_attendance')
    date = models.DateTimeField(auto_now=True)
    is_present = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.name} - {self.date}'
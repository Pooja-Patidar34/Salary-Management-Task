from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
class AdminManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Email is required")
        admin = self.model(email=self.normalize_email(email), name=name)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin
    def create_superuser(self, email, name, password):
        admin = self.create_user(email, name, password)
        admin.is_superuser = True
        admin.is_staff = True
        admin.save(using=self._db)
        return admin

class Admin(AbstractBaseUser, PermissionsMixin): 
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile = models.ImageField(upload_to="profiles", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = AdminManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email



class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    base_salary = models.FloatField(default=0) 

    def __str__(self):
         return self.name


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    total_working_days = models.IntegerField()
    total_leave_taken = models.IntegerField()
    overtime = models.FloatField(default=0)
    total_salary_made = models.FloatField(default=0)
    is_salary_calculated = models.BooleanField(default=False) 

    class Meta:
                unique_together=('employee','month','year')
    def __str__(self):
         return f"{self.employee.name} - {self.month}/{self.year}"

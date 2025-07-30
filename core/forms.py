from  django import forms
from .models import *

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = [
            'employee',
            'month',
            'year',
            'total_working_days',
            'total_leave_taken',
            'overtime',
        ]
                  
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'phone', 'department','base_salary']
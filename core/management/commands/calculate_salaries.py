from django.core.management.base import BaseCommand
from  core.models import*
from django.core.mail import send_mail

class Command(BaseCommand):
          def handle(self, *args,**kwargs):
                  salaries=Salary.objects.filter(is_salary_calculated=False)
                  for s in salaries:
                          per_day=s.employee.base_salary/s.total_working_days
                          total_salary=per_day*(s.total_working_days-s.total_leave_taken+s.overtime/8)
                          s.total_salary_made=total_salary
                          s.is_salary_calculated=True
                          s.save()

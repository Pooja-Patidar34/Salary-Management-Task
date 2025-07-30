from core import views
from django.urls import path

urlpatterns = [
    path('',views.admin_login,name="admin_login"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<int:pk>/delete/',views.delete_employee,name='delete'),
    path('salary-list/', views.salary_list, name='salary_list'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('add-salary/', views.add_salary, name='add_salary'),
]

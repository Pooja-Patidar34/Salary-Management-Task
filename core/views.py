from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from .models import *
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.timezone import now
from django.db.models import Sum
from datetime import datetime
from .forms import *

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            admin = Admin.objects.get(email=email)
            if admin.check_password(password):
                request.session['admin_id'] = admin.id
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid password')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin not found')
    return render(request, 'core/admin_login.html')


def dashboard(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')
    employees_count = Employee.objects.count()
    now = datetime.now()
    # ---------- This Month ----------
    this_month = now.month
    this_year = now.year
    current_salaries = Salary.objects.filter(
        month=this_month, year=this_year, is_salary_calculated=True
    )
    total_leaves_current = current_salaries.aggregate(total=Sum('total_leave_taken'))['total'] or 0
    total_days_current = current_salaries.aggregate(total=Sum('total_working_days'))['total'] or 0
    if total_days_current > 0:
        attendance_percentage_current = 100 - (total_leaves_current / total_days_current) * 100
    else:
        attendance_percentage_current = 100
    # ---------- Last Month ----------
    if this_month == 1:
        last_month = 12
        last_year = this_year - 1
    else:
        last_month = this_month - 1
        last_year = this_year
    last_salaries = Salary.objects.filter(
        month=last_month, year=last_year, is_salary_calculated=True
    )
    total_leaves_last = last_salaries.aggregate(total=Sum('total_leave_taken'))['total'] or 0
    total_days_last = last_salaries.aggregate(total=Sum('total_working_days'))['total'] or 0
    if total_days_last > 0:
        attendance_percentage_last = 100 - (total_leaves_last / total_days_last) * 100
    else:
        attendance_percentage_last = 100
    return render(request, 'core/dashboard.html', {
        'employees': employees_count,
        'this_month': round(attendance_percentage_current, 2),
        'last_month': round(attendance_percentage_last, 2),
    })

def salary_details(request):
    salary_list = Salary.objects.filter(is_salary_calculated=True).order_by('-year', '-month')
    paginator = Paginator(salary_list, 3)
    page = request.GET.get('page') or 1 
    salaries = paginator.get_page(page)
    return render(request, 'core/salary_list.html', {'salaries': salaries})

def employee_list(request):
    employees = Employee.objects.all().order_by('id')
    employee_data = []
    for emp in employees:
        latest_salary = Salary.objects.filter(
            employee=emp,
            is_salary_calculated=True
        ).order_by('-year', '-month').first()

        employee_data.append({
            'employee': emp,
            'latest_salary': latest_salary.total_salary_made if latest_salary else 0.0
        })
    return render(request, 'core/employee_list.html', {'employee_data': employee_data})

def salary_list(request):
    salary_qs = Salary.objects.filter(is_salary_calculated=True).order_by('-year', '-month')
    paginator = Paginator(salary_qs, 3) 
    page = request.GET.get('page') or 1
    salaries = paginator.get_page(page)
    return render(request, 'core/salary_list.html', {'salaries': salaries})

def add_employee(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'core/add_employee.html', {'form': form})

def delete_employee(request,pk):
    e=Employee(pk=pk)
    e.delete()
    return redirect('employee_list')

def add_salary(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')
    
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            salary = form.save(commit=False)
            base_salary = salary.employee.base_salary or 0
            working_days = salary.total_working_days or 0
            leaves = salary.total_leave_taken or 0
            overtime = salary.overtime or 0

            # 👉 Set current month and year
            today = datetime.today()
            salary.month = today.month
            salary.year = today.year

            # Salary calculation
            per_day_salary = base_salary / working_days if working_days else 0
            deduction = leaves * per_day_salary
            overtime_payment = overtime * 100

            salary.total_salary_made = base_salary - deduction + overtime_payment
            salary.is_salary_calculated = True
            salary.save()
            messages.success(request, 'Salary record added successfully!')
            return redirect('salary_list')
    else:
        form = SalaryForm()
    
    return render(request, 'core/add_salary.html', {'form': form})

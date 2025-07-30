from django.core.management.base import BaseCommand
from core.models import *

class Command(BaseCommand):
    help = 'Creates a default admin user'

    def handle(self, *args, **kwargs):
        if not Admin.objects.filter(email='admin@email.com').exists():
            Admin.objects.create_user(
                name='Admin',
                email='admin@gmail.com',
                password='admin'
            )
            self.stdout.write(self.style.SUCCESS('✅ Default admin created.'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Admin already exists.'))
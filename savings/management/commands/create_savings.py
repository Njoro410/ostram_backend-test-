from django.core.management.base import BaseCommand
from members.models import Members
from savings.models import SavingsAccount
from datetime import date


class Command(BaseCommand):
    help = 'Create savings instances for all members'

    def handle(self, *args, **options):
        members = Members.objects.all()

        for member in members:
            # Create savings instance for each member
            savings = SavingsAccount(account_owner=member, savings_balance=0, created_on=date.today(
            ), updated_on=date.today())  # Set initial balance as desired
            savings.save()

        self.stdout.write(self.style.SUCCESS(
            'Savings instances created for all members.'))

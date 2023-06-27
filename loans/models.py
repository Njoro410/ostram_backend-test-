from django.db import models
from members.models import Members
from administration.choices import *
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.db import transaction

# Create your models here.


class LoanProduct(models.Model):
    name = models.CharField(max_length=50)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    need_collateral = models.BooleanField(
        help_text='does this type of Loan need Coollateral')
    interest_type = models.CharField(
        max_length=50, choices=INTEREST_TYPE_CHOICES)
    need_guarantor = models.BooleanField(
        help_text='does this type of loan need a gurantor')
    documents = models.ManyToManyField(
        'documentType', help_text="Include documents that are needed here for this particular loan.. You can go to the document section to add or delete document")
    min_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    max_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='loantype_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='loantype_instance_updater', null=True)

    class Meta:
        db_table = "loan_type"

    def __str__(self):
        return self.name


class LoanStatus(models.Model):
    status_name = models.CharField(
        max_length=60, null=True, blank=True, choices=LOAN_STATUS_CHOICES)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='loanStatus_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='loanStatus_instance_updater', null=True)

    class Meta:
        db_table = "loan_status"

    def __str__(self):
        return self.status_name


class Loans(models.Model):
    member = models.ForeignKey(
        Members, on_delete=models.DO_NOTHING, related_name='member')
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.DO_NOTHING)
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    status = models.ForeignKey(LoanStatus, on_delete=models.PROTECT)
    term = models.IntegerField()
    grace_period = models.IntegerField()
    application_date = models.DateField()
    start_date = models.DateField()
    guarantors = models.ManyToManyField(Members, related_name='guarantors')
    reason = models.TextField()
    payment_frequency = models.CharField(
        max_length=50, choices=PAYMENT_FREQUENCY_CHOICES)
    monthly_payment = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    total_interest = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    total_payment = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    excess_payment = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    late_charge_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    total_late_charge = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='loan_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='loan_instance_updater', null=True)

    def clean(self):
        if self.principal_amount < self.loan_product.min_amount:
            raise ValidationError(
                {'principal_amount': f'Amount must be at least {self.loan_product.min_amount} for the selected loan type.'})

    # class Meta:
    #     db_table = "loans"

    def __str__(self):
        return f"{self.member.names}'s loan"

    def save(self, *args, **kwargs):
        self.monthly_payment = self.calculate_monthly_payment()
        self.total_payment = self.get_total_payment()
        self.total_interest = self.get_total_interest()

        self.remaining_balance = self.principal_amount + self.total_interest

        # Update the next interest amount
        self.next_interest_amount = self.get_interest()

        super().save(*args, **kwargs)

    def calculate_monthly_payment(self):
        r = self.loan_product.interest_rate / 100 / 12  # Monthly interest rate
        n = self.term  # Loan term in months
        remaining_balance = self.principal_amount

        if self.loan_product.interest_type == "Simple":
            monthly_payment = (self.principal_amount +
                               (self.principal_amount * r * n)) / n
            installment = monthly_payment
        elif self.loan_product.interest_type == "Compounding":
            monthly_payment = (self.principal_amount * r *
                               (1 + r) ** n) / ((1 + r) ** n - 1)
            interest_amount = remaining_balance * r
            principal_amount = monthly_payment - interest_amount
            installment = interest_amount + principal_amount
            remaining_balance = remaining_balance - principal_amount

        else:
            raise ValueError(
                "Invalid interest type. Choose 'simple' or 'compounded'.")
        return installment

    def get_interest(self):
        remaining_days = (
            self.start_date + timezone.timedelta(days=self.grace_period) - timezone.now().date()).days
        if remaining_days > 0:
            return 0  # Return 0 interest during the grace period
        else:
            interest = self.remaining_balance * \
                (self.loan_product.interest_rate / 100 / 12)
            return interest

    def get_total_payment(self):
        return self.monthly_payment * self.term

    def get_total_interest(self):
        return self.total_payment - self.principal_amount

    def calculate_remaining_balance(self):
        return self.principal_amount + self.total_interest

    def make_payment(self, payment_amount):
        self.remaining_balance -= payment_amount
        if self.remaining_balance <= 0:
            self.excess_payment = abs(self.remaining_balance)
            self.remaining_balance = 0
            self.status = LoanStatus.objects.get(status_name='REPAID')
        else:
            self.excess_payment = 0
        super().save(update_fields=[
            'remaining_balance', 'excess_payment', 'status'])

    def is_defaulted(self):
        grace_period = self.grace_period  # Define the grace period in days
        # Define the number of consecutive missed payments
        consecutive_missed_payments = self.consecutive_missed_payments

        last_payment_date = self.loanrepayment_set.order_by(
            '-payment_date').first().payment_date
        due_date = self.start_date + timedelta(days=(self.term * 30))
        current_date = timezone.now().date()

        if last_payment_date < due_date:
            days_past_due = (current_date - due_date).days
            if days_past_due > grace_period and self.missed_payments_count() >= consecutive_missed_payments:
                return True

        return False

    def missed_payments_count(self):
        return self.loanrepayment_set.filter(payment_date__gt=self.start_date).count()

    def add_late_charge(self):
        if self.days_after_late_repayment > 0:
            current_date = timezone.now().date()
            due_date = self.start_date + \
                timedelta(days=self.days_after_late_repayment)

            if current_date > due_date and self.remaining_balance > 0:
                late_fee = self.monthly_payment * \
                    (self.late_charge_percentage / 100)
                self.late_charge += late_fee
                self.save()


@receiver(post_save, sender=Loans)
def generate_installments(sender, instance, created, **kwargs):
    if created:
        installment_amount = instance.calculate_monthly_payment()
        starter_date = instance.start_date + timedelta(days=30)
        for i in range(instance.term):
            # Assuming 30 days in a month
            due_date = starter_date + timezone.timedelta(days=i * 30)
            Installment.objects.create(
                loan=instance,
                installment_number=i + 1,
                due_date=due_date,
                amount_due=installment_amount,
                total_installment_amount=installment_amount
            )

    @property
    def borrower_membership_number(self):
        return self.member.mbr_no


class Installment(models.Model):
    loan = models.ForeignKey(Loans, on_delete=models.CASCADE)
    due_date = models.DateField()
    installment_number = models.IntegerField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    total_installment_amount = models.DecimalField(
        max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)

    class Meta:
        db_table = "loans_installments"

    def __str__(self):
        return f"{self.loan.member.names}'s {self.installment_number} loan installment."


class LoanRepayment(models.Model):
    loan = models.ForeignKey(Loans, on_delete=models.CASCADE,
                             null=True, blank=True, related_name="loanrepayment_set")
    payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    # is_insterest_included = models.BooleanField(
    #     help_text='is the interest amount already included in the amount')
    # loan_interest = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    payment_date = models.DateField(blank=True, null=True)
    # loan_form_fee = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    # loan_processing_fee = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    # loan_insurance_fee = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    # late_charges = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='loanRepayment_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='loanRepayment_instance_updater', null=True)

    class Meta:
        db_table = "loans_repayment"

    def __str__(self):
        return f"{self.loan.member.names}'s loan repayment"

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        installments = self.loan.installment_set.order_by('installment_number')
        payment_amount = self.payment_amount
        self.loan.make_payment(payment_amount)
        for installment in installments:
            if installment.amount_paid == installment.total_installment_amount:
                continue
            if not installment.paid:
                if payment_amount >= installment.amount_due:
                    payment_amount -= installment.amount_due
                    installment.amount_paid += installment.amount_due
                    installment.amount_due = 0
                    installment.paid = True
                else:
                    installment.amount_due -= payment_amount
                    installment.amount_paid += payment_amount
                    payment_amount = 0
            installment.save()
            if payment_amount == 0:
                break


class Documents(models.Model):
    upload_date = models.DateField(auto_now_add=True)
    loan = models.ForeignKey(
        Loans, on_delete=models.CASCADE, null=True, related_name='loan_documents')
    document_type = models.ForeignKey(
        'documentType', on_delete=models.CASCADE, null=True)
    status = models.ForeignKey("DocumentStatus", on_delete=models.PROTECT)
    file = models.FileField(upload_to='documents/')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='documents_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='documents_instance_updater', null=True)

    class Meta:
        db_table = "documents"

    def __str__(self):
        return f" {self.loan.member.names}'s {self.document_type.name}"


class DocumentStatus(models.Model):
    status_name = models.CharField(
        max_length=60, null=True, blank=True, choices=DOCUMENT_STATUS_CHOICES)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='DocumentStatus_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='DocumentStatus_instance_updater', null=True)

    class Meta:
        db_table = "document_status"

    def __str__(self):
        return self.status_name


class DocumentType(models.Model):
    name = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='documentType_instance_creator', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='documentType_instance_updater', null=True)

    class Meta:
        db_table = "document_type"

    def __str__(self):
        return self.name

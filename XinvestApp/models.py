from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class InvestmentPlan(models.Model):
    name = models.CharField(max_length=100)
    duration_in_days = models.IntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    investment_return = models.DecimalField(max_digits=20, decimal_places=2)
    increament_rate_per_day = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField(null=True, unique=True)
    wallet_address = models.CharField(max_length=100, null=True, blank=True)
    investment_plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, related_name='investment_plans', null=True, blank=True)
    balance = models.IntegerField(default=0)
    STATUS = (
        ('admin', 'admin'),
        ('investor', 'investor'),
    )
    status = models.CharField(max_length=100, choices=STATUS, default='investor')

    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
    
    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transaction_user')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    proof_of_payment = models.ImageField(upload_to='proof_of_payments/', null=True, blank=True)
    TRANSACTION_TYPES = (
        ('deposit', 'deposit'),
        ('withdrawal', 'withdrawal'),
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default='deposit')
    TRANSACTION_STATUS = (
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('declined', 'declined'),
    )
    transaction_status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.transaction_status}"

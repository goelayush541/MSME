from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('MSME', 'MSME Owner'),
        ('BUYER', 'Large Buyer'),
        ('LENDER', 'Financial Institution'),
        ('ADVISOR', 'Business Advisor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100, default='Delhi')
    verified = models.BooleanField(default=False)
    profile_completed = models.BooleanField(default=False)

class MSMEProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255, default='')
    registration_number = models.CharField(max_length=50, blank=True, null=True)
    business_type = models.CharField(max_length=100, default='Manufacturing')
    industry_sector = models.CharField(max_length=100, default='Other')
    years_in_operation = models.IntegerField(default=1)  
    annual_turnover = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    employee_count = models.IntegerField(default=1)
    products_services = models.TextField(default='')
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    udhyam_registration_number = models.CharField(max_length=20, blank=True, null=True)

class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255)
    organization_type = models.CharField(max_length=100)
    industry_sector = models.CharField(max_length=100)
    annual_procurement_budget = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        null=True,  
        blank=True  
    )
    preferred_supplier_criteria = models.TextField()

class LenderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=255)
    institution_type = models.CharField(max_length=100)
    financial_products_offered = models.TextField()
    min_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)

def create_default_site():
    """Function to create default site data if needed"""
    from django.contrib.sites.models import Site
    Site.objects.get_or_create(
        domain='example.com',
        name='MSME Sahayata'
    )

class LoanApplication(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('DISBURSED', 'Disbursed'),
    )
    msme = models.ForeignKey(MSMEProfile, on_delete=models.CASCADE)
    lender = models.ForeignKey('LenderProfile', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    purpose = models.TextField()
    tenure_months = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    applied_date = models.DateTimeField(auto_now_add=True)
    documents = models.JSONField()

class CreditScore(models.Model):
    msme = models.ForeignKey(MSMEProfile, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[MinValueValidator(300), MaxValueValidator(900)]
    )
    last_updated = models.DateTimeField(auto_now=True)
    factors = models.JSONField()

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
    )
    msme = models.ForeignKey(MSMEProfile, on_delete=models.CASCADE)
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    items = models.JSONField()

class InvoiceDiscountingRequest(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    msme = models.ForeignKey(MSMEProfile, on_delete=models.CASCADE)
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

# class LoanApplication(models.Model):
#     STATUS_CHOICES = (
#         ('PENDING', 'Pending'),
#         ('UNDER_REVIEW', 'Under Review'),
#         ('APPROVED', 'Approved'),
#         ('REJECTED', 'Rejected'),
#         ('DISBURSED', 'Disbursed'),
#     )
#     msme = models.ForeignKey(MSMEProfile, on_delete=models.CASCADE)
#     lender = models.ForeignKey(LenderProfile, on_delete=models.CASCADE, null=True, blank=True)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     purpose = models.TextField()
#     tenure_months = models.IntegerField()
#     interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
#     applied_date = models.DateTimeField(auto_now_add=True)
#     documents = models.JSONField()

class ProductListing(models.Model):
    msme = models.ForeignKey(MSMEProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    moq = models.IntegerField(default=1)
    specifications = models.JSONField()
    images = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProcurementRequest(models.Model):
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    expected_price_range = models.CharField(max_length=100)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Bid(models.Model):
    STATUS_CHOICES = (
        ('SUBMITTED', 'Submitted'),
        ('SHORTLISTED', 'Shortlisted'),
        ('REJECTED', 'Rejected'),
        ('AWARDED', 'Awarded'),
    )
    procurement_request = models.ForeignKey(ProcurementRequest, on_delete=models.CASCADE)
    msme = models.ForeignKey(MSMEProfile, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_time = models.CharField(max_length=100)
    terms = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    submitted_at = models.DateTimeField(auto_now_add=True)

class LearningCourse(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    duration_hours = models.IntegerField()
    level = models.CharField(max_length=50)
    instructor = models.CharField(max_length=255)
    thumbnail_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(LearningCourse, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

class BusinessTool(models.Model):
    TOOL_TYPE_CHOICES = (
        ('ERP', 'Enterprise Resource Planning'),
        ('CRM', 'Customer Relationship Management'),
        ('INV', 'Inventory Management'),
        ('ACC', 'Accounting'),
    )
    name = models.CharField(max_length=255)
    tool_type = models.CharField(max_length=3, choices=TOOL_TYPE_CHOICES)
    description = models.TextField()
    access_url = models.URLField()
    tutorial_url = models.URLField()
    is_free = models.BooleanField(default=False)

class MSMEToolSubscription(models.Model):
    msme = models.ForeignKey(MSMEProfile, on_delete=models.CASCADE)
    tool = models.ForeignKey(BusinessTool, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
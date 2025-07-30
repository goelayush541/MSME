from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100, initial='Delhi')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type', 'phone', 'address', 'city']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))

class MSMEProfileForm(forms.ModelForm):
    class Meta:
        model = MSMEProfile
        exclude = ['user']
        widgets = {
            'products_services': forms.Textarea(attrs={'rows': 3}),
        }

class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        exclude = ['user']
        widgets = {
            'preferred_supplier_criteria': forms.Textarea(attrs={'rows': 3}),
        }

class LenderProfileForm(forms.ModelForm):
    class Meta:
        model = LenderProfile
        exclude = ['user']
        widgets = {
            'financial_products_offered': forms.Textarea(attrs={'rows': 3}),
        }

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['amount', 'purpose', 'tenure_months']
        widgets = {
            'purpose': forms.Textarea(attrs={'rows': 3}),
        }

class ProductListingForm(forms.ModelForm):
    class Meta:
        model = ProductListing
        exclude = ['msme', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'specifications': forms.Textarea(attrs={'rows': 3}),
        }

class ProcurementRequestForm(forms.ModelForm):
    class Meta:
        model = ProcurementRequest
        fields = ['title', 'description', 'category', 'quantity', 'expected_price_range', 'deadline']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ['procurement_request', 'msme', 'status', 'submitted_at']
        widgets = {
            'terms': forms.Textarea(attrs={'rows': 3}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'buyer', 'amount', 'issue_date', 'due_date']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class InvoiceDiscountingForm(forms.ModelForm):
    class Meta:
        model = InvoiceDiscountingRequest
        fields = ['requested_amount', 'discount_rate']
        widgets = {
            'requested_amount': forms.NumberInput(attrs={'min': 0}),
            'discount_rate': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.1}),
        }
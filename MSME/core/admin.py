from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'verified', 'profile_completed')
    list_filter = ('user_type', 'verified', 'profile_completed')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_type', 'phone', 'address', 'city', 'verified', 'profile_completed')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('user_type', 'phone', 'address', 'city')}),
    )

@admin.register(MSMEProfile)
class MSMEProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'industry_sector', 'annual_turnover', 'employee_count')
    search_fields = ('business_name', 'gst_number', 'udhyam_registration_number')
    list_filter = ('industry_sector', 'business_type')

@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'industry_sector', 'annual_procurement_budget')
    search_fields = ('organization_name',)

@admin.register(LenderProfile)
class LenderProfileAdmin(admin.ModelAdmin):
    list_display = ('institution_name', 'institution_type', 'min_loan_amount', 'max_loan_amount')
    search_fields = ('institution_name',)

@admin.register(ProductListing)
class ProductListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'msme', 'category', 'price')
    search_fields = ('name', 'description')
    list_filter = ('category',)

@admin.register(ProcurementRequest)
class ProcurementRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'buyer', 'category', 'deadline')
    list_filter = ('category', 'deadline')

admin.site.register(User, CustomUserAdmin)
admin.site.register(CreditScore)
admin.site.register(LoanApplication)
admin.site.register(Invoice)
admin.site.register(InvoiceDiscountingRequest)
admin.site.register(Bid)
admin.site.register(LearningCourse)
admin.site.register(Enrollment)
admin.site.register(BusinessTool)
admin.site.register(MSMEToolSubscription)
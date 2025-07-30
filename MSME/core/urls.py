from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),
  
    # Profile Completion
    path('profile/msme/', views.complete_msme_profile, name='complete_msme_profile'),
    path('profile/buyer/', views.complete_buyer_profile, name='complete_buyer_profile'),
    path('profile/lender/', views.complete_lender_profile, name='complete_lender_profile'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Finance Module
    path('finance/', views.finance_dashboard, name='finance_dashboard'),
    path('finance/apply-loan/', views.apply_for_loan, name='apply_loan'),
    path('finance/loan/<int:pk>/', views.loan_detail, name='loan_detail'),
    path('finance/credit-score/', views.calculate_credit_score, name='calculate_credit_score'),
    path('finance/invoices/', views.invoice_list, name='invoice_list'),
    path('finance/invoices/add/', views.add_invoice, name='add_invoice'),
    path('finance/invoices/discount/<int:pk>/', views.request_invoice_discounting, name='request_invoice_discounting'),
    path('finance/options/', views.view_finance_options, name='finance_options'),
    
    # Marketplace
    path('marketplace/', views.marketplace, name='marketplace'),
    path('marketplace/product/<int:pk>/', views.product_detail, name='product_detail'),
    path('marketplace/procurement/<int:pk>/', views.procurement_detail, name='procurement_detail'),
    path('marketplace/bid/<int:pk>/', views.submit_bid, name='submit_bid'),
    path('marketplace/post-requirement/', views.post_requirement, name='post_requirement'),
    
    # Learning Hub
    path('learning/', views.learning_hub, name='learning_hub'),
    path('learning/course/<int:pk>/', views.course_detail, name='course_detail'),
    path('learning/enroll/<int:pk>/', views.enroll_course, name='enroll_course'),
    path('learning/my-courses/', views.my_courses, name='my_courses'),
    
    # Business Tools
    path('tools/', views.business_tools, name='business_tools'),
    path('tools/subscribe/<int:pk>/', views.subscribe_tool, name='subscribe_tool'),
    path('tools/erp/', views.erp_dashboard, name='erp_dashboard'),
    path('tools/inventory/', views.inventory_management, name='inventory_management'),
    path('tools/crm/', views.crm_dashboard, name='crm_dashboard'),
]
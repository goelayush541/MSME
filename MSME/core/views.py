from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import *
from .forms import *


# Authentication Views
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create empty profile immediately
            try:
                if user.user_type == 'MSME':
                    MSMEProfile.objects.create(user=user)
                elif user.user_type == 'BUYER':
                    BuyerProfile.objects.create(user=user)
                elif user.user_type == 'LENDER':
                    LenderProfile.objects.create(user=user)
            except Exception as e:
                messages.error(request, "Error creating your profile. Please contact support.")
                return redirect('register')
            
            login(request, user)
            return redirect('complete_profile')  # Redirect to profile completion
            
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Check if profile exists, if not create empty one
                try:
                    if user.user_type == 'MSME' and not hasattr(user, 'msmeprofile'):
                        MSMEProfile.objects.create(user=user)
                    elif user.user_type == 'BUYER' and not hasattr(user, 'buyerprofile'):
                        BuyerProfile.objects.create(user=user)
                    elif user.user_type == 'LENDER' and not hasattr(user, 'lenderprofile'):
                        LenderProfile.objects.create(user=user)
                except Exception as e:
                    messages.error(request, "Error setting up your profile. Please contact support.")
                    return redirect('login')
                
                login(request, user)
                
                # Redirect to profile completion if not completed
                if not user.profile_completed:
                    if user.user_type == 'MSME':
                        return redirect('complete_msme_profile')
                    elif user.user_type == 'BUYER':
                        return redirect('complete_buyer_profile')
                    elif user.user_type == 'LENDER':
                        return redirect('complete_lender_profile')
                
                return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def complete_profile(request):
    if not request.user.profile_completed:
        if request.user.user_type == 'MSME':
            return redirect('complete_msme_profile')
        elif request.user.user_type == 'BUYER':
            return redirect('complete_buyer_profile')
        elif request.user.user_type == 'LENDER':
            return redirect('complete_lender_profile')
    return redirect('dashboard')

# Profile Views
@login_required
def complete_msme_profile(request):
    if request.method == 'POST':
        form = MSMEProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            request.user.profile_completed = True
            request.user.save()
            return redirect('dashboard')
    else:
        form = MSMEProfileForm()
    return render(request, 'registration/profile_msme.html', {'form': form})

@login_required
def complete_buyer_profile(request):
    if request.method == 'POST':
        form = BuyerProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            request.user.profile_completed = True
            request.user.save()
            return redirect('dashboard')
    else:
        form = BuyerProfileForm()
    return render(request, 'registration/profile_buyer.html', {'form': form})

@login_required
def complete_lender_profile(request):
    if request.method == 'POST':
        form = LenderProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            request.user.profile_completed = True
            request.user.save()
            return redirect('dashboard')
    else:
        form = LenderProfileForm()
    return render(request, 'registration/profile_lender.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    context = {}
    
    try:
        if user.user_type == 'MSME':
            profile = MSMEProfile.objects.get(user=user)
            credit_score = CreditScore.objects.filter(msme=profile).first()
            loan_applications = LoanApplication.objects.filter(msme=profile).order_by('-applied_date')[:5]
            products = ProductListing.objects.filter(msme=profile).order_by('-created_at')[:5]
            bids = Bid.objects.filter(msme=profile).order_by('-submitted_at')[:5]
            
            context.update({
                'profile': profile,
                'credit_score': credit_score,
                'loan_applications': loan_applications,
                'products': products,
                'bids': bids
            })
        
        elif user.user_type == 'BUYER':
            profile = BuyerProfile.objects.get(user=user)
            procurement_requests = ProcurementRequest.objects.filter(buyer=profile).order_by('-created_at')[:5]
            bids_received = Bid.objects.filter(procurement_request__buyer=profile).order_by('-submitted_at')[:5]
            
            context.update({
                'profile': profile,
                'procurement_requests': procurement_requests,
                'bids_received': bids_received
            })
        
        elif user.user_type == 'LENDER':
            profile = LenderProfile.objects.get(user=user)
            loan_applications = LoanApplication.objects.filter(lender=profile).order_by('-applied_date')[:5]
            
            context.update({
                'profile': profile,
                'loan_applications': loan_applications
            })
    
    except (MSMEProfile.DoesNotExist, BuyerProfile.DoesNotExist, LenderProfile.DoesNotExist):
        messages.warning(request, 'Please complete your profile to access all features')
        if user.user_type == 'MSME':
            return redirect('complete_msme_profile')
        elif user.user_type == 'BUYER':
            return redirect('complete_buyer_profile')
        elif user.user_type == 'LENDER':
            return redirect('complete_lender_profile')
    
    return render(request, 'dashboard.html', context)

# Finance Module Views
@login_required
def finance_dashboard(request):
    if request.user.user_type != 'MSME':
        return redirect('dashboard')
    
    profile = MSMEProfile.objects.get(user=request.user)
    credit_score = CreditScore.objects.filter(msme=profile).first()
    loan_applications = LoanApplication.objects.filter(msme=profile).order_by('-applied_date')
    invoice_discounting = InvoiceDiscountingRequest.objects.filter(msme=profile).order_by('-created_at')
    
    return render(request, 'finance/dashboard.html', {
        'credit_score': credit_score,
        'loan_applications': loan_applications,
        'invoice_discounting': invoice_discounting
    })

@login_required
def apply_for_loan(request):
    if request.user.user_type != 'MSME':
        return redirect('dashboard')
    
    profile = MSMEProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.msme = profile
            loan.save()
            messages.success(request, 'Loan application submitted successfully!')
            return redirect('finance_dashboard')
    else:
        form = LoanApplicationForm()
    
    return render(request, 'finance/loan_apply.html', {'form': form})

@login_required
def loan_detail(request, pk):
    loan = LoanApplication.objects.get(pk=pk)
    return render(request, 'finance/loan_detail.html', {'loan': loan})

@login_required
def calculate_credit_score(request):
    if request.user.user_type != 'MSME':
        return redirect('dashboard')
    
    profile = MSMEProfile.objects.get(user=request.user)
    
    # Simplified credit scoring logic
    score = 650  # Base score
    
    # Adjust based on business factors
    if profile.years_in_operation > 5:
        score += 50
    if profile.annual_turnover > 1000000:
        score += 30
        
    # Create or update credit score
    CreditScore.objects.update_or_create(
        msme=profile,
        defaults={
            'score': score,
            'factors': {
                'years_in_operation': profile.years_in_operation,
                'annual_turnover': float(profile.annual_turnover),
                'employee_count': profile.employee_count
            }
        }
    )
    
    messages.success(request, 'Credit score updated successfully!')
    return redirect('finance_dashboard')

# Marketplace Views
@login_required
def marketplace(request):
    products = ProductListing.objects.all().order_by('-created_at')[:20]
    procurement_requests = ProcurementRequest.objects.all().order_by('-created_at')[:20]
    
    return render(request, 'marketplace/browse.html', {
        'products': products,
        'procurement_requests': procurement_requests
    })

@login_required
def product_detail(request, pk):
    product = ProductListing.objects.get(pk=pk)
    return render(request, 'marketplace/product_detail.html', {'product': product})

@login_required
def procurement_detail(request, pk):
    procurement = ProcurementRequest.objects.get(pk=pk)
    bids = Bid.objects.filter(procurement_request=procurement)
    return render(request, 'marketplace/procurement_detail.html', {
        'procurement': procurement,
        'bids': bids
    })

@login_required
def submit_bid(request, pk):
    if request.user.user_type != 'MSME':
        return redirect('dashboard')
    
    procurement = ProcurementRequest.objects.get(pk=pk)
    profile = MSMEProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.procurement_request = procurement
            bid.msme = profile
            bid.save()
            messages.success(request, 'Bid submitted successfully!')
            return redirect('procurement_detail', pk=pk)
    else:
        form = BidForm()
    
    return render(request, 'marketplace/bid_submit.html', {
        'form': form,
        'procurement': procurement
    })

# Learning Hub Views
@login_required
def learning_hub(request):
    courses = LearningCourse.objects.all().order_by('-created_at')
    enrolled_courses = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
    
    return render(request, 'learning/courses.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses
    })

@login_required
def course_detail(request, pk):
    course = LearningCourse.objects.get(pk=pk)
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    return render(request, 'learning/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled
    })

@login_required
def enroll_course(request, pk):
    course = LearningCourse.objects.get(pk=pk)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    messages.success(request, f'Enrolled in {course.title} successfully!')
    return redirect('course_detail', pk=pk)

# Business Tools Views
@login_required
def business_tools(request):
    tools = BusinessTool.objects.all()
    subscribed_tools = []
    
    # Only try to get subscribed tools if user is MSME
    if request.user.user_type == 'MSME':
        try:
            profile = MSMEProfile.objects.get(user=request.user)
            subscribed_tools = MSMEToolSubscription.objects.filter(
                msme=profile,
                active=True
            ).values_list('tool_id', flat=True)
        except MSMEProfile.DoesNotExist:
            # If profile doesn't exist, just show tools without subscriptions
            pass
    
    return render(request, 'tools/tools.html', {
        'tools': tools,
        'subscribed_tools': subscribed_tools
    })

@login_required
def post_requirement(request):
    if request.user.user_type != 'BUYER':
        return redirect('dashboard')
    
    profile = BuyerProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProcurementRequestForm(request.POST)
        if form.is_valid():
            procurement = form.save(commit=False)
            procurement.buyer = profile
            procurement.save()
            messages.success(request, 'Procurement requirement posted successfully!')
            return redirect('marketplace')
    else:
        form = ProcurementRequestForm()
    
    return render(request, 'marketplace/requirement_post.html', {'form': form})

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    completed_courses = enrollments.filter(completed=True).count()
    in_progress_courses = enrollments.filter(completed=False).count()
    hours_learned = sum(e.course.duration_hours for e in enrollments.filter(completed=True))
    
    return render(request, 'learning/my_courses.html', {
        'enrollments': enrollments,
        'completed_courses': completed_courses,
        'in_progress_courses': in_progress_courses,
        'hours_learned': hours_learned
    })

@login_required
def inventory_management(request):
    if request.user.user_type != 'MSME':
        return redirect('dashboard')
    return render(request, 'tools/inventory.html')

@login_required
def crm_dashboard(request):
    if request.user.user_type != 'MSME':
        return redirect('dashboard')
    return render(request, 'tools/crm.html')

@login_required
def subscribe_tool(request, pk):
    if request.user.user_type != 'MSME':
        return redirect('dashboard')
    
    tool = BusinessTool.objects.get(pk=pk)
    profile = MSMEProfile.objects.get(user=request.user)
    
    MSMEToolSubscription.objects.get_or_create(msme=profile, tool=tool)
    messages.success(request, f'Subscribed to {tool.name} successfully!')
    return redirect('business_tools')

@login_required
def erp_dashboard(request):
    if request.user.user_type != 'MSME':
        return redirect('dashboard')
    return render(request, 'tools/erp_dashboard.html')

# core/views.py
@login_required
def invoice_list(request):
    if request.user.user_type != 'MSME':
        return redirect('dashboard')
    
    profile = MSMEProfile.objects.get(user=request.user)
    invoices = Invoice.objects.filter(msme=profile).order_by('-issue_date')
    buyers = BuyerProfile.objects.all()
    
    return render(request, 'finance/invoice_list.html', {
        'invoices': invoices,
        'buyers': buyers
    })

@login_required
def view_finance_options(request):
    lenders = LenderProfile.objects.all()
    return render(request, 'finance/options.html', {'lenders': lenders})

@login_required
def add_invoice(request):
    if request.user.user_type != 'MSME':
        return redirect('dashboard')
    
    profile = MSMEProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.msme = profile
            invoice.save()
            messages.success(request, 'Invoice added successfully!')
            return redirect('invoice_list')
    else:
        form = InvoiceForm()
    
    buyers = BuyerProfile.objects.all()
    return render(request, 'finance/invoice_list.html', {
        'form': form,
        'buyers': buyers
    })

@login_required
def request_invoice_discounting(request, invoice_id):
    if request.user.user_type != 'MSME':
        return redirect('dashboard')
    
    invoice = Invoice.objects.get(id=invoice_id)
    if request.method == 'POST':
        form = InvoiceDiscountingForm(request.POST)
        if form.is_valid():
            discount_request = form.save(commit=False)
            discount_request.invoice = invoice
            discount_request.msme = MSMEProfile.objects.get(user=request.user)
            discount_request.save()
            messages.success(request, 'Discount request submitted successfully!')
            return redirect('invoice_list')
    else:
        form = InvoiceDiscountingForm()
    
    return render(request, 'finance/invoice_discount.html', {
        'form': form,
        'invoice': invoice
    })
from .models import MSMEProfile, BuyerProfile, LenderProfile

def user_profile(request):
    context = {}
    if request.user.is_authenticated:
        try:
            if request.user.user_type == 'MSME':
                context['user_profile'] = MSMEProfile.objects.get(user=request.user)
            elif request.user.user_type == 'BUYER':
                context['user_profile'] = BuyerProfile.objects.get(user=request.user)
            elif request.user.user_type == 'LENDER':
                context['user_profile'] = LenderProfile.objects.get(user=request.user)
        except:
             context['user_profile'] = None
    return context
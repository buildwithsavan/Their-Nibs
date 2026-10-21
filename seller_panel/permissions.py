from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from admin_panel.models import Seller


def seller_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access the Seller Studio.")
            return redirect(f"/seller/login/?next={request.path}")
        
        is_admin = request.user.is_superuser or request.user.is_staff
        seller = Seller.objects.filter(user=request.user).first()
        if not seller and request.user.email:
            seller = Seller.objects.filter(email__iexact=request.user.email).first()
        
        if not (is_admin or seller):
            messages.error(request, "Seller account required. Please register as a seller first.")
            return redirect("/seller/register/step1/")

        if not is_admin and seller:
            if seller.status == 'pending':
                messages.warning(request, f"Your seller boutique '{seller.store_name}' is currently under review by administrator. You will be notified via email upon approval.")
                return redirect("/seller/login/")
            elif seller.status == 'suspended':
                messages.error(request, f"Your seller boutique '{seller.store_name}' has been temporarily disabled/suspended. Please contact administration.")
                return redirect("/seller/login/")
            elif seller.status == 'rejected':
                messages.error(request, f"Your seller application for '{seller.store_name}' was not approved.")
                return redirect("/seller/login/")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

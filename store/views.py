from decimal import Decimal
import json
import random
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from admin_panel.models import (
    Seller, AdminNotification, SellerNotification, Order, OrderItem,
    Product, ProductVariant, Coupon
)

def homepage(request):
    context = {
        'brand_name': 'Their Nibs',
        'announcements': [
            {'text': '£3.95 Standard delivery or Free delivery on all UK orders over £60', 'link': '#'},
            {'text': 'We Donate 20% of the Profits From our Kids Collection to our Chosen Charity!', 'link': '#'},
            {'text': 'Shop New In: Discover our Autumn Satin & Organic Cotton Loungewear', 'link': '#'},
        ],
        'nav_categories': [
            {
                'title': 'Halloween',
                'url': '#halloween',
            },
            {
                'title': 'Women',
                'url': '#women',
                'columns': [
                    ['Traditional Long Pyjamas', 'Oversized Pyjamas', 'Short Pyjamas', 'Capri Pyjamas', 'Boxy Pyjamas', 'Dressing Gowns & Robes'],
                    ['Nightdresses & Shirts', 'Satin Sleepwear', 'Cotton Pyjamas', 'Linen Blend', 'Jersey Loungewear']
                ]
            },
            {
                'title': 'Mens',
                'url': '#mens',
                'items': ['Mens Pyjamas', 'Matching Family Pyjamas']
            },
            {
                'title': 'Kids',
                'url': '#kids',
                'items': ['Kids Pyjamas', 'Tween Pyjamas & Nightwear', 'Matching Family Pyjamas', 'All Kids & Tweens']
            },
            {
                'title': 'Accessories',
                'url': '#accessories',
                'items': ['Make-up Bags', 'Eye Masks', 'Shower Caps', 'Scrunchies']
            },
            {
                'title': 'Gifting',
                'url': '#gifting',
                'items': ['Gifts For Her', 'Gifts For Him', 'Gifts For Kids', 'Matching Pyjamas', 'Gifts Under £100', 'Gifts Under £50', 'Gifts Under £25', 'Gifts under £15', 'E-Gift Card']
            },
        ],
        'hero_slides': [
            {
                'subtitle': 'Trick, Treat, Sleep, Repeat',
                'title': 'Sleepwear with star quality',
                'button_text': 'SHOP NOW',
                'button_link': '#new-in',
            },
            {
                'subtitle': 'Autumn Boutique Collection',
                'title': 'Elegance woven into every thread',
                'button_text': 'EXPLORE WOMENS',
                'button_link': '#womens',
            },
            {
                'subtitle': 'Matching Family Lounge Sets',
                'title': 'Unmatched comfort for cosy evenings',
                'button_text': 'DISCOVER MATCHING',
                'button_link': '#matching',
            }
        ],
        'featured_products': [
            {
                'name': 'Celestial Star & Moon Satin Pyjama Set',
                'category': 'Womens Sleepwear',
                'badge': 'BEST SELLER',
                'badge_type': 'best-seller',
                'rating': 5,
                'color': 'Navy Gold',
            },
            {
                'name': 'Midnight Wildflower Botanical Robe',
                'category': 'Loungewear & Robes',
                'badge': 'NEW',
                'badge_type': 'new',
                'rating': 5,
                'color': 'Emerald Floral',
            },
            {
                'name': 'Vintage Leopard Print Cotton Pyjama Set',
                'category': 'Womens Classic',
                'badge': 'POPULAR',
                'badge_type': 'popular',
                'rating': 4.9,
                'color': 'Warm Honey',
            },
            {
                'name': 'Heritage Stripe Brushed Cotton Mens Set',
                'category': 'Mens Loungewear',
                'badge': 'MATCHING SET',
                'badge_type': 'matching-set',
                'rating': 4.8,
                'color': 'Oxford Navy',
            },
        ],
        'categories_grid': [
            {
                'title': 'Womens Pyjamas',
                'description': 'Hand-drawn prints on whisper-soft fabrics',
                'link': '#womens',
            },
            {
                'title': 'Mens Sleepwear',
                'description': 'Tailored cuts, breathable comfort',
                'link': '#mens',
            },
            {
                'title': 'Kids Nightwear',
                'description': '20% of profits donated to children charity',
                'link': '#kids',
            },
            {
                'title': 'Luxury Gifting',
                'description': 'Curated gift boxes & monogrammed sets',
                'link': '#gifting',
            },
        ]
    }
    return render(request, 'homepage.html', context)


def seller_register_step1(request):
    if request.method == 'POST':
        session_data = request.session.get('seller_registration', {})
        pwd = request.POST.get('password')
        confirm_pwd = request.POST.get('confirm_password')
        if pwd and confirm_pwd and pwd != confirm_pwd:
            return render(request, 'seller_register_step1.html', {
                'step1_data': request.POST,
                'error': 'Passwords do not match. Please re-enter identical passwords.'
            })

        session_data['step1'] = {
            'full_name': request.POST.get('full_name'),
            'dob': request.POST.get('dob'),
            'gender': request.POST.get('gender'),
            'mobile': request.POST.get('mobile'),
            'mobile_verified': request.POST.get('mobile_verified') == 'true',
            'email': request.POST.get('email'),
            'email_verified': request.POST.get('email_verified') == 'true',
            'password': pwd,
            'present_address': request.POST.get('present_address'),
            'present_state': request.POST.get('present_state'),
            'present_district': request.POST.get('present_district'),
            'present_pincode': request.POST.get('present_pincode'),
            'same_as_present': request.POST.get('same_as_present') == 'on',
            'permanent_address': request.POST.get('permanent_address'),
            'permanent_state': request.POST.get('permanent_state'),
            'permanent_district': request.POST.get('permanent_district'),
            'permanent_pincode': request.POST.get('permanent_pincode'),
            'id_type': request.POST.get('id_type'),
            'id_number': request.POST.get('id_number'),
            'applicant_role': request.POST.get('applicant_role'),
        }
        request.session['seller_registration'] = session_data
        return redirect('seller_register_step2')

    saved_data = request.session.get('seller_registration', {}).get('step1', {})
    return render(request, 'seller_register_step1.html', {
        'step1_data': saved_data
    })


def seller_register_step2(request):
    if request.method == 'POST':
        session_data = request.session.get('seller_registration', {})
        session_data['step2'] = {
            'business_name': request.POST.get('business_name'),
            'business_type': request.POST.get('business_type'),
            'business_description': request.POST.get('business_description'),
            'year_started': request.POST.get('year_started'),
            'registration_number': request.POST.get('registration_number'),
            'business_address': request.POST.get('business_address'),
            'business_city': request.POST.get('business_city'),
            'business_state': request.POST.get('business_state'),
            'business_pincode': request.POST.get('business_pincode'),
            'different_pickup': request.POST.get('different_pickup'),
            'pickup_address': request.POST.get('pickup_address'),
            'pickup_city': request.POST.get('pickup_city'),
            'pickup_state': request.POST.get('pickup_state'),
            'pickup_pincode': request.POST.get('pickup_pincode'),
            'main_category': request.POST.get('main_category'),
            'product_subcategory': request.POST.get('product_subcategory'),
            'target_customers': request.POST.getlist('target_customers'),
            'product_source': request.POST.get('product_source'),
            'years_experience': request.POST.get('years_experience'),
            'selling_channels': request.POST.getlist('selling_channels'),
            'online_store_link': request.POST.get('online_store_link'),
            'pan_number': request.POST.get('pan_number'),
            'gst_registered': request.POST.get('gst_registered'),
            'gstin': request.POST.get('gstin'),
            'account_holder_name': request.POST.get('account_holder_name'),
            'bank_account_number': request.POST.get('bank_account_number'),
            'ifsc_code': request.POST.get('ifsc_code'),
        }
        request.session['seller_registration'] = session_data
        return redirect('seller_register_step3')

    saved_step2 = request.session.get('seller_registration', {}).get('step2', {})
    saved_step1 = request.session.get('seller_registration', {}).get('step1', {})
    return render(request, 'seller_register_step2.html', {
        'step1_data': saved_step1,
        'step2_data': saved_step2
    })


def seller_register_step3(request):
    session_data = request.session.get('seller_registration', {})
    saved_step1 = session_data.get('step1', {})
    saved_step2 = session_data.get('step2', {})

    if request.method == 'POST':
        app_ref = f"CLF-SELL-2026-{random.randint(10000, 99999)}"
        session_data['step3'] = {
          'submitted': True,
          'app_ref': app_ref,
        }
        request.session['seller_registration'] = session_data

        seller_email = saved_step1.get('email') or f"seller_{random.randint(100, 999)}@theirnibs.com"
        raw_password = saved_step1.get('password') or 'Seller123!'
        full_name = saved_step1.get('full_name', '')
        name_parts = full_name.split(' ') if full_name else ['Seller']
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        seller_user = User.objects.filter(Q(email__iexact=seller_email) | Q(username__iexact=seller_email)).first()
        if not seller_user:
            seller_user = User.objects.create_user(
                username=seller_email,
                email=seller_email,
                password=raw_password,
                first_name=first_name,
                last_name=last_name,
                is_staff=False
            )
        else:
            seller_user.set_password(raw_password)
            seller_user.save()

        store_name = saved_step2.get('business_name') or f"Store_{random.randint(1000, 9999)}"
        
        full_reg_data = {
            'step1': saved_step1,
            'step2': saved_step2,
            'app_ref': app_ref,
            'submitted_at': timezone.now().isoformat()
        }

        target_cust = saved_step2.get('target_customers', [])
        target_cust_str = ', '.join(target_cust) if isinstance(target_cust, list) else str(target_cust or '')
        selling_ch = saved_step2.get('selling_channels', [])
        selling_ch_str = ', '.join(selling_ch) if isinstance(selling_ch, list) else str(selling_ch or '')

        seller_defaults = {
            'store_name': store_name,
            'company_name': saved_step2.get('business_name') or store_name,
            'email': seller_email,
            'phone': saved_step1.get('mobile') or '0000000000',
            'status': 'pending',
            'gst_number': saved_step2.get('gstin') or '',
            'pan_number': saved_step2.get('pan_number') or '',
            'bank_name': saved_step2.get('account_holder_name') or '',
            'account_holder_name': saved_step2.get('account_holder_name') or '',
            'account_number': saved_step2.get('bank_account_number') or '',
            'ifsc_code': saved_step2.get('ifsc_code') or '',
            'city': saved_step2.get('business_city') or saved_step1.get('present_district') or '',
            'state': saved_step2.get('business_state') or saved_step1.get('present_state') or '',
            'pickup_address': saved_step2.get('pickup_address') or saved_step2.get('business_address') or saved_step1.get('present_address') or '',
            'pickup_pincode': saved_step2.get('pickup_pincode') or saved_step2.get('business_pincode') or saved_step1.get('present_pincode') or '',
            'business_type': saved_step2.get('business_type') or '',
            'business_reg_no': saved_step2.get('registration_number') or '',
            'main_category': saved_step2.get('main_category') or '',
            'product_subcategory': saved_step2.get('product_subcategory') or '',
            'target_customers': target_cust_str,
            'product_source': saved_step2.get('product_source') or '',
            'years_experience': saved_step2.get('years_experience') or '',
            'selling_channels': selling_ch_str,
            'online_store_link': saved_step2.get('online_store_link') or '',
            'store_description': saved_step2.get('business_description') or '',
            'registration_data': full_reg_data,
        }

        seller_obj, created = Seller.objects.get_or_create(
            user=seller_user,
            defaults=seller_defaults
        )
        if not created:
            for k, v in seller_defaults.items():
                if k == 'status' and seller_obj.status == 'approved':
                    continue
                setattr(seller_obj, k, v)
            if seller_obj.status != 'approved':
                seller_obj.status = 'pending'
            seller_obj.registration_data = full_reg_data
            seller_obj.save()

        AdminNotification.objects.create(
            title="New Seller Application Received",
            message=f"Store '{store_name}' ({full_name}) submitted a seller registration application ({app_ref}). Awaiting admin review and approval.",
            notification_type="new_seller",
            link="/admin-panel/sellers/"
        )

        SellerNotification.objects.create(
            seller=seller_obj,
            title="Application Submitted – Under Review",
            message=f"Your merchant boutique '{store_name}' registration ({app_ref}) has been submitted. Our atelier team will review your application and send an approval email upon verification.",
            notification_type="application_status",
            link="/seller-panel/settings/profile/"
        )

        return render(request, 'seller_register_step3.html', {
            'application_submitted': True,
            'app_ref': app_ref,
            'step1_data': saved_step1,
            'step2_data': saved_step2
        })

    return render(request, 'seller_register_step3.html', {
        'application_submitted': session_data.get('step3', {}).get('submitted', False),
        'app_ref': session_data.get('step3', {}).get('app_ref', ''),
        'step1_data': saved_step1,
        'step2_data': saved_step2
    })


def customer_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        login_type = request.POST.get('login_type', 'customer')

        matched_user = None
        seller_obj = None

        seller_obj = Seller.objects.filter(Q(store_name__iexact=identifier) | Q(email__iexact=identifier)).first()
        if seller_obj and seller_obj.user:
            matched_user = seller_obj.user

        if not matched_user and '@' in identifier:
            matched_user = User.objects.filter(email__iexact=identifier).first()

        if not matched_user:
            matched_user = User.objects.filter(username__iexact=identifier).first()

        user = None
        if matched_user:
            user = authenticate(request, username=matched_user.username, password=password)
            
            if not user:
                is_seller_acct = Seller.objects.filter(Q(user=matched_user) | Q(email__iexact=matched_user.email)).exists()
                if is_seller_acct and password and not matched_user.has_usable_password():
                    matched_user.set_password(password)
                    matched_user.save()
                    user = authenticate(request, username=matched_user.username, password=password)

        if not user:
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)
            request.session['customer_logged_in'] = True
            request.session['customer_email'] = user.email or user.username
            request.session['customer_name'] = user.get_full_name() or user.username

            is_admin = user.is_superuser or user.is_staff or (
                hasattr(user, 'profile') and getattr(user.profile, 'role', '') != 'customer'
            )
            is_seller = Seller.objects.filter(Q(user=user) | Q(email__iexact=user.email), status='approved').exists()

            next_url = request.POST.get('next') or request.GET.get('next')

            if next_url and next_url.startswith('/'):
                if next_url.startswith('/seller-panel/') and (is_seller or is_admin):
                    return redirect(next_url)
                elif next_url.startswith('/admin-panel/') and is_admin:
                    return redirect(next_url)
                elif not next_url.startswith('/admin-panel/') and not next_url.startswith('/seller-panel/'):
                    return redirect(next_url)

            if is_admin:
                return redirect('admin_panel:dashboard')
            elif is_seller:
                return redirect('seller_panel:dashboard')
            else:
                return redirect('homepage')
        else:
            user_exists = User.objects.filter(Q(username__iexact=identifier) | Q(email__iexact=identifier)).exists() or Seller.objects.filter(Q(store_name__iexact=identifier) | Q(email__iexact=identifier)).exists()
            if user_exists or identifier.lower() in ['admin', 'admin@theirnibs.com']:
                messages.error(request, "Invalid username/email or password.")
                next_url = request.POST.get('next') or request.GET.get('next') or ''
                return render(request, 'customer_login.html', {'next': next_url})

            request.session['customer_logged_in'] = True
            request.session['customer_email'] = identifier
            request.session['customer_name'] = identifier.split('@')[0].capitalize() if '@' in identifier else identifier
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('homepage')

    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_panel:dashboard')
        elif Seller.objects.filter(Q(user=request.user) | Q(email__iexact=request.user.email), status='approved').exists():
            return redirect('seller_panel:dashboard')

    if request.session.get('customer_logged_in', False):
        next_url = request.GET.get('next')
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect('homepage')

    next_url = request.GET.get('next') or request.POST.get('next') or ''
    return render(request, 'customer_login.html', {'next': next_url})


def customer_logout(request):
    was_admin = False
    was_seller = False
    if request.user.is_authenticated:
        was_admin = request.user.is_staff or request.user.is_superuser
        was_seller = Seller.objects.filter(Q(user=request.user) | Q(email__iexact=request.user.email), status='approved').exists()
        logout(request)
    request.session.flush()
    messages.info(request, "You have been logged out successfully.")
    if was_admin:
        return redirect('admin_panel:login')
    elif was_seller:
        return redirect('seller_login')
    return redirect('customer_login')


def seller_login_view(request):
    if request.user.is_authenticated:
        seller_obj = Seller.objects.filter(Q(user=request.user) | Q(email__iexact=request.user.email)).first()
        is_admin = request.user.is_staff or request.user.is_superuser
        if is_admin:
            next_url = request.GET.get('next') or '/seller-panel/dashboard/'
            return redirect(next_url)
        elif seller_obj:
            if seller_obj.status == 'approved':
                next_url = request.GET.get('next') or '/seller-panel/dashboard/'
                return redirect(next_url)
            elif seller_obj.status == 'pending':
                messages.warning(request, f"Your seller application for '{seller_obj.store_name}' is currently under review by our administration. You will receive an approval email at {seller_obj.email} once approved.")
            elif seller_obj.status == 'suspended':
                messages.error(request, f"Your seller boutique '{seller_obj.store_name}' has been temporarily disabled/suspended. Please contact administration.")
            elif seller_obj.status == 'rejected':
                messages.error(request, f"Your seller application for '{seller_obj.store_name}' was not approved.")

    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip() or request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')

        matched_user = None
        seller_obj = Seller.objects.filter(Q(store_name__iexact=identifier) | Q(email__iexact=identifier)).first()
        if seller_obj and seller_obj.user:
            matched_user = seller_obj.user

        if not matched_user and '@' in identifier:
            matched_user = User.objects.filter(email__iexact=identifier).first()

        if not matched_user:
            matched_user = User.objects.filter(username__iexact=identifier).first()

        user = None
        if matched_user:
            user = authenticate(request, username=matched_user.username, password=password)
            if not user:
                is_seller_acct = Seller.objects.filter(Q(user=matched_user) | Q(email__iexact=matched_user.email)).exists()
                if is_seller_acct and password and not matched_user.has_usable_password():
                    matched_user.set_password(password)
                    matched_user.save()
                    user = authenticate(request, username=matched_user.username, password=password)

        if not user:
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            if not seller_obj:
                seller_obj = Seller.objects.filter(Q(user=user) | Q(email__iexact=user.email)).first()
            is_admin = user.is_staff or user.is_superuser

            if is_admin:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                next_url = request.POST.get('next') or request.GET.get('next') or '/seller-panel/dashboard/'
                return redirect(next_url)

            if not seller_obj:
                messages.error(request, "Seller account required. Please register as a seller first.")
                next_url = request.POST.get('next') or request.GET.get('next') or '/seller-panel/dashboard/'
                return render(request, 'seller_login.html', {'next': next_url})

            if seller_obj.status == 'pending':
                messages.warning(
                    request,
                    f"Your seller application for '{seller_obj.store_name}' is currently under review by our administration. Once approved, you will receive an approval email at {seller_obj.email}."
                )
                return render(request, 'seller_login.html', {'next': request.POST.get('next') or '/seller-panel/dashboard/'})

            if seller_obj.status == 'suspended':
                messages.error(
                    request,
                    f"Your seller boutique '{seller_obj.store_name}' has been temporarily disabled/suspended by administration. Please contact customer care for support."
                )
                return render(request, 'seller_login.html', {'next': request.POST.get('next') or '/seller-panel/dashboard/'})

            if seller_obj.status == 'rejected':
                messages.error(
                    request,
                    f"Your seller application for '{seller_obj.store_name}' was not approved. Please contact support."
                )
                return render(request, 'seller_login.html', {'next': request.POST.get('next') or '/seller-panel/dashboard/'})

            if seller_obj.status == 'approved':
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                next_url = request.POST.get('next') or request.GET.get('next') or '/seller-panel/dashboard/'
                return redirect(next_url)
        else:
            messages.error(request, "Invalid seller email/store name or password.")
            next_url = request.POST.get('next') or request.GET.get('next') or '/seller-panel/dashboard/'
            return render(request, 'seller_login.html', {'next': next_url})

    next_url = request.GET.get('next') or request.POST.get('next') or '/seller-panel/dashboard/'
    return render(request, 'seller_login.html', {'next': next_url})


def seller_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    request.session.flush()
    messages.info(request, "You have been logged out successfully.")
    return redirect('seller_login')


def customer_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password') or 'Customer123!'
        mobile = request.POST.get('mobile', '')
        dob = request.POST.get('dob', '')
        address_line1 = request.POST.get('address_line1', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        pincode = request.POST.get('pincode', '')
        country = request.POST.get('country', '')
        newsletter = request.POST.get('newsletter') == 'on'
        sms_alerts = request.POST.get('sms_alerts') == 'on'
        
        user_display_name = f"{first_name} {last_name}".strip() or email.split('@')[0].capitalize()

        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'is_active': True,
            }
        )
        if created:
            user.set_password(password)
            user.save()

        login(request, user)

        request.session['customer_logged_in'] = True
        request.session['customer_email'] = email
        request.session['customer_name'] = user_display_name
        request.session['customer_account'] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'mobile': mobile,
            'dob': dob,
            'address_line1': address_line1,
            'city': city,
            'state': state,
            'pincode': pincode,
            'country': country,
            'newsletter': newsletter,
            'sms_alerts': sms_alerts,
            'created': True
        }
        
        return render(request, 'customer_register.html', {
            'account_created': True,
            'user_name': user_display_name,
            'user_email': email
        })

    return render(request, 'customer_register.html')


def get_customer_info(request):
    email = request.session.get('customer_email')
    name = request.session.get('customer_name')
    mobile = ''
    addresses = request.session.get('customer_addresses', [])
    
    if hasattr(request, 'user') and request.user.is_authenticated:
        if not email:
            email = request.user.email or request.user.username
        if not name:
            name = request.user.get_full_name() or request.user.username

    acct = request.session.get('customer_account', {})
    if not mobile and acct.get('mobile'):
        mobile = acct.get('mobile')
    if not addresses and acct.get('address_line1'):
        addresses = [{
            'full_name': name or f"{acct.get('first_name', '')} {acct.get('last_name', '')}".strip(),
            'address_line1': acct.get('address_line1'),
            'city': acct.get('city', ''),
            'pincode': acct.get('pincode', ''),
            'country': acct.get('country', 'United Kingdom')
        }]
        request.session['customer_addresses'] = addresses
        
    return {
        'customer_email': email or 'user@theirnibs.com',
        'customer_name': name or (email.split('@')[0].capitalize() if email and '@' in email else 'Customer'),
        'customer_mobile': mobile,
        'customer_addresses': addresses
    }


def customer_orders(request):
    if not request.session.get('customer_logged_in', False) and not request.user.is_authenticated:
        return redirect('/account/login/?next=/account/orders/')

    info = get_customer_info(request)
    user_orders = []
    try:
        if request.user.is_authenticated:
            user_orders = Order.objects.filter(customer=request.user).order_by('-created_at')[:10]
    except Exception:
        pass

    context = {
        **info,
        'active_tab': 'orders',
        'user_orders': user_orders,
    }
    return render(request, 'customer_account.html', context)


def customer_profile(request):
    if not request.session.get('customer_logged_in', False) and not request.user.is_authenticated:
        return redirect('/account/login/?next=/account/profile/')

    info = get_customer_info(request)
    context = {
        **info,
        'active_tab': 'profile',
    }
    return render(request, 'customer_account.html', context)


def customer_wishlist(request):
    info = get_customer_info(request)
    context = {
        **info,
        'active_tab': 'wishlist',
    }
    return render(request, 'customer_account.html', context)


def customer_profile_update(request):
    if not request.session.get('customer_logged_in', False) and not request.user.is_authenticated:
        return redirect('customer_login')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()

        if email:
            request.session['customer_email'] = email
        if full_name:
            request.session['customer_name'] = full_name

        acct = request.session.get('customer_account', {})
        acct['email'] = email
        acct['full_name'] = full_name
        acct['mobile'] = mobile
        request.session['customer_account'] = acct

        if request.user.is_authenticated:
            if email:
                request.user.email = email
            if full_name:
                parts = full_name.split(' ', 1)
                request.user.first_name = parts[0]
                request.user.last_name = parts[1] if len(parts) > 1 else ''
            request.user.save()

        messages.success(request, "Your contact information has been updated successfully.")

    return redirect('customer_profile')


def customer_address_add(request):
    if not request.session.get('customer_logged_in', False) and not request.user.is_authenticated:
        return redirect('customer_login')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        address_line1 = request.POST.get('address_line1', '').strip()
        city = request.POST.get('city', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        country = request.POST.get('country', 'India').strip()

        addresses = request.session.get('customer_addresses', [])
        new_addr = {
            'full_name': full_name,
            'address_line1': address_line1,
            'city': city,
            'pincode': pincode,
            'country': country
        }
        addresses.append(new_addr)
        request.session['customer_addresses'] = addresses

        acct = request.session.get('customer_account', {})
        acct['addresses'] = addresses
        request.session['customer_account'] = acct

        messages.success(request, "Your address has been added successfully.")

    return redirect('customer_profile')


def checkout_view(request):
    
    is_customer_logged_in = request.user.is_authenticated or request.session.get('customer_logged_in', False) or request.session.get('customer_id')
    if not is_customer_logged_in:
        messages.info(request, "Please log in to your account to complete checkout.")
        return redirect('/customer/login/?next=/checkout/')

    customer_email = request.session.get('customer_email', '')
    customer_name = request.session.get('customer_name', '')
    first_name = ''
    last_name = ''
    if customer_name:
        parts = customer_name.split(' ', 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''
    elif request.user.is_authenticated:
        customer_email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name

    context = {
        'brand_name': 'Their Nibs',
        'customer_email': customer_email,
        'first_name': first_name,
        'last_name': last_name,
    }
    return render(request, 'checkout.html', context)


def place_order_view(request):
    is_customer_logged_in = request.user.is_authenticated or request.session.get('customer_logged_in', False) or request.session.get('customer_id')
    if not is_customer_logged_in:
        messages.info(request, "Please log in to your account to place an order.")
        return redirect('/customer/login/?next=/checkout/')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        full_name = f"{first_name} {last_name}".strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        postcode = request.POST.get('postcode', '').strip()
        country = request.POST.get('country', 'India').strip()
        payment_method_raw = request.POST.get('payment_method', 'Credit / Debit Card')
        shipping_method = request.POST.get('shipping_method', 'Express Courier Tracked')

        is_cod = 'cash' in payment_method_raw.lower() or 'cod' in payment_method_raw.lower()

        cart_data_str = request.POST.get('cart_data', '') or request.POST.get('cart_items_json', '')
        cart_items = []
        if cart_data_str:
            try:
                cart_items = json.loads(cart_data_str)
            except Exception:
                pass

        if not cart_items:
            session_cart = request.session.get('cart', [])
            for item in session_cart:
                p_id = item.get('product_id')
                p = Product.objects.filter(pk=p_id).first()
                if p:
                    qty = int(item.get('quantity', 1))
                    cart_items.append({
                        'product': p,
                        'product_id': p.id,
                        'name': p.name,
                        'sku': p.sku,
                        'price': p.price or Decimal('1499.00'),
                        'quantity': qty,
                        'size': item.get('size', 'M'),
                    })
        else:
            hydrated = []
            for itm in cart_items:
                p_id = itm.get('product_id') or itm.get('id')
                p = Product.objects.filter(pk=p_id).first() if p_id else None
                title = itm.get('title') or itm.get('name')
                if not p and title:
                    p = Product.objects.filter(name__icontains=title.split()[0]).first()
                if not p:
                    p = Product.objects.filter(status='active').first()
                if p:
                    qty = int(itm.get('quantity') or itm.get('qty') or 1)
                    raw_price = itm.get('price')
                    price_val = Decimal(str(raw_price)) if raw_price is not None else (p.price or Decimal('1499.00'))
                    var_str = str(itm.get('variant', ''))
                    size_val = itm.get('size') or (var_str.split('/')[-1].strip() if '/' in var_str else ('M' if not var_str else var_str))
                    hydrated.append({
                        'product': p,
                        'product_id': p.id,
                        'name': title or p.name,
                        'sku': itm.get('sku', p.sku),
                        'price': price_val,
                        'quantity': qty,
                        'size': size_val,
                    })
            cart_items = hydrated

        if not cart_items:
            fallback_prod = Product.objects.filter(status='active').first()
            if fallback_prod:
                cart_items.append({
                    'product': fallback_prod,
                    'product_id': fallback_prod.id,
                    'name': fallback_prod.name,
                    'sku': fallback_prod.sku,
                    'price': fallback_prod.price or Decimal('1499.00'),
                    'quantity': 1,
                    'size': 'M',
                })

        subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
        shipping = Decimal('0.00') if subtotal >= Decimal('999.00') else Decimal('99.00')

        coupon_code = (request.POST.get('coupon_code') or '').strip().upper()
        if not coupon_code and 'applied_coupon' in request.session:
            coupon_code = request.session['applied_coupon'].get('code', '')

        discount_amount = Decimal('0.00')
        if coupon_code:
            coupon = Coupon.objects.filter(code__iexact=coupon_code).first()
            if coupon and coupon.is_valid and subtotal >= coupon.min_order_amount:
                if coupon.discount_type == 'percentage':
                    discount_amount = (subtotal * (coupon.discount_value / Decimal('100'))).quantize(Decimal('0.01'))
                    if coupon.max_discount and discount_amount > coupon.max_discount:
                        discount_amount = coupon.max_discount
                else:
                    discount_amount = min(coupon.discount_value, subtotal).quantize(Decimal('0.01'))

                coupon.used_count += 1
                coupon.save(update_fields=['used_count'])
            else:
                coupon_code = ''

        total = max(Decimal('0.00'), subtotal - discount_amount + shipping)

        request.session.pop('applied_coupon', None)
        request.session.modified = True

        order_num = f"TN-{random.randint(100000, 999999)}"

        customer_user = request.user if request.user.is_authenticated else None
        if not customer_user:
            cust_email = email or f"customer_{random.randint(1000, 9999)}@theirnibs.com"
            customer_user = User.objects.filter(Q(email__iexact=cust_email) | Q(username__iexact=cust_email)).first()
            if not customer_user:
                customer_user = User.objects.create_user(
                    username=cust_email,
                    email=cust_email,
                    first_name=first_name or 'Valued',
                    last_name=last_name or 'Customer'
                )

        order = Order.objects.create(
            order_number=order_num,
            user=customer_user,
            shipping_name=full_name or 'Valued Customer',
            shipping_phone=phone or '0000000000',
            shipping_address=address or '14 Kensington High Street',
            shipping_city=city or 'Mumbai',
            shipping_state=country or 'Maharashtra',
            shipping_pincode=postcode or '400001',
            payment_method='cod' if is_cod else 'credit_card',
            payment_status='pending',
            cod_status='pending' if is_cod else 'none',
            status='pending',
            subtotal=subtotal,
            discount_amount=discount_amount,
            coupon_code=coupon_code,
            shipping_charge=shipping,
            total_amount=total,
            notes=f"Shipping Method: {shipping_method}"
        )

        for item in cart_items:
            prod = item.get('product')
            if not prod:
                prod = Product.objects.filter(status='active').first()
            if prod:
                itm_price = item.get('price') or prod.price or Decimal('1499.00')
                itm_qty = item.get('quantity', 1)
                OrderItem.objects.create(
                    order=order,
                    product=prod,
                    product_name=item.get('name') or prod.name,
                    sku=item.get('sku') or prod.sku,
                    size=item.get('size', 'M'),
                    price=itm_price,
                    quantity=itm_qty,
                    total_price=itm_price * itm_qty,
                )

        try:
            from admin_panel.models import OrderTimeline
            OrderTimeline.objects.create(
                order=order,
                status='pending',
                notes="Order placed with Cash on Delivery. Awaiting admin approval." if is_cod else "Order placed successfully."
            )
        except Exception:
            pass

        if is_cod:
            AdminNotification.objects.create(
                title="New CoD Approval Request",
                message=f"Order #{order.order_number} (₹{order.total_amount}) by {order.shipping_name} requires Cash on Delivery verification & approval.",
                notification_type="order",
                link="/admin-panel/cod-requests/"
            )

        try:
            from .invoice_generator import generate_invoice_pdf, save_invoice_pdf
            from datetime import datetime
            order_info = {
                'order_id': order.order_number,
                'full_name': order.shipping_name,
                'email': customer_user.email if customer_user else email,
                'phone': order.shipping_phone,
                'address': order.shipping_address,
                'city': order.shipping_city,
                'postcode': order.shipping_pincode,
                'country': order.shipping_state or 'India',
                'payment_method': 'Cash on Delivery (Pay on Arrival)' if is_cod else 'Razorpay (Online Verified)',
                'payment_id': request.POST.get('payment_id', order.order_number),
                'total': str(order.total_amount),
                'created_at': datetime.now().strftime('%d %B %Y, %I:%M %p'),
                'email_sent': False,
                'pdf_generated': False,
            }
            pdf_items = [{
                'title': itm['name'],
                'variant': f"{itm['name']} / {itm['size']}",
                'price': str(itm['price']),
                'qty': itm['quantity'],
            } for itm in cart_items]
            generate_invoice_pdf(order_info, pdf_items)
            save_invoice_pdf(order_info, pdf_items)
        except Exception:
            pass

        if 'cart' in request.session:
            del request.session['cart']
            request.session.modified = True

        return redirect('order_success_with_id', order_number=order.order_number)

    return redirect('checkout')


def order_success_view(request, order_number=None):
    if not order_number:
        session_order = request.session.get('latest_order')
        if session_order and session_order.get('order_id'):
            order_number = session_order.get('order_id')
        else:
            latest_db_order = Order.objects.order_by('-created_at').first()
            if latest_db_order:
                order_number = latest_db_order.order_number

    order = Order.objects.filter(order_number=order_number).prefetch_related('items__product').first() if order_number else None
    if not order:
        session_order = request.session.get('latest_order')
        if session_order:
            order_dict = session_order
            items = request.session.get('latest_order_items', [])
            return render(request, 'order_success.html', {
                'order': order_dict,
                'items': items,
                'is_cod_pending': False,
            })
        return redirect('homepage')

    is_cod_pending = (order.cod_status == 'pending')

    order_dict = {
        'order_id': order.order_number,
        'full_name': order.shipping_name,
        'email': order.email,
        'phone': order.shipping_phone,
        'address': order.shipping_address,
        'city': order.shipping_city,
        'postcode': order.shipping_pincode,
        'country': order.shipping_state or 'India',
        'payment_method': 'Cash on Delivery (Pay on Arrival)' if order.cod_status != 'none' else 'Razorpay (Online Verified)',
        'subtotal': order.subtotal,
        'shipping': order.shipping_charge,
        'total': order.total_amount,
        'is_cod': order.cod_status != 'none',
        'cod_status': order.cod_status,
        'items': order.items.all(),
        'email_sent': True,
        'pdf_generated': True,
        'created_at': order.created_at.strftime('%d %B %Y, %I:%M %p') if order.created_at else '',
    }

    items_list = []
    for itm in order.items.all():
        items_list.append({
            'title': itm.product_name,
            'variant': f"{itm.product_name} / {itm.size}",
            'price': str(itm.price),
            'qty': itm.quantity,
        })

    context = {
        'order': order_dict,
        'items': items_list if items_list else order.items.all(),
        'is_cod_pending': is_cod_pending,
    }
    return render(request, 'order_success.html', context)


def download_invoice_view(request, order_id):
    
    invoices_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
    pdf_filename = f"TheirNibs_Invoice_{order_id}.pdf"
    pdf_path = os.path.join(invoices_dir, pdf_filename)

    pdf_bytes = None
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
    else:
        order = Order.objects.filter(order_number=order_id).prefetch_related('items').first()
        try:
            from .invoice_generator import generate_invoice_pdf, save_invoice_pdf
            from datetime import datetime
            order_info = {
                'order_id': order.order_number if order else order_id,
                'full_name': order.shipping_name if order else 'Valued Customer',
                'email': order.email if order else 'customer@boutique.co.uk',
                'phone': order.shipping_phone if order else '',
                'address': order.shipping_address if order else '',
                'city': order.shipping_city if order else '',
                'postcode': order.shipping_pincode if order else '',
                'country': order.shipping_country if order else 'India',
                'payment_method': 'Cash on Delivery (COD)' if (order and order.cod_status != 'none') else 'Razorpay / Prepaid',
                'payment_id': order_id,
                'total': str(order.total_amount) if order else '40.00',
                'created_at': order.created_at.strftime('%d %B %Y, %I:%M %p') if (order and order.created_at) else datetime.now().strftime('%d %B %Y, %I:%M %p'),
            }
            items = []
            if order:
                for itm in order.items.all():
                    items.append({
                        'title': itm.product_name,
                        'variant': f"{itm.product_name} / {itm.size}",
                        'price': str(itm.price),
                        'qty': itm.quantity,
                    })
            pdf_bytes = generate_invoice_pdf(order_info, items)
            save_invoice_pdf(order_info, items)
        except Exception:
            pdf_bytes = None

    if pdf_bytes:
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
        return response
    raise Http404("Invoice not found")


def track_order_view(request, order_number=None):

    if not order_number:
        session_order = request.session.get('latest_order')
        if session_order and session_order.get('order_id'):
            order_number = session_order.get('order_id')
        else:
            latest_db_order = Order.objects.order_by('-created_at').first()
            if latest_db_order:
                order_number = latest_db_order.order_number
            else:
                order_number = 'TN-492025'

    order = Order.objects.filter(order_number=order_number).prefetch_related('items__product').first() if order_number else None

    if order:
        order_dict = {
            'order_id': order.order_number,
            'full_name': order.shipping_name or 'Valued Customer',
            'email': order.email or 'customer@boutique.co.uk',
            'phone': order.shipping_phone or '+91 85115 30779',
            'address': order.shipping_address or '14 Kensington High Street, Suite 4B',
            'city': order.shipping_city or 'Mumbai',
            'postcode': order.shipping_pincode or '400050',
            'state': order.shipping_state or 'Maharashtra',
            'payment_method': 'Cash on Delivery (Pay on Arrival)' if order.cod_status != 'none' else 'Razorpay (Online Verified)',
            'subtotal': order.subtotal,
            'shipping': order.shipping_charge,
            'total': order.total_amount,
            'items': order.items.all(),
            'courier': 'BlueDart Express',
            'awb': 'BD-98234105',
            'created_at': order.created_at.strftime('%d %B %Y, %I:%M %p') if order.created_at else '17 October 2026, 04:09 AM',
            'est_delivery': '21 October 2026',
        }
    else:
        session_order = request.session.get('latest_order', {})
        items = request.session.get('latest_order_items', [])
        order_dict = {
            'order_id': order_number or session_order.get('order_id', 'TN-492025'),
            'full_name': session_order.get('full_name', 'Eleanor Vance'),
            'email': session_order.get('email', 'customer@boutique.co.uk'),
            'phone': session_order.get('phone', '+91 85115 30779'),
            'address': session_order.get('address', '14 Kensington High Street, Suite 4B'),
            'city': session_order.get('city', 'Mumbai'),
            'postcode': session_order.get('postcode', '400050'),
            'state': session_order.get('country', 'Maharashtra'),
            'payment_method': session_order.get('payment_method', 'Razorpay (Online Verified)'),
            'subtotal': session_order.get('subtotal', '1,899.00'),
            'shipping': session_order.get('shipping', '0.00'),
            'total': session_order.get('total', '1,899.00'),
            'items': items,
            'courier': 'BlueDart Express',
            'awb': 'BD-98234105',
            'created_at': session_order.get('created_at', '17 October 2026, 04:09 AM'),
            'est_delivery': '21 October 2026',
        }

    return render(request, 'track_order.html', {'order': order_dict})


def about_us_view(request):
    return render(request, 'pages/about_us.html')


def size_guides_view(request):
    return render(request, 'pages/size_guides.html')


def contact_us_view(request):
    form_submitted = False
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        order_number = request.POST.get('order_number', '').strip()
        topic = request.POST.get('topic', '').strip()
        message_text = request.POST.get('message', '').strip()
        if name and email and message_text:
            form_submitted = True
            admin_recipient = getattr(settings, 'ADMIN_EMAIL', getattr(settings, 'DEFAULT_FROM_EMAIL', 'customercare@theirnibs.com'))
            subject = f"[Their Nibs] Customer Inquiry: {topic or 'General'} - {name}"
            body = (
                f"New customer message submitted via Their Nibs Contact Us page:\n\n"
                f"Customer Name: {name}\n"
                f"Customer Email: {email}\n"
                f"Order Number: {order_number or 'Not provided'}\n"
                f"Topic: {topic or 'General'}\n\n"
                f"Message:\n"
                f"{message_text}\n\n"
                f"----------------------------------------\n"
                f"Their Nibs Customer Care Host Dispatch"
            )
            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'customercare@theirnibs.com'),
                    recipient_list=[admin_recipient],
                    fail_silently=False,
                )
            except Exception:
                pass
            messages.success(request, "Thank you for reaching out! Your message has been received and our London team will get back to you shortly.")
    return render(request, 'pages/contact_us.html', {'form_submitted': form_submitted})


def stores_view(request):
    return render(request, 'pages/stores.html')


def here_to_help_view(request):
    return render(request, 'pages/here_to_help.html')


def delivery_returns_view(request):
    return render(request, 'pages/delivery_returns.html')


def refund_policy_view(request):
    return render(request, 'pages/refund_policy.html')


def terms_conditions_view(request):
    return render(request, 'pages/terms_conditions.html')


def terms_of_service_view(request):
    return render(request, 'pages/terms_of_service.html')


def privacy_policy_view(request):
    return render(request, 'pages/privacy_policy.html')


def behind_the_seams_view(request):
    return render(request, 'pages/behind_the_seams.html')


def cms_page_view(request, page_slug):
    slug = (page_slug or '').strip().lower()
    mapping = {
        'about-us': 'pages/about_us.html',
        'about': 'pages/about_us.html',
        'size-guides': 'pages/size_guides.html',
        'size-guide': 'pages/size_guides.html',
        'contact-us': 'pages/contact_us.html',
        'contact': 'pages/contact_us.html',
        'their-nibs-stores': 'pages/stores.html',
        'stores': 'pages/stores.html',
        'our-stores': 'pages/stores.html',
        'here-to-help': 'pages/here_to_help.html',
        'help': 'pages/here_to_help.html',
        'delivery-returns': 'pages/delivery_returns.html',
        'delivery': 'pages/delivery_returns.html',
        'shipping': 'pages/delivery_returns.html',
        'refund-policy': 'pages/refund_policy.html',
        'refunds': 'pages/refund_policy.html',
        'returns': 'pages/refund_policy.html',
        'terms-and-conditions': 'pages/terms_conditions.html',
        'terms-conditions': 'pages/terms_conditions.html',
        'terms': 'pages/terms_conditions.html',
        'terms-of-service': 'pages/terms_of_service.html',
        'terms-of-use': 'pages/terms_of_service.html',
        'privacy-policy': 'pages/privacy_policy.html',
        'privacy': 'pages/privacy_policy.html',
        'behind-the-seams': 'pages/behind_the_seams.html',
        'blog': 'pages/behind_the_seams.html',
    }
    template_name = mapping.get(slug, 'pages/here_to_help.html')
    return render(request, template_name)


def api_available_coupons(request):
    
    today = timezone.now().date()
    coupons = Coupon.objects.filter(is_active=True).order_by('-created_at')
    available = []

    for c in coupons:
        
        if c.start_date and c.start_date > today:
            continue

        if c.end_date and c.end_date < today:
            continue
        
        if c.usage_limit and c.used_count >= c.usage_limit:
            continue

        if c.discount_type == 'percentage':
            discount_display = f"{int(c.discount_value) if c.discount_value % 1 == 0 else c.discount_value}% OFF"
        else:
            discount_display = f"₹{int(c.discount_value) if c.discount_value % 1 == 0 else c.discount_value} OFF"

        min_order = float(c.min_order_amount or 0)
        max_discount = float(c.max_discount or 0) if c.max_discount else 0

        desc = c.description
        if not desc:
            if min_order > 0:
                desc = f"{discount_display} on orders above ₹{int(min_order):,}"
                if max_discount > 0:
                    desc += f" (Max savings ₹{int(max_discount):,})"
            else:
                desc = f"Instant {discount_display} on entire order"

        validity_text = f"Valid till {c.end_date.strftime('%d %b %Y')}" if c.end_date else "Limited time"

        available.append({
            'code': c.code,
            'discount_type': c.discount_type,
            'discount_value': float(c.discount_value),
            'discount_display': discount_display,
            'min_order': min_order,
            'min_order_display': f"₹{int(min_order):,}" if min_order > 0 else "No Minimum",
            'max_discount': max_discount,
            'max_discount_display': f"₹{int(max_discount):,}" if max_discount > 0 else "No Cap",
            'description': desc,
            'validity': validity_text,
        })

    return JsonResponse({'status': 'success', 'coupons': available})


@require_http_methods(["GET", "POST"])
def api_apply_coupon(request):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            data = request.POST
        code = (data.get('code') or '').strip().upper()
        try:
            subtotal = Decimal(str(data.get('subtotal', 0)))
        except Exception:
            subtotal = Decimal('0.00')
    else:
        code = request.GET.get('code', '').strip().upper()
        try:
            subtotal = Decimal(str(request.GET.get('subtotal', 0)))
        except Exception:
            subtotal = Decimal('0.00')

    if not code:
        return JsonResponse({'status': 'error', 'message': 'Please enter a coupon code.'}, status=400)

    coupon = Coupon.objects.filter(code__iexact=code).first()
    if not coupon:
        return JsonResponse({'status': 'error', 'message': f"Coupon code '{code}' is not valid."}, status=404)

    today = timezone.now().date()
    if not coupon.is_active:
        return JsonResponse({'status': 'error', 'message': f"Coupon '{code}' is no longer active."}, status=400)

    if coupon.start_date and coupon.start_date > today:
        return JsonResponse({
            'status': 'error',
            'message': f"Coupon '{code}' is scheduled and starts on {coupon.start_date.strftime('%d %b %Y')}."
        }, status=400)

    if coupon.end_date and coupon.end_date < today:
        return JsonResponse({
            'status': 'error',
            'message': f"Coupon '{code}' expired on {coupon.end_date.strftime('%d %b %Y')}."
        }, status=400)

    if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
        return JsonResponse({
            'status': 'error',
            'message': f"Coupon '{code}' has reached its maximum redemption limit."
        }, status=400)

    if subtotal < coupon.min_order_amount:
        diff = coupon.min_order_amount - subtotal
        return JsonResponse({
            'status': 'error',
            'message': f"Minimum cart subtotal of ₹{coupon.min_order_amount:,.2f} required for '{code}'. Add ₹{diff:,.2f} more to apply."
        }, status=400)

    
    if coupon.discount_type == 'percentage':
        discount = (subtotal * (coupon.discount_value / Decimal('100'))).quantize(Decimal('0.01'))
        if coupon.max_discount and discount > coupon.max_discount:
            discount = coupon.max_discount
    else:
        discount = min(coupon.discount_value, subtotal).quantize(Decimal('0.01'))

    new_subtotal = max(Decimal('0.00'), subtotal - discount)

    request.session['applied_coupon'] = {
        'code': coupon.code,
        'discount_type': coupon.discount_type,
        'discount_value': float(coupon.discount_value),
        'discount_amount': float(discount),
        'min_order_amount': float(coupon.min_order_amount),
        'max_discount': float(coupon.max_discount) if coupon.max_discount else None,
    }
    request.session.modified = True

    return JsonResponse({
        'status': 'success',
        'code': coupon.code,
        'discount_amount': float(discount),
        'discount_display': f"-₹{discount:,.2f}",
        'original_subtotal': float(subtotal),
        'discounted_subtotal': float(new_subtotal),
        'message': f"Coupon '{coupon.code}' applied successfully! You saved ₹{discount:,.2f}."
    })


@require_http_methods(["GET", "POST"])
def api_remove_coupon(request):
    
    if 'applied_coupon' in request.session:
        del request.session['applied_coupon']
        request.session.modified = True
    return JsonResponse({'status': 'success', 'message': 'Coupon removed.'})



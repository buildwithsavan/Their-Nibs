import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theirnibs.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from admin_panel.models import Seller

def setup_demo_accounts():
    print("=== Setting up Demo Accounts ===")
    
    # 1. Admin
    admin_user, created = User.objects.get_or_create(username='admin')
    admin_user.email = 'admin@theirnibs.com'
    admin_user.first_name = 'Platform'
    admin_user.last_name = 'Admin'
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.set_password('admin123')
    admin_user.save()
    print(f"[{'CREATED' if created else 'UPDATED'}] Admin account: username='admin', password='admin123'")

    # 2. Seller
    seller_user, created = User.objects.get_or_create(username='seller@gmail.com')
    seller_user.email = 'seller@gmail.com'
    seller_user.first_name = 'Demo'
    seller_user.last_name = 'Seller'
    seller_user.is_staff = False
    seller_user.is_superuser = False
    seller_user.set_password('seller123')
    seller_user.save()
    print(f"[{'CREATED' if created else 'UPDATED'}] Seller user: username='seller@gmail.com', password='seller123'")

    seller_profile, s_created = Seller.objects.get_or_create(
        user=seller_user,
        defaults={
            'store_name': 'Their Nibs Flagship Boutique',
            'business_name': 'Their Nibs Ltd',
            'email': 'seller@gmail.com',
            'phone': '+91 9876543210',
            'status': 'approved',
            'commission_rate': 10.00,
        }
    )
    if not s_created:
        seller_profile.email = 'seller@gmail.com'
        seller_profile.status = 'approved'
        seller_profile.save()
    print(f"[{'CREATED' if s_created else 'VERIFIED'}] Seller profile for {seller_profile.store_name} (Status: {seller_profile.status})")

    # 3. User (Customer)
    customer_user, created = User.objects.get_or_create(username='user@gmail.com')
    customer_user.email = 'user@gmail.com'
    customer_user.first_name = 'Demo'
    customer_user.last_name = 'Customer'
    customer_user.is_staff = False
    customer_user.is_superuser = False
    customer_user.set_password('user123')
    customer_user.save()
    print(f"[{'CREATED' if created else 'UPDATED'}] Customer user: username='user@gmail.com', password='user123'")

    print("\n=== Verifying Authentication ===")
    u_admin = authenticate(username='admin', password='admin123')
    print("Admin Auth Check:", "SUCCESS" if u_admin else "FAILED")

    u_seller = authenticate(username='seller@gmail.com', password='seller123')
    print("Seller Auth Check:", "SUCCESS" if u_seller else "FAILED")

    u_customer = authenticate(username='user@gmail.com', password='user123')
    print("Customer Auth Check:", "SUCCESS" if u_customer else "FAILED")

if __name__ == '__main__':
    setup_demo_accounts()

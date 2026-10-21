from admin_panel.models import Seller, SellerNotification

def seller_context(request):
    if not request.path.startswith('/seller-panel'):
        return {}

    seller = None
    if request.user and request.user.is_authenticated:
        
        seller = Seller.objects.filter(user=request.user).first()
        
        if not seller and request.user.email:
            seller = Seller.objects.filter(email__iexact=request.user.email).first()
            if seller and not seller.user:
                seller.user = request.user
                seller.save()

    if not seller:
        seller = Seller.objects.order_by('-id').first()

    seller_unread_notifications = []
    seller_unread_count = 0
    seller_all_notifications = []

    if seller:
        try:
            seller_unread_notifications = list(SellerNotification.objects.filter(seller=seller, is_read=False).order_by('-created_at')[:5])
            seller_unread_count = SellerNotification.objects.filter(seller=seller, is_read=False).count()
            seller_all_notifications = list(SellerNotification.objects.filter(seller=seller).order_by('-created_at')[:20])
        except Exception:
            pass

    return {
        'seller': seller,
        'seller_notifications': seller_all_notifications,
        'seller_unread_notifications': seller_unread_notifications,
        'seller_unread_count': seller_unread_count,
    }

from .models import AdminNotification, StoreSetting, Product, Order, ProductReview, Seller
from .permissions import get_user_role


def admin_context(request):
    if not request.path.startswith('/admin-panel') and not request.path.startswith('/admin'):
        return {}

    unread_notifications = []
    unread_count = 0
    low_stock_count = 0
    pending_orders_count = 0
    pending_reviews_count = 0
    pending_cod_count = 0
    pending_sellers_count = 0
    user_role = None

    if request.user.is_authenticated:
        user_role = get_user_role(request.user)
        try:
            unread_notifications = list(AdminNotification.objects.filter(is_read=False)[:5])
            unread_count = AdminNotification.objects.filter(is_read=False).count()
            low_stock_count = Product.objects.filter(stock__lte=10, status='active').count()
            pending_orders_count = Order.objects.filter(status='pending').count()
            pending_reviews_count = ProductReview.objects.filter(status='pending').count()
            pending_cod_count = Order.objects.filter(cod_status='pending').count()
            pending_sellers_count = Seller.objects.filter(status='pending').count()
        except Exception:
            pass

    store_settings = StoreSetting.get_settings()

    return {
        'store_settings': store_settings,
        'unread_notifications': unread_notifications,
        'unread_count': unread_count,
        'nav_low_stock_count': low_stock_count,
        'nav_pending_orders_count': pending_orders_count,
        'nav_pending_reviews_count': pending_reviews_count,
        'nav_pending_cod_count': pending_cod_count,
        'nav_pending_sellers_count': pending_sellers_count,
        'current_user_role': user_role,
    }


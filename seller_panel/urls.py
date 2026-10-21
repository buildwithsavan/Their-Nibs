from django.urls import path
from . import views

app_name = 'seller_panel'

urlpatterns = [
    # Dashboard
    path('', views.seller_dashboard_view, name='index'),
    path('dashboard/', views.seller_dashboard_view, name='dashboard'),
    path('logout/', views.seller_logout_view, name='logout'),

    # Catalog
    path('products/', views.my_products_view, name='my_products'),
    path('products/add/', views.add_product_view, name='add_product'),
    path('products/<int:pk>/delete/', views.delete_product_view, name='delete_product'),
    path('products/variants/', views.product_variants_view, name='product_variants'),

    # Inventory
    path('inventory/', views.my_inventory_view, name='my_inventory'),
    path('inventory/low-stock/', views.low_stock_view, name='low_stock'),
    path('inventory/update-stock/', views.update_stock_action_view, name='update_stock_action'),

    # Orders & Fulfillment
    path('orders/', views.orders_view, name='orders'),
    path('orders/ready-to-ship/', views.ready_to_ship_view, name='ready_to_ship'),
    path('orders/track/', views.seller_track_order_view, name='seller_track_order_default'),
    path('orders/track/<str:order_number>/', views.seller_track_order_view, name='seller_track_order'),
    path('shipping/', views.shipping_view, name='shipping'),
    path('returns/', views.returns_view, name='returns'),

    # Finance
    path('finance/earnings/', views.earnings_view, name='earnings'),
    path('finance/payments/', views.payments_view, name='payments'),
    path('finance/transactions/', views.transactions_view, name='transactions'),

    # Marketing
    path('marketing/promotions/', views.promotions_view, name='promotions'),
    path('marketing/promotions/add/', views.add_promotion_action_view, name='add_promotion_action'),
    path('marketing/coupons/', views.coupons_view, name='coupons'),
    path('marketing/coupons/add/', views.add_coupon_action_view, name='add_coupon_action'),

    # Analytics
    path('analytics/sales/', views.sales_analytics_view, name='sales_analytics'),
    path('analytics/performance/', views.product_performance_view, name='product_performance'),

    # Customer
    path('customer/reviews/', views.reviews_view, name='reviews'),
    path('customer/reviews/reply/', views.reply_review_action_view, name='reply_review_action'),
    path('customer/questions/', views.customer_questions_view, name='customer_questions'),
    path('customer/questions/answer/', views.answer_question_action_view, name='answer_question_action'),

    # Settings
    path('settings/profile/', views.store_profile_view, name='store_profile'),
    path('settings/bank/', views.bank_payment_view, name='bank_payment'),
    path('settings/notifications/', views.notifications_view, name='notifications'),

    # Seller API
    path('api/inventory/update-stock/', views.api_update_stock, name='api_update_stock'),
    path('api/notifications/mark-read/', views.api_mark_notifications_read, name='api_mark_notifications_read'),
    path('api/notifications/dismiss/', views.api_dismiss_notification, name='api_dismiss_notification'),
]

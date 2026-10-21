from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Auth
    path('login/', views.admin_login_view, name='login'),
    path('logout/', views.admin_logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard_view, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Catalog & Products
    path('products/', views.product_list_view, name='product_list'),
    path('products/add/', views.product_create_view, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit_view, name='product_edit'),
    path('products/<int:pk>/toggle-status/', views.product_toggle_status_view, name='product_toggle_status'),
    path('products/<int:pk>/archive/', views.product_archive_view, name='product_archive'),
    path('products/<int:product_id>/variants/add/', views.variant_create_view, name='variant_create'),
    path('products/variants/', views.product_variants_view, name='product_variants'),
    path('variants/<int:pk>/delete/', views.variant_delete_view, name='variant_delete'),

    # Categories & Taxonomy
    path('categories/', views.category_list_view, name='categories'),
    path('categories/<int:pk>/edit/', views.category_edit_view, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete_view, name='category_delete'),
    path('subcategories/', views.subcategory_list_view, name='subcategories'),
    path('subcategories/<int:pk>/delete/', views.subcategory_delete_view, name='subcategory_delete'),
    path('brands/', views.brand_list_view, name='brands'),
    path('brands/<int:pk>/delete/', views.brand_delete_view, name='brand_delete'),
    path('seasons/', views.season_list_view, name='seasons'),
    path('occasions/', views.occasion_list_view, name='occasions'),

    # Inventory
    path('inventory/', views.inventory_list_view, name='inventory'),
    path('inventory/low-stock/', views.low_stock_view, name='low_stock'),

    # Customers
    path('customers/', views.customer_list_view, name='customers'),
    path('customers/<int:pk>/', views.customer_detail_view, name='customer_detail'),

    # Orders
    path('orders/', views.order_list_view, name='orders'),
    path('orders/<int:pk>/', views.order_detail_view, name='order_detail'),

    # Payments & Refunds
    path('payments/', views.payment_list_view, name='payments'),
    path('refunds/', views.refund_list_view, name='refunds'),

    # Marketing
    path('coupons/', views.coupon_list_view, name='coupons'),
    path('coupons/add/', views.coupon_create_view, name='coupon_create'),
    path('coupons/<int:pk>/edit/', views.coupon_edit_view, name='coupon_edit'),
    path('coupons/<int:pk>/delete/', views.coupon_delete_view, name='coupon_delete'),
    path('gift-cards/', views.gift_card_list_view, name='gift_cards'),

    # Wallet
    path('wallet/', views.wallet_list_view, name='wallets'),
    path('wallet/<int:pk>/', views.wallet_detail_view, name='wallet_detail'),

    # Reviews
    path('reviews/', views.review_list_view, name='reviews'),
    path('reviews/<int:pk>/<str:action>/', views.review_action_view, name='review_action'),

    # Seller's Management
    path('sellers/', views.seller_list_view, name='sellers'),
    path('sellers/<int:pk>/<str:action>/', views.seller_action_view, name='seller_action'),

    # Cash on Delivery (CoD) Approvals
    path('cod-requests/', views.cod_requests_view, name='cod_requests'),
    path('cod-requests/<int:pk>/<str:action>/', views.cod_action_view, name='cod_action'),

    # Dedicated Shipping & Logistics
    path('shipping/', views.shipping_dashboard_view, name='shipping'),
    path('shipping/<int:pk>/update-status/', views.shipping_update_status_view, name='shipping_update_status'),

    # Collaboration & Influencers
    path('collaborations/', views.collaboration_list_view, name='collaborations'),
    path('collaborations/<int:pk>/<str:action>/', views.collaboration_action_view, name='collaboration_action'),

    # AI Management
    path('ai/descriptions/', views.ai_descriptions_view, name='ai_descriptions'),
    path('ai/tags/', views.ai_tags_view, name='ai_tags'),
    path('ai/conversations/', views.ai_conversations_view, name='ai_conversations'),
    path('ai/recommendations/', views.ai_recommendations_view, name='ai_recommendations'),

    # Roles, Settings & Audit
    path('roles/', views.roles_list_view, name='roles'),
    path('settings/', views.store_settings_view, name='store_settings'),
    path('audit-logs/', views.audit_log_view, name='audit_logs'),
    path('notifications/', views.notifications_view, name='notifications'),

    # Admin Async APIs
    path('api/ai/generate-description/', views.api_generate_description, name='api_generate_description'),
    path('api/ai/generate-tags/', views.api_generate_tags, name='api_generate_tags'),
    path('api/ai/approve-content/', views.api_approve_ai_content, name='api_approve_ai_content'),
    path('api/inventory/quick-update/', views.api_update_stock, name='api_update_stock'),
    path('api/notifications/mark-read/', views.api_mark_notification_read, name='api_mark_notification_read'),
    path('api/notifications/mark-all-read/', views.api_mark_all_notifications_read, name='api_mark_all_notifications_read'),
]

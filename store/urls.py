from django.urls import path
from . import views
import product.views as product_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('account/', views.customer_orders, name='customer_account'),
    path('account/orders/', views.customer_orders, name='customer_orders'),
    path('account/profile/', views.customer_profile, name='customer_profile'),
    path('account/profile/update/', views.customer_profile_update, name='customer_profile_update'),
    path('account/address/add/', views.customer_address_add, name='customer_address_add'),
    path('account/wishlist/', views.customer_wishlist, name='customer_wishlist'),
    path('account/login/', views.customer_login, name='customer_login'),
    path('account/logout/', views.customer_logout, name='customer_logout'),
    path('account/create/', views.customer_register, name='customer_register'),
    path('seller/login/', views.seller_login_view, name='seller_login'),
    path('seller/logout/', views.seller_logout_view, name='seller_logout'),
    path('seller/register/step1/', views.seller_register_step1, name='seller_register_step1'),
    path('seller/register/step2/', views.seller_register_step2, name='seller_register_step2'),
    path('seller/register/step3/', views.seller_register_step3, name='seller_register_step3'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/place-order/', views.place_order_view, name='place_order'),
    path('order-success/', views.order_success_view, name='order_success'),
    path('order-success/<str:order_number>/', views.order_success_view, name='order_success_with_id'),
    path('order/<str:order_id>/download-invoice/', views.download_invoice_view, name='download_invoice'),
    path('track-order/', views.track_order_view, name='track_order'),
    path('track-order/<str:order_number>/', views.track_order_view, name='track_order_with_id'),

    # Discount Coupons API
    path('api/coupons/available/', views.api_available_coupons, name='api_available_coupons'),
    path('api/coupons/apply/', views.api_apply_coupon, name='api_apply_coupon'),
    path('api/coupons/remove/', views.api_remove_coupon, name='api_remove_coupon'),

    # Product Catalog & Collections
    path('search/', product_views.search_view, name='search'),
    path('api/search/', product_views.search_api_view, name='search_api'),
    path('collections/new-in-1/', product_views.womens_new_in_view, name='womens_new_in'),
    path('collections/<slug:collection_slug>/', product_views.womens_new_in_view, name='collection_detail'),
    path('product/<str:slug>/', product_views.product_detail_view, name='product_detail'),
    path('products/<str:slug>/', product_views.product_detail_view, name='product_detail_plural'),
    path('category/<str:category_name>/', product_views.womens_new_in_view, name='category_page'),

    # Brand & Informational Pages
    path('about-us/', views.about_us_view, name='about_us'),
    path('size-guides/', views.size_guides_view, name='size_guides'),
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('their-nibs-stores/', views.stores_view, name='their_nibs_stores'),
    path('stores/', views.stores_view, name='stores'),
    path('behind-the-seams/', views.behind_the_seams_view, name='behind_the_seams'),
    path('here-to-help/', views.here_to_help_view, name='here_to_help'),
    path('delivery-returns/', views.delivery_returns_view, name='delivery_returns'),
    path('refund-policy/', views.refund_policy_view, name='refund_policy'),
    path('terms-and-conditions/', views.terms_conditions_view, name='terms_conditions'),
    path('terms-conditions/', views.terms_conditions_view, name='terms_conditions_alias'),
    path('terms-of-service/', views.terms_of_service_view, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('pages/<slug:page_slug>/', views.cms_page_view, name='cms_page'),
]


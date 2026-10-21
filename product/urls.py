from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('collections/<slug:collection_slug>/', views.womens_new_in_view, name='collection_detail'),
    path('collections/new-in-1/', views.womens_new_in_view, name='womens_new_in'),
    path('detail/<str:slug>/', views.product_detail_view, name='product_detail'),
    path('search/', views.search_view, name='search'),
    path('api/search/', views.search_api_view, name='search_api'),
]

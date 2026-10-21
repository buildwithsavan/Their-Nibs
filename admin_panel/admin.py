from django.contrib import admin
from .models import (
    Category, Subcategory, Brand, Season, Occasion,
    Seller, Product, ProductImage, ProductVariant,
    Order, OrderItem, OrderTimeline, Coupon, GiftCard
)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'display_order', 'created_at')
    list_editable = ('is_active', 'display_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    ordering = ('display_order', 'name')

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'is_active')
    list_filter = ('category', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'discount_percent', 'final_price', 'status', 'stock', 'is_featured')
    list_filter = ('category', 'status', 'is_featured', 'gender')
    list_editable = ('price', 'discount_percent', 'status', 'stock', 'is_featured')
    search_fields = ('name', 'sku', 'description', 'tags')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]
    ordering = ('-created_at',)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'color', 'size', 'price', 'stock', 'is_available')
    list_filter = ('size', 'is_available')
    search_fields = ('product__name', 'sku')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_url', 'is_primary', 'alt_text')
    list_filter = ('is_primary',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'shipping_name', 'total_amount', 'status', 'payment_method', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_method', 'payment_status')
    search_fields = ('order_number', 'shipping_name', 'shipping_phone')
    inlines = [OrderItemInline]

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'is_active', 'start_date', 'end_date')
    list_filter = ('discount_type', 'is_active')
    search_fields = ('code',)

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'email', 'phone', 'status', 'rating')
    list_filter = ('status',)
    search_fields = ('store_name', 'email')

from django import forms
from django.contrib.auth.models import User
from .models import (
    Product, ProductVariant, Category, Subcategory, Brand, Season, Occasion, Seller,
    Coupon, GiftCard, Wallet, StoreSetting
)


class AdminLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'admin@theirnibs.com or username',
            'id': 'login-username',
            'autocomplete': 'username',
            'required': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••••••',
            'id': 'login-password',
            'autocomplete': 'current-password',
            'required': True
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'remember-me'})
    )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'sku', 'brand', 'seller', 'category', 'subcategory', 'gender',
            'description', 'material', 'price', 'discount_percent',
            'season', 'occasion', 'color', 'size', 'stock', 'status',
            'image_url', 'tags', 'is_featured'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Celestial Star Satin Pyjama Set'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. TN-PYJ-001'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'seller': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'id_category'}),
            'subcategory': forms.Select(attrs={'class': 'form-select', 'id': 'id_subcategory'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detailed garment description...'}),
            'material': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 100% Organic Silk & Satin'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.5'}),
            'season': forms.Select(attrs={'class': 'form-select'}),
            'occasion': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Navy Gold'}),
            'size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. S / M / L'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://images.unsplash.com/...'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Silk, Loungewear, Autumn, Star Print'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['sku', 'color', 'size', 'price', 'stock', 'image_url', 'is_available']
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. TN-PYJ-001-NVY-M'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color'}),
            'size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Size'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'image_url', 'display_order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'auto-generated if empty'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['category', 'name', 'slug', 'description', 'is_active']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'slug', 'logo_url', 'description', 'website', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'logo_url': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['name', 'slug', 'banner_url', 'description', 'start_month', 'end_month', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'banner_url': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_month': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'end_month': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class OccasionForm(forms.ModelForm):
    class Meta:
        model = Occasion
        fields = ['name', 'slug', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            'code', 'description', 'discount_type', 'discount_value',
            'min_order_amount', 'max_discount', 'start_date', 'end_date',
            'usage_limit', 'user_usage_limit', 'is_active',
            'applicable_categories', 'applicable_products'
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control text-uppercase', 'placeholder': 'BOUTIQUE10'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10% off on Autumn loungewear'}),
            'discount_type': forms.Select(attrs={'class': 'form-select'}),
            'discount_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'min_order_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'usage_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'user_usage_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'applicable_categories': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
            'applicable_products': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }


class GiftCardForm(forms.ModelForm):
    class Meta:
        model = GiftCard
        fields = ['initial_amount', 'recipient_name', 'recipient_email', 'sender_name', 'message', 'expiry_date']
        widgets = {
            'initial_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 50.00'}),
            'recipient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipient Name'}),
            'recipient_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'recipient@example.com'}),
            'sender_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sender Name'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Personalized gift note...'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class WalletAdjustmentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}))
    transaction_type = forms.ChoiceField(
        choices=[
            ('credit', 'Manual Credit / Promotional'),
            ('refund_credit', 'Refund Credit'),
            ('debit', 'Administrative Debit'),
            ('manual_adjustment', 'General Balance Correction'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    description = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reason for adjustment'}))


class StoreSettingForm(forms.ModelForm):
    class Meta:
        model = StoreSetting
        fields = [
            'site_name', 'tagline', 'contact_email', 'contact_phone',
            'currency_symbol', 'currency_code', 'low_stock_threshold',
            'tax_percentage', 'free_shipping_min', 'shipping_fee',
            'enable_ai_assistant', 'require_ai_approval'
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'currency_symbol': forms.TextInput(attrs={'class': 'form-control'}),
            'currency_code': forms.TextInput(attrs={'class': 'form-control'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'free_shipping_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'shipping_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'enable_ai_assistant': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'require_ai_approval': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = [
            'store_name', 'company_name', 'email', 'phone', 'city', 'state',
            'commission_rate', 'gst_number', 'bank_name', 'account_number', 'ifsc_code',
            'store_description', 'store_logo', 'status'
        ]
        widgets = {
            'store_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Silk & Velvet Studio', 'required': True}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. S&V Apparel Ltd'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seller@example.com', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+44 20 7946 0912', 'required': True}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. London'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Greater London'}),
            'commission_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'placeholder': '15.0'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VAT / Tax Registration'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Barclays Bank'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account number'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sort Code / BIC'}),
            'store_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of boutique vendor...'}),
            'store_logo': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

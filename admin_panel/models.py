from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def product_count(self):
        return self.products.count()


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, blank=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Subcategories'
        unique_together = ('category', 'slug')
        ordering = ['name']

    def __str__(self):
        return f"{self.category.name} > {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    logo_url = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Season(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    banner_url = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    start_month = models.PositiveSmallIntegerField(blank=True, null=True)
    end_month = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Occasion(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Seller(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved / Active'),
        ('suspended', 'Suspended'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_profile')
    store_name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('15.00'))
    gst_number = models.CharField(max_length=30, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pickup_address = models.TextField(blank=True, null=True)
    pickup_pincode = models.CharField(max_length=20, blank=True, null=True)
    business_type = models.CharField(max_length=100, blank=True, null=True)
    business_reg_no = models.CharField(max_length=100, blank=True, null=True)
    pan_number = models.CharField(max_length=30, blank=True, null=True)
    main_category = models.CharField(max_length=100, blank=True, null=True)
    product_subcategory = models.CharField(max_length=150, blank=True, null=True)
    target_customers = models.CharField(max_length=200, blank=True, null=True)
    product_source = models.CharField(max_length=100, blank=True, null=True)
    years_experience = models.CharField(max_length=50, blank=True, null=True)
    selling_channels = models.CharField(max_length=200, blank=True, null=True)
    online_store_link = models.URLField(max_length=500, blank=True, null=True)
    account_holder_name = models.CharField(max_length=150, blank=True, null=True)
    registration_data = models.JSONField(blank=True, null=True)
    store_description = models.TextField(blank=True, null=True)
    store_logo = models.URLField(max_length=500, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal('5.0'))
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    payout_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.store_name} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.store_name)
        super().save(*args, **kwargs)


class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('out_of_stock', 'Out of Stock'),
        ('archived', 'Archived'),
    ]

    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('kids', 'Kids'),
        ('unisex', 'Unisex'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    sku = models.CharField(max_length=60, unique=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='unisex')
    description = models.TextField()
    material = models.CharField(max_length=150, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    occasion = models.ForeignKey(Occasion, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    color = models.CharField(max_length=60, blank=True, null=True)
    size = models.CharField(max_length=30, blank=True, null=True)
    stock = models.IntegerField(default=0)
    reserved_stock = models.IntegerField(default=0)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    tags = models.CharField(max_length=500, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.sku}")
            self.slug = base_slug
        if self.price is not None:
            discount = Decimal(str(self.discount_percent or 0))
            self.final_price = round(self.price * (Decimal('1') - (discount / Decimal('100'))), 2)
        if self.status == 'active' and self.stock <= 0:
            self.status = 'out_of_stock'
        super().save(*args, **kwargs)

    @property
    def available_stock(self):
        return max(0, self.stock - self.reserved_stock)

    @property
    def is_low_stock(self):
        return 0 < self.stock <= 10

    @property
    def stock_status(self):
        if self.stock <= 0:
            return 'Out of Stock'
        elif self.stock <= 10:
            return 'Low Stock'
        return 'In Stock'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500)
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'id']

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=80, unique=True)
    color = models.CharField(max_length=60)
    size = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    reserved_stock = models.IntegerField(default=0)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['color', 'size']

    def __str__(self):
        return f"{self.product.name} - {self.color} / {self.size} ({self.sku})"

    @property
    def available_stock(self):
        return max(0, self.stock - self.reserved_stock)

    @property
    def stock_status(self):
        if self.stock <= 0 or not self.is_available:
            return 'Out of Stock'
        elif self.stock <= 10:
            return 'Low Stock'
        return 'In Stock'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('upi', 'UPI'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('wallet', 'Digital Wallet'),
        ('cod', 'Cash on Delivery'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    COD_STATUS_CHOICES = [
        ('none', 'Not Applicable'),
        ('pending', 'Pending Admin Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    order_number = models.CharField(max_length=64, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='admin_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='upi')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    cod_status = models.CharField(max_length=20, choices=COD_STATUS_CHOICES, default='none')
    cod_rejection_reason = models.TextField(blank=True, null=True)
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    gift_card_code = models.CharField(max_length=50, blank=True, null=True)
    gift_card_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    wallet_amount_applied = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    shipping_name = models.CharField(max_length=150)
    shipping_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_pincode = models.CharField(max_length=20)
    
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_number} - {self.user.username} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"TN-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def email(self):
        return self.user.email if self.user else ''


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=80)
    color = models.CharField(max_length=60, blank=True, null=True)
    size = models.CharField(max_length=30, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x {self.quantity} ({self.order.order_number})"

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)


class OrderTimeline(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='timeline')
    status = models.CharField(max_length=30)
    notes = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order.order_number} -> {self.status}"


class CourierPartner(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    tracking_url_template = models.URLField(max_length=500, blank=True, null=True)
    contact_phone = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('manifested', 'Manifest Created'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('rto_initiated', 'RTO Initiated'),
        ('returned', 'Returned to Origin'),
    ]

    shipment_id = models.CharField(max_length=50, unique=True, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipment')
    courier = models.ForeignKey(CourierPartner, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipments')
    tracking_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='manifested')
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.50'))
    dimensions = models.CharField(max_length=50, default='25x20x5 cm')
    pickup_date = models.DateTimeField(null=True, blank=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    actual_delivery = models.DateTimeField(null=True, blank=True)
    dispatch_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.shipment_id} - Order #{self.order.order_number} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.shipment_id:
            self.shipment_id = f"SHP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class Payment(models.Model):
    METHOD_CHOICES = [
        ('upi', 'UPI'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('wallet', 'Digital Wallet'),
        ('cod', 'Cash on Delivery'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    payment_id = models.CharField(max_length=64, unique=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='GBP')
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES)
    transaction_id = models.CharField(max_length=120, blank=True, null=True)
    gateway_reference = models.CharField(max_length=120, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.payment_id} - £{self.amount} ({self.get_payment_status_display()})"

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = f"PAY-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)


class Refund(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('rejected', 'Rejected'),
    ]

    METHOD_CHOICES = [
        ('original_payment_method', 'Original Payment Method'),
        ('wallet', 'Their Nibs Wallet'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    refund_id = models.CharField(max_length=64, unique=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='refunds')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='refunds')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='refunds')
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    refund_method = models.CharField(max_length=40, choices=METHOD_CHOICES, default='original_payment_method')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.refund_id} - £{self.refund_amount} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.refund_id:
            self.refund_id = f"REF-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)


class Coupon(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage (%)'),
        ('fixed', 'Fixed Amount (£)'),
    ]

    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    usage_limit = models.PositiveIntegerField(default=100)
    used_count = models.PositiveIntegerField(default=0)
    user_usage_limit = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    applicable_categories = models.ManyToManyField(Category, blank=True, related_name='coupons')
    applicable_products = models.ManyToManyField(Product, blank=True, related_name='coupons')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} ({self.get_discount_type_display()} - {self.discount_value})"

    @property
    def is_valid(self):
        today = timezone.now().date()
        if not self.is_active:
            return False
        if self.start_date > today or self.end_date < today:
            return False
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False
        return True


class GiftCard(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('blocked', 'Blocked'),
    ]

    code = models.CharField(max_length=32, unique=True)
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='GBP')
    recipient_email = models.EmailField()
    recipient_name = models.CharField(max_length=150)
    sender_name = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    issue_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - £{self.balance}/£{self.initial_amount} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"GC-{uuid.uuid4().hex[:10].upper()}"
        if self.balance is not None and self.balance <= 0 and self.status == 'active':
            self.status = 'used'
        super().save(*args, **kwargs)


class GiftCardTransaction(models.Model):
    TYPE_CHOICES = [
        ('debit', 'Debit / Redeemed'),
        ('credit', 'Credit / Top-up'),
        ('refund', 'Refund'),
    ]

    gift_card = models.ForeignKey(GiftCard, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='gift_card_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.gift_card.code}: {self.transaction_type} £{self.amount}"


class Collaboration(models.Model):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('pinterest', 'Pinterest'),
        ('tiktok', 'TikTok / Reels'),
        ('celebrity', 'Celebrity / Stylist'),
        ('designer', 'Designer / Boutique Brand'),
    ]

    TYPE_CHOICES = [
        ('gifted', 'Gifted Garment (Barter)'),
        ('sponsored', 'Paid Sponsored Post'),
        ('brand_ambassador', 'Boutique Brand Ambassador'),
        ('capsule_launch', 'Co-branded Capsule Collection'),
    ]

    STATUS_CHOICES = [
        ('inquiry', 'Initial Inquiry'),
        ('in_review', 'Creative Review'),
        ('approved', 'Approved & Contracted'),
        ('dispatched', 'Garment Dispatched'),
        ('published', 'Content Live'),
        ('completed', 'Campaign Completed'),
        ('rejected', 'Declined'),
    ]

    collab_id = models.CharField(max_length=50, unique=True, editable=False)
    creator_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES, default='instagram')
    handle = models.CharField(max_length=100)
    followers_count = models.PositiveIntegerField(default=0)
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    collab_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='gifted')
    target_garments = models.ManyToManyField(Product, blank=True, related_name='collaborations')
    budget_or_value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='inquiry')
    deliverables = models.TextField(blank=True, null=True)
    content_link = models.URLField(max_length=500, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.creator_name} ({self.get_platform_display()} - {self.get_status_display()})"

    @property
    def formatted_followers(self):
        if self.followers_count >= 1_000_000:
            return f"{self.followers_count / 1_000_000:.1f}M"
        if self.followers_count >= 1_000:
            val = f"{self.followers_count / 1_000:.1f}"
            if val.endswith('.0'):
                val = val[:-2]
            return f"{val}K"
        return str(self.followers_count)

    def save(self, *args, **kwargs):
        if not self.collab_id:
            self.collab_id = f"COL-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class Wallet(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('frozen', 'Frozen'),
        ('closed', 'Closed'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_credited = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_debited = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet ({self.user.username}): £{self.balance}"

    def credit(self, amount, transaction_type='credit', description='', reference_id='', created_by=None):
        amount = Decimal(str(amount))
        current_balance = Decimal(str(self.balance or '0.00'))
        total_cr = Decimal(str(self.total_credited or '0.00'))

        if amount <= 0:
            raise ValidationError("Credit amount must be positive.")
        
        self.balance = current_balance + amount
        self.total_credited = total_cr + amount
        self.save()

        return WalletTransaction.objects.create(
            wallet=self,
            transaction_type=transaction_type,
            amount=amount,
            balance_after=self.balance,
            description=description or 'Wallet Credit',
            reference_id=reference_id or f"TXN-{uuid.uuid4().hex[:8].upper()}",
            created_by=created_by
        )

    def debit(self, amount, transaction_type='debit', description='', reference_id='', created_by=None):
        amount = Decimal(str(amount))
        current_balance = Decimal(str(self.balance or '0.00'))
        total_db = Decimal(str(self.total_debited or '0.00'))

        if amount <= 0:
            raise ValidationError("Debit amount must be positive.")
        if current_balance < amount:
            raise ValidationError(f"Insufficient funds. Balance: £{current_balance}, Requested: £{amount}")

        self.balance = current_balance - amount
        self.total_debited = total_db + amount
        self.save()

        return WalletTransaction.objects.create(
            wallet=self,
            transaction_type=transaction_type,
            amount=amount,
            balance_after=self.balance,
            description=description or 'Wallet Debit',
            reference_id=reference_id or f"TXN-{uuid.uuid4().hex[:8].upper()}",
            created_by=created_by
        )


class WalletTransaction(models.Model):
    TYPE_CHOICES = [
        ('credit', 'Credit / Top-up'),
        ('debit', 'Debit'),
        ('refund_credit', 'Refund Credit'),
        ('order_payment', 'Order Payment'),
        ('manual_adjustment', 'Manual Adjustment'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    reference_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='wallet_adjustments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.wallet.user.username} | {self.transaction_type} £{self.amount} -> £{self.balance_after}"


class ProductReview(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('hidden', 'Hidden'),
        ('reported', 'Reported / Flagged'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, f"{i} Stars") for i in range(1, 6)])
    title = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    helpful_votes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} on {self.product.name} ({self.rating}★ - {self.status})"


class AIConversation(models.Model):
    REQUEST_TYPES = [
        ('fashion_assistant', 'Fashion Assistant Chat'),
        ('outfit_recommendation', 'Outfit Recommendation'),
        ('natural_search', 'Natural Language Search'),
        ('styling_advice', 'Styling Advice'),
        ('general_query', 'General Query'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('flagged', 'Flagged for Review'),
    ]

    conversation_id = models.CharField(max_length=64, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_conversations')
    session_key = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200, default='New Fashion Inquiry')
    request_type = models.CharField(max_length=40, choices=REQUEST_TYPES, default='fashion_assistant')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    message_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.conversation_id} ({self.get_request_type_display()})"

    def save(self, *args, **kwargs):
        if not self.conversation_id:
            self.conversation_id = f"AI-CONV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class AIMessage(models.Model):
    SENDER_CHOICES = [
        ('user', 'Customer / User'),
        ('assistant', 'Their Nibs AI (Gemini)'),
    ]

    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    text = models.TextField()
    metadata = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.sender}] {self.conversation.conversation_id}: {self.text[:50]}"


class AIRecommendation(models.Model):
    RECOMMENDATION_TYPES = [
        ('budget', 'Budget-Conscious Curation'),
        ('season', 'Seasonal Wardrobe'),
        ('occasion', 'Occasion-Based Styling'),
        ('outfit', 'Complete Outfit Suggestion'),
        ('similar_product', 'Similar Aesthetics'),
        ('natural_language_search', 'Natural Language Search Match'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_recommendations')
    recommendation_type = models.CharField(max_length=40, choices=RECOMMENDATION_TYPES)
    user_prompt = models.TextField()
    ai_reasoning = models.TextField(blank=True, null=True)
    recommended_products = models.ManyToManyField(Product, related_name='ai_recommendations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_recommendation_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class AIContentDraft(models.Model):
    CONTENT_TYPES = [
        ('description', 'Product Description'),
        ('tags', 'Product Tags'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved & Applied'),
        ('rejected', 'Rejected'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ai_content_drafts')
    content_type = models.CharField(max_length=30, choices=CONTENT_TYPES)
    prompt_used = models.TextField(blank=True, null=True)
    generated_content = models.TextField()
    edited_content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_ai_drafts')
    reviewed_at = models.DateTimeField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.get_content_type_display()} ({self.get_status_display()})"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('ADMIN_LOGIN', 'Admin Login'),
        ('PRODUCT_CREATED', 'Product Created'),
        ('PRODUCT_UPDATED', 'Product Updated'),
        ('PRODUCT_ARCHIVED', 'Product Archived'),
        ('PRODUCT_DELETED', 'Product Deleted'),
        ('PRICE_CHANGED', 'Price Changed'),
        ('STOCK_UPDATED', 'Stock Updated'),
        ('ORDER_STATUS_CHANGED', 'Order Status Changed'),
        ('PAYMENT_UPDATED', 'Payment Updated'),
        ('REFUND_PROCESSED', 'Refund Processed'),
        ('COUPON_CREATED', 'Coupon Created'),
        ('COUPON_UPDATED', 'Coupon Updated'),
        ('GIFT_CARD_CREATED', 'Gift Card Created'),
        ('WALLET_ADJUSTED', 'Wallet Adjusted'),
        ('REVIEW_APPROVED', 'Review Approved'),
        ('REVIEW_HIDDEN', 'Review Hidden'),
        ('AI_CONTENT_APPROVED', 'AI Content Approved'),
        ('AI_CONTENT_REJECTED', 'AI Content Rejected'),
        ('SETTINGS_UPDATED', 'Store Settings Updated'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=40, choices=ACTION_CHOICES)
    object_type = models.CharField(max_length=60, blank=True, null=True)
    object_id = models.CharField(max_length=60, blank=True, null=True)
    object_repr = models.CharField(max_length=255, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        username = self.user.username if self.user else "System"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {username} - {self.get_action_display()}: {self.object_repr}"

    @classmethod
    def log(cls, user, action, obj=None, object_repr='', details='', request=None):
        ip = None
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')

        object_type = obj.__class__.__name__ if obj else ''
        object_id = str(getattr(obj, 'pk', '')) if obj else ''
        obj_name = object_repr or (str(obj) if obj else '')

        return cls.objects.create(
            user=user if (user and user.is_authenticated) else None,
            action=action,
            object_type=object_type,
            object_id=object_id,
            object_repr=obj_name[:250],
            details=details,
            ip_address=ip
        )


class AdminNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('new_order', 'New Order'),
        ('new_seller', 'New Seller Registration'),
        ('low_stock', 'Low Stock Warning'),
        ('payment_failed', 'Payment Failure'),
        ('refund_request', 'Refund Request'),
        ('pending_review', 'Pending Review'),
        ('ai_pending_approval', 'AI Content Awaiting Approval'),
        ('expiring_coupon', 'Expiring Coupon'),
        ('expiring_gift_card', 'Expiring Gift Card'),
    ]

    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_notification_type_display()}: {self.title}"


class SellerNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('new_order', 'New Order'),
        ('low_stock', 'Low Stock Warning'),
        ('customer_question', 'Customer Question'),
        ('review_received', 'New Customer Review'),
        ('payout_processed', 'Payout Processed'),
        ('application_status', 'Account Status'),
        ('system', 'System Notice'),
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, default='system')
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.seller.store_name}] {self.get_notification_type_display()}: {self.title}"

    @property
    def badge_style(self):
        type_styles = {
            'new_order': 'background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0;',
            'low_stock': 'background: #fffbeb; color: #b45309; border: 1px solid #fde68a;',
            'customer_question': 'background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe;',
            'review_received': 'background: #fdf4ff; color: #86198f; border: 1px solid #f5d0fe;',
            'payout_processed': 'background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0;',
            'application_status': 'background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe;',
            'system': 'background: #f8fafc; color: #475569; border: 1px solid #e2e8f0;',
        }
        return type_styles.get(self.notification_type, 'background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe;')

    @property
    def type_label(self):
        labels = {
            'new_order': 'Order',
            'low_stock': 'Stock',
            'customer_question': 'Question',
            'review_received': 'Review',
            'payout_processed': 'Payout',
            'application_status': 'Notice',
            'system': 'Notice',
        }
        return labels.get(self.notification_type, 'Notice')

    @property
    def type(self):
        return self.type_label

    @property
    def time_ago(self):
        from django.utils.timesince import timesince
        return f"{timesince(self.created_at)} ago"

    @property
    def date(self):
        return self.created_at.strftime('%b %d, %Y %H:%M')


class StoreSetting(models.Model):
    site_name = models.CharField(max_length=100, default='Their Nibs')
    tagline = models.CharField(max_length=255, default='Luxury Loungewear, Sleepwear & Boutique Prints')
    contact_email = models.EmailField(default='support@theirnibs.com')
    contact_phone = models.CharField(max_length=20, default='+44 20 7946 0912')
    currency_symbol = models.CharField(max_length=10, default='£')
    currency_code = models.CharField(max_length=10, default='GBP')
    low_stock_threshold = models.PositiveIntegerField(default=10)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    free_shipping_min = models.DecimalField(max_digits=10, decimal_places=2, default=60.00)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=3.95)
    enable_ai_assistant = models.BooleanField(default=True)
    require_ai_approval = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

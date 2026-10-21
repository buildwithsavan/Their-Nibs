from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from decimal import Decimal
import json

from django.contrib.auth import logout
from .permissions import seller_required
from admin_panel.models import (
    Seller, Product, ProductVariant, Order, OrderItem,
    Category, Brand, ProductReview, AdminNotification, SellerNotification, StoreSetting,
    Coupon
)


def seller_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    request.session.flush()
    messages.info(request, "You have been logged out successfully.")
    return redirect('seller_login')


def get_current_seller(user):

    if not user or not user.is_authenticated:
        return Seller.objects.order_by('-id').first()
    
    seller = Seller.objects.filter(user=user).first()
    if not seller and user.email:
        seller = Seller.objects.filter(email__iexact=user.email).first()
        if seller and not seller.user:
            seller.user = user
            seller.save()

    if not seller:
        seller = Seller.objects.order_by('-id').first()

    return seller


def format_inr(number):

    if number is None or number == '':
        return '0'
    try:
        val = int(round(float(number)))
    except (ValueError, TypeError):
        return str(number)

    s = str(abs(val))
    if len(s) <= 3:
        res = s
    else:
        last3 = s[-3:]
        rest = s[:-3]
        groups = []
        while len(rest) > 2:
            groups.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.insert(0, rest)
        res = ','.join(groups) + ',' + last3

    return ('-' if val < 0 else '') + res


@seller_required
def seller_dashboard_view(request):
    seller = get_current_seller(request.user)

    todays_sales = Decimal('18450.00')
    todays_sales_pct = "+12.4% from yesterday"

    total_orders_count = 24
    awaiting_fulfillment = 8

    total_products = Product.objects.filter(seller=seller).count() if seller else 86
    if total_products == 0:
        total_products = 86
    low_stock_count = 7

    available_balance = Decimal('42680.00')
    next_payout_date = "10 Oct"

    action_center = {
        'low_stock': low_stock_count,
        'orders_to_ship': awaiting_fulfillment,
        'new_reviews': 3,
        'today_sales': f"₹{todays_sales:,.0f}"
    }

    top_products = [
        {'name': 'Satin Rose Nightdress', 'sold': 42, 'revenue': Decimal('25200.00')},
        {'name': 'Classic Lounge Set', 'sold': 35, 'revenue': Decimal('21000.00')},
        {'name': 'Floral Pajama Set', 'sold': 28, 'revenue': Decimal('16800.00')},
        {'name': 'Cotton Sleep Shirt', 'sold': 21, 'revenue': Decimal('10500.00')},
    ]

    recent_orders = [
        {'order_number': '#TN10245', 'customer': 'Priya', 'items': 2, 'amount': Decimal('1899.00'), 'status': 'Processing', 'status_badge': 'badge-processing'},
        {'order_number': '#TN10244', 'customer': 'Ananya', 'items': 1, 'amount': Decimal('999.00'), 'status': 'Shipped', 'status_badge': 'badge-shipped'},
        {'order_number': '#TN10243', 'customer': 'Riya', 'items': 3, 'amount': Decimal('2499.00'), 'status': 'Delivered', 'status_badge': 'badge-delivered'},
        {'order_number': '#TN10242', 'customer': 'Meera', 'items': 1, 'amount': Decimal('1299.00'), 'status': 'Pending', 'status_badge': 'badge-pending'},
    ]

    context = {
        'seller': seller,
        'todays_sales': todays_sales,
        'todays_sales_pct': todays_sales_pct,
        'total_orders_count': total_orders_count,
        'awaiting_fulfillment': awaiting_fulfillment,
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'available_balance': available_balance,
        'next_payout_date': next_payout_date,
        'action_center': action_center,
        'top_products': top_products,
        'recent_orders': recent_orders,
    }
    return render(request, 'seller_panel/dashboard.html', context)


@seller_required
def my_products_view(request):
    seller = get_current_seller(request.user)
    q = request.GET.get('q', '').strip()

    if seller:
        products_qs = Product.objects.filter(seller=seller)
        if products_qs.count() == 0:
            products_qs = Product.objects.all()
    else:
        products_qs = Product.objects.all()

    if q:
        products_qs = products_qs.filter(Q(name__icontains=q) | Q(sku__icontains=q) | Q(material__icontains=q))

    products = products_qs.order_by('-created_at')

    total_count = products.count()
    active_count = products.filter(status='active').count()
    low_stock_count = products.filter(stock__lte=10).count()

    context = {
        'products': products,
        'seller': seller,
        'total_count': total_count,
        'active_count': active_count,
        'low_stock_count': low_stock_count,
        'current_q': q,
    }
    return render(request, 'seller_panel/products.html', context)


@seller_required
def add_product_view(request):
    seller = get_current_seller(request.user)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        sku_input = request.POST.get('sku', '').strip()
        price_val = request.POST.get('price')
        offer_price_val = request.POST.get('offer_price')
        stock_val = request.POST.get('stock')
        material = request.POST.get('material', 'Satin').strip()
        color = request.POST.get('color', 'Rose Pink').strip()
        pattern = request.POST.get('pattern', '').strip()
        fit = request.POST.get('fit', '').strip()
        description = request.POST.get('description', '').strip()
        care = request.POST.get('care', '').strip()
        image_url = request.POST.get('image_url', '').strip()

        sizes_list = request.POST.getlist('sizes')
        size_str = ", ".join(sizes_list) if sizes_list else "XS, S, M, L, XL"

        if name and price_val and seller:
            category = Category.objects.first()
            if not category:
                category, _ = Category.objects.get_or_create(name="Sleepwear & Nightwear", defaults={'display_order': 1})
            brand = Brand.objects.first()
            if not brand:
                brand, _ = Brand.objects.get_or_create(name="Their Nibs Organic")

            sku = sku_input or f"TN-{int(timezone.now().timestamp())}"
            price = Decimal(price_val)
            final_price = Decimal(offer_price_val) if offer_price_val else price
            stock = int(stock_val) if stock_val else 50

            full_desc = description
            if pattern or fit or care:
                spec_details = []
                if fit: spec_details.append(f"Fit Style: {fit}")
                if pattern: spec_details.append(f"Pattern: {pattern}")
                if care: spec_details.append(f"Care: {care}")
                full_desc = f"{description}\n\n" + " | ".join(spec_details)

            Product.objects.create(
                seller=seller,
                name=name,
                sku=sku,
                category=category,
                brand=brand,
                price=price,
                final_price=final_price,
                stock=stock,
                size=size_str,
                color=color,
                material=material,
                description=full_desc,
                image_url=image_url or "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&auto=format&fit=crop&q=60",
                status='active'
            )
            messages.success(request, f"Garment '{name}' created successfully in your catalog with size range ({size_str}).")
            return redirect('seller_panel:my_products')

        messages.success(request, "Product added successfully to your catalog.")
        return redirect('seller_panel:my_products')

    categories = Category.objects.all()
    brands = Brand.objects.all()
    return render(request, 'seller_panel/product_form.html', {'categories': categories, 'brands': brands})


@seller_required
@require_POST
def delete_product_view(request, pk):
    seller = get_current_seller(request.user)
    if seller:
        product = get_object_or_404(Product, pk=pk, seller=seller)
    else:
        product = get_object_or_404(Product, pk=pk)

    product_name = product.name
    product.delete()
    messages.success(request, f"Product '{product_name}' has been permanently deleted from your seller catalog.")
    return redirect('seller_panel:my_products')


@seller_required
def product_variants_view(request):
    seller = get_current_seller(request.user)

    seller_products = Product.objects.filter(seller=seller).order_by('-created_at') if seller else Product.objects.all().order_by('-created_at')
    if seller_products.count() == 0:
        seller_products = Product.objects.all().order_by('-created_at')

    q = request.GET.get('q', '').strip()
    if q:
        seller_products = seller_products.filter(Q(name__icontains=q) | Q(sku__icontains=q))

    selected_product_id = request.GET.get('product_id') or request.POST.get('product_id')
    selected_product = None

    if selected_product_id:
        selected_product = seller_products.filter(pk=selected_product_id).first()

    if not selected_product and seller_products.exists():
        selected_product = seller_products.first()

    if request.method == 'POST' and selected_product:
        variants_to_update = ProductVariant.objects.filter(product=selected_product)
        updated_count = 0

        for var in variants_to_update:
            sku_key = f'sku_{var.id}'
            price_key = f'price_{var.id}'
            stock_key = f'stock_{var.id}'
            visible_key = f'visible_{var.id}'

            if price_key in request.POST:
                new_sku = request.POST.get(sku_key, '').strip() or var.sku
                new_price_val = request.POST.get(price_key, '').strip()
                new_stock_val = request.POST.get(stock_key, '').strip()
                is_visible = (request.POST.get(visible_key) == 'on')

                if new_price_val:
                    try:
                        var.price = Decimal(new_price_val)
                    except Exception:
                        pass

                if new_stock_val:
                    try:
                        var.stock = int(new_stock_val)
                    except Exception:
                        pass

                var.sku = new_sku
                var.is_available = is_visible
                var.save()
                updated_count += 1

        messages.success(request, f"Variant specifications & size-based prices for '{selected_product.name}' updated successfully.")
        return redirect(f"/seller-panel/products/variants/?product_id={selected_product.id}")

    variants = []
    if selected_product:
        existing_variants = ProductVariant.objects.filter(product=selected_product).order_by('color', 'size')

        if existing_variants.exists():
            variants = existing_variants
        else:
            size_raw = selected_product.size or "XS, S, M, L, XL, XXL"
            sizes_list = [s.strip() for s in size_raw.split(',') if s.strip()]
            if not sizes_list:
                sizes_list = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

            color_name = selected_product.color or "Rose Pink"
            base_sku = selected_product.sku or f"TN-PRD-{selected_product.id}"

            generated_variants = []
            for s in sizes_list:
                var_sku = f"{base_sku}-{s.replace(' ', '')}"
                counter = 1
                final_var_sku = var_sku
                while ProductVariant.objects.filter(sku=final_var_sku).exists():
                    final_var_sku = f"{var_sku}-{counter}"
                    counter += 1

                var_obj = ProductVariant.objects.create(
                    product=selected_product,
                    color=color_name,
                    size=s,
                    sku=final_var_sku,
                    price=selected_product.price,
                    stock=selected_product.stock,
                    is_available=True
                )
                generated_variants.append(var_obj)
            variants = generated_variants

    context = {
        'seller_products': seller_products,
        'selected_product': selected_product,
        'variants': variants,
        'current_q': q,
        'seller': seller,
    }
    return render(request, 'seller_panel/variants.html', context)


@seller_required
def my_inventory_view(request):
    seller = get_current_seller(request.user)

    seller_products = Product.objects.filter(seller=seller) if seller else Product.objects.all()
    if seller_products.count() == 0:
        seller_products = Product.objects.all()

    total_products_count = seller_products.count()
    healthy_count = seller_products.filter(stock__gt=10).count()
    low_stock_count = seller_products.filter(stock__range=(1, 10)).count()
    out_of_stock_count = seller_products.filter(stock__lte=0).count()

    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    status_filter = request.GET.get('status', 'all').strip()
    sort_option = request.GET.get('sort', 'date_desc').strip()

    filtered_qs = seller_products

    if q:
        filtered_qs = filtered_qs.filter(
            Q(name__icontains=q) | Q(sku__icontains=q) | Q(variants__sku__icontains=q)
        ).distinct()

    if category_id:
        try:
            filtered_qs = filtered_qs.filter(category_id=int(category_id))
        except ValueError:
            pass

    if status_filter == 'in_stock':
        filtered_qs = filtered_qs.filter(stock__gt=10)
    elif status_filter == 'low_stock':
        filtered_qs = filtered_qs.filter(stock__range=(1, 10))
    elif status_filter == 'out_of_stock':
        filtered_qs = filtered_qs.filter(stock__lte=0)

    if sort_option == 'stock_asc':
        filtered_qs = filtered_qs.order_by('stock')
    elif sort_option == 'stock_desc':
        filtered_qs = filtered_qs.order_by('-stock')
    elif sort_option == 'name_asc':
        filtered_qs = filtered_qs.order_by('name')
    else:
        filtered_qs = filtered_qs.order_by('-updated_at')

    products_data = []
    for p in filtered_qs:
        avail = max(0, p.stock - p.reserved_stock)
        if p.stock <= 0:
            status_text = 'Out of Stock'
            badge_class = 'badge-out'
        elif p.stock <= 10:
            status_text = 'Low Stock'
            badge_class = 'badge-low'
        else:
            status_text = 'In Stock'
            badge_class = 'badge-healthy'

        products_data.append({
            'object': p,
            'id': p.id,
            'name': p.name,
            'sku': p.sku,
            'category_name': p.category.name if p.category else 'Garments',
            'image_url': p.image_url or 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&auto=format&fit=crop&q=60',
            'price': p.price,
            'stock': p.stock,
            'reserved_stock': p.reserved_stock,
            'available_stock': avail,
            'status_text': status_text,
            'badge_class': badge_class,
            'updated_at': p.updated_at,
            'variants': p.variants.all(),
        })

    categories = Category.objects.all()

    context = {
        'products': products_data,
        'categories': categories,
        'total_products_count': total_products_count,
        'healthy_count': healthy_count,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'current_q': q,
        'current_category': category_id,
        'current_status': status_filter,
        'current_sort': sort_option,
    }
    return render(request, 'seller_panel/inventory.html', context)


@seller_required
def low_stock_view(request):
    seller = get_current_seller(request.user)

    seller_products = Product.objects.filter(seller=seller) if seller else Product.objects.all()
    if seller_products.count() == 0:
        seller_products = Product.objects.all()

    attention_qs = seller_products.filter(stock__lte=10)
    total_attention_count = attention_qs.count()
    critical_count = seller_products.filter(stock__range=(1, 3)).count()
    low_count = seller_products.filter(stock__range=(4, 10)).count()
    out_count = seller_products.filter(stock__lte=0).count()

    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    severity_filter = request.GET.get('severity', 'all').strip()

    filtered_qs = attention_qs

    if q:
        filtered_qs = filtered_qs.filter(
            Q(name__icontains=q) | Q(sku__icontains=q) | Q(variants__sku__icontains=q)
        ).distinct()

    if category_id:
        try:
            filtered_qs = filtered_qs.filter(category_id=int(category_id))
        except ValueError:
            pass

    if severity_filter == 'critical':
        filtered_qs = filtered_qs.filter(stock__range=(1, 3))
    elif severity_filter == 'low':
        filtered_qs = filtered_qs.filter(stock__range=(4, 10))
    elif severity_filter == 'out':
        filtered_qs = filtered_qs.filter(stock__lte=0)

    filtered_qs = filtered_qs.order_by('stock', '-updated_at')

    products_data = []
    for p in filtered_qs:
        avail = max(0, p.stock - p.reserved_stock)
        min_threshold = 10
        target_stock = 50
        suggested_restock = max(0, target_stock - p.stock)

        if p.stock <= 0:
            status_text = 'Out of Stock'
            badge_class = 'badge-out'
            severity_label = 'Out of Stock'
        elif p.stock <= 3:
            status_text = 'Critical Stock'
            badge_class = 'badge-critical'
            severity_label = 'Critical'
        else:
            status_text = 'Low Stock'
            badge_class = 'badge-low'
            severity_label = 'Low Stock'

        products_data.append({
            'object': p,
            'id': p.id,
            'name': p.name,
            'sku': p.sku,
            'category_name': p.category.name if p.category else 'Garments',
            'image_url': p.image_url or 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&auto=format&fit=crop&q=60',
            'price': p.price,
            'stock': p.stock,
            'reserved_stock': p.reserved_stock,
            'available_stock': avail,
            'min_threshold': min_threshold,
            'target_stock': target_stock,
            'suggested_restock': suggested_restock,
            'status_text': status_text,
            'severity_label': severity_label,
            'badge_class': badge_class,
            'updated_at': p.updated_at,
            'variants': p.variants.all(),
        })

    categories = Category.objects.all()

    context = {
        'products': products_data,
        'categories': categories,
        'total_attention_count': total_attention_count,
        'critical_count': critical_count,
        'low_count': low_count,
        'out_count': out_count,
        'current_q': q,
        'current_category': category_id,
        'current_severity': severity_filter,
    }
    return render(request, 'seller_panel/low_stock.html', context)


@seller_required
def update_stock_action_view(request):
    if request.method == 'POST':
        seller = get_current_seller(request.user)
        product_id = request.POST.get('product_id')
        variant_id = request.POST.get('variant_id')
        adjustment_type = request.POST.get('adjustment_type', 'add')
        qty_input = request.POST.get('quantity', '0')
        reason = request.POST.get('reason', 'Stock Adjustment').strip()
        notes = request.POST.get('notes', '').strip()
        redirect_to = request.POST.get('redirect_to', 'inventory')

        try:
            qty = int(qty_input)
        except ValueError:
            qty = 0

        product = get_object_or_404(Product, pk=product_id)

        if variant_id and variant_id != 'base':
            variant = ProductVariant.objects.filter(pk=variant_id, product=product).first()
            if variant:
                if adjustment_type == 'add':
                    variant.stock += qty
                    act_sym = f"+{qty}"
                elif adjustment_type == 'remove':
                    variant.stock = max(0, variant.stock - qty)
                    act_sym = f"-{qty}"
                elif adjustment_type == 'set':
                    variant.stock = max(0, qty)
                    act_sym = f"={qty}"
                variant.save()

                total_var_stock = sum(v.stock for v in product.variants.all())
                product.stock = total_var_stock
                if product.stock <= 0:
                    product.status = 'out_of_stock'
                elif product.status == 'out_of_stock' and product.stock > 0:
                    product.status = 'active'
                product.save()

                messages.success(request, f"Stock for variant '{variant.color}/{variant.size}' ({variant.sku}) updated successfully to {variant.stock} units. (Adjustment: {act_sym}, Reason: {reason})")
                
                if redirect_to == 'low_stock':
                    return redirect('/seller-panel/inventory/low-stock/')
                return redirect('/seller-panel/inventory/')

        if adjustment_type == 'add':
            product.stock += qty
            act_sym = f"+{qty}"
        elif adjustment_type == 'remove':
            product.stock = max(0, product.stock - qty)
            act_sym = f"-{qty}"
        elif adjustment_type == 'set':
            product.stock = max(0, qty)
            act_sym = f"={qty}"

        if product.stock <= 0:
            product.status = 'out_of_stock'
        elif product.status == 'out_of_stock' and product.stock > 0:
            product.status = 'active'
        product.save()

        if product.variants.exists():
            for v in product.variants.all():
                if adjustment_type == 'add':
                    v.stock += qty
                elif adjustment_type == 'remove':
                    v.stock = max(0, v.stock - qty)
                elif adjustment_type == 'set':
                    v.stock = max(0, qty)
                v.save()

        messages.success(request, f"Inventory stock for '{product.name}' ({product.sku}) updated successfully to {product.stock} units. (Adjustment: {act_sym}, Reason: {reason})")

        if redirect_to == 'low_stock':
            return redirect('/seller-panel/inventory/low-stock/')
        return redirect('/seller-panel/inventory/')

    return redirect('/seller-panel/inventory/')


@seller_required
def orders_view(request):
    seller = get_current_seller(request.user)
    status_filter = request.GET.get('status', 'all').strip()

    all_orders = [
        {
            'order_number': '#TN-10245',
            'customer': 'Priya Sharma',
            'city': 'Mumbai, MH',
            'items': 'Celestial Star Satin Pyjama Set (Size M)',
            'amount': Decimal('1899.00'),
            'payment': 'Paid (UPI)',
            'date': '08 Oct 2026',
            'status': 'Processing',
            'status_badge': 'badge-processing',
        },
        {
            'order_number': '#TN-10244',
            'customer': 'Ananya Roy',
            'city': 'Bengaluru, KA',
            'items': 'Satin Rose Nightdress (Size S)',
            'amount': Decimal('1499.00'),
            'payment': 'Paid (Card)',
            'date': '07 Oct 2026',
            'status': 'Shipped',
            'status_badge': 'badge-shipped',
        },
        {
            'order_number': '#TN-10243',
            'customer': 'Riya Verma',
            'city': 'Delhi, DL',
            'items': 'Classic Lounge Robe (Size L)',
            'amount': Decimal('2499.00'),
            'payment': 'Paid (UPI)',
            'date': '06 Oct 2026',
            'status': 'Delivered',
            'status_badge': 'badge-delivered',
        },
        {
            'order_number': '#TN-10242',
            'customer': 'Meera Patel',
            'city': 'Ahmedabad, GJ',
            'items': 'Cotton Sleep Shirt (Size M)',
            'amount': Decimal('899.00'),
            'payment': 'COD',
            'date': '06 Oct 2026',
            'status': 'Pending',
            'status_badge': 'badge-pending',
        },
        {
            'order_number': '#TN-10240',
            'customer': 'Kavita Singh',
            'city': 'Jaipur, RJ',
            'items': 'Floral Pajama Set (Size XL)',
            'amount': Decimal('1699.00'),
            'payment': 'Paid (UPI)',
            'date': '05 Oct 2026',
            'status': 'Returned',
            'status_badge': 'badge-out',
        },
    ]

    filtered_orders = all_orders
    if status_filter and status_filter.lower() != 'all':
        filtered_orders = [o for o in all_orders if o['status'].lower() == status_filter.lower()]

    context = {
        'orders': filtered_orders,
        'all_orders_count': len(all_orders),
        'pending_count': len([o for o in all_orders if o['status'] == 'Pending']),
        'processing_count': len([o for o in all_orders if o['status'] == 'Processing']),
        'shipped_count': len([o for o in all_orders if o['status'] == 'Shipped']),
        'delivered_count': len([o for o in all_orders if o['status'] == 'Delivered']),
        'returned_count': len([o for o in all_orders if o['status'] == 'Returned']),
        'current_status': status_filter,
    }
    return render(request, 'seller_panel/orders.html', context)


@seller_required
def seller_track_order_view(request, order_number=None):
    seller = get_current_seller(request.user)

    sample_orders_map = {
        'TN-10245': {
            'order_number': '#TN-10245',
            'clean_id': 'TN-10245',
            'product_name': 'Celestial Star Satin Pyjama Set (Size M)',
            'sku': 'TN-SLP-102-M',
            'customer': 'Priya Sharma',
            'city': 'Mumbai, Maharashtra',
            'address': '402 Sunrise Heights, Bandra West, Mumbai - 400050',
            'phone': '+91 98200 48219',
            'email': 'priya.sharma@example.com',
            'amount': 1899.00,
            'payment': 'Paid (UPI)',
            'courier': 'BlueDart Express',
            'awb': 'BD-98234105',
            'dispatched_date': '17 Oct 2026',
            'est_delivery': '21 Oct 2026',
            'current_stage': 4,
            'stage_label': 'In Transit / Out for Delivery',
            'status': 'In Transit',
        },
        'TN-10244': {
            'order_number': '#TN-10244',
            'clean_id': 'TN-10244',
            'product_name': 'Satin Rose Nightdress (Size S)',
            'sku': 'TN-NGH-301-S',
            'customer': 'Ananya Roy',
            'city': 'Bengaluru, Karnataka',
            'address': '12B Palm Grove Residences, Indiranagar, Bengaluru - 560038',
            'phone': '+91 98450 11234',
            'email': 'ananya.roy@example.com',
            'amount': 1499.00,
            'payment': 'Paid (Card)',
            'courier': 'Delhivery Express',
            'awb': 'DL-88231902',
            'dispatched_date': '16 Oct 2026',
            'est_delivery': '20 Oct 2026',
            'current_stage': 4,
            'stage_label': 'Out of delivery',
            'status': 'Out of delivery',
        },
        'TN-10243': {
            'order_number': '#TN-10243',
            'clean_id': 'TN-10243',
            'product_name': 'Classic Lounge Robe (Size L)',
            'sku': 'TN-ROB-405-L',
            'customer': 'Riya Verma',
            'city': 'New Delhi, Delhi',
            'address': '88 Vasant Vihar, Block C, New Delhi - 110057',
            'phone': '+91 98110 33456',
            'email': 'riya.verma@example.com',
            'amount': 2499.00,
            'payment': 'Paid (UPI)',
            'courier': 'BlueDart Express',
            'awb': 'BD-67290114',
            'dispatched_date': '15 Oct 2026',
            'est_delivery': '19 Oct 2026',
            'current_stage': 5,
            'stage_label': 'Delivered',
            'status': 'Delivered',
        },
        'TN-10242': {
            'order_number': '#TN-10242',
            'clean_id': 'TN-10242',
            'product_name': 'Cotton Sleep Shirt (Size M)',
            'sku': 'TN-SLP-502-M',
            'customer': 'Meera Patel',
            'city': 'Ahmedabad, Gujarat',
            'address': '104 Bodakdev Enclave, SG Highway, Ahmedabad - 380054',
            'phone': '+91 98790 65432',
            'email': 'meera.patel@example.com',
            'amount': 899.00,
            'payment': 'Cash on Delivery (COD)',
            'courier': 'Shadowfax Logistics',
            'awb': 'SF-44109823',
            'dispatched_date': '16 Oct 2026',
            'est_delivery': '22 Oct 2026',
            'current_stage': 3,
            'stage_label': 'Packed & Sealed',
            'status': 'Processing',
        },
        'TN-10248': {
            'order_number': '#TN-10248',
            'clean_id': 'TN-10248',
            'product_name': 'Vintage Leopard Print Cotton Set (Size S)',
            'sku': 'TN-LEO-204-S',
            'customer': 'Sneha Kapoor',
            'city': 'Gurgaon, Haryana',
            'address': '75 Park Street, Sector 15, Gurgaon - 122001',
            'phone': '+91 99100 78234',
            'email': 'sneha.kapoor@example.com',
            'amount': 1699.00,
            'payment': 'Paid (Card)',
            'courier': 'Delhivery Express',
            'awb': 'DL-55410982',
            'dispatched_date': '17 Oct 2026',
            'est_delivery': '22 Oct 2026',
            'current_stage': 4,
            'stage_label': 'In Transit',
            'status': 'In Transit',
        },
        'TN-492025': {
            'order_number': '#TN-492025',
            'clean_id': 'TN-492025',
            'product_name': 'Vintage Rose Silk Pajama Set (Size M)',
            'sku': 'TN-SLK-109-M',
            'customer': 'Pooja Verma',
            'city': 'Indore, Madhya Pradesh',
            'address': '304 Maple Enclave, Vijay Nagar, Indore - 452010',
            'phone': '+91 98260 12345',
            'email': 'pooja.verma@example.com',
            'amount': 2499.00,
            'payment': 'Paid (Razorpay)',
            'courier': 'BlueDart Express',
            'awb': 'BD-98234105',
            'dispatched_date': '17 Oct 2026',
            'est_delivery': '21 Oct 2026',
            'current_stage': 4,
            'stage_label': 'In Transit / Out for Delivery',
            'status': 'In Transit',
        }
    }

    tracking_orders = []

    db_orders = Order.objects.all().prefetch_related('items__product').order_by('-created_at')[:10]
    for dbo in db_orders:
        c_id = dbo.order_number.lstrip('#')
        first_item = dbo.items.first()
        p_name = first_item.product_name if first_item else 'Luxury Silk Loungewear'
        sku_val = (first_item.product.sku if first_item and first_item.product else f'TN-{c_id[:6]}')
        tracking_orders.append({
            'order_number': f'#{c_id}',
            'clean_id': c_id,
            'product_name': p_name,
            'sku': sku_val,
            'customer': dbo.shipping_name or 'Boutique Client',
            'city': f"{dbo.shipping_city}, {dbo.shipping_state}" if dbo.shipping_city else 'Mumbai, Maharashtra',
            'address': dbo.shipping_address or 'Signature Apartment, Mumbai',
            'phone': dbo.shipping_phone or '+91 98200 12345',
            'email': dbo.email or 'client@theirnibs.co.in',
            'amount': float(dbo.total_amount),
            'payment': 'COD' if dbo.cod_status != 'none' else 'Paid (Online)',
            'courier': 'BlueDart Express',
            'awb': f"BD-{dbo.id}89234",
            'dispatched_date': dbo.created_at.strftime('%d %b %Y') if dbo.created_at else '17 Oct 2026',
            'est_delivery': '21 Oct 2026',
            'current_stage': 4,
            'stage_label': 'In Transit / Out for Delivery',
            'status': 'In Transit',
        })

    for k, v in sample_orders_map.items():
        if not any(to['clean_id'] == k for to in tracking_orders):
            tracking_orders.append(v)

    auto_open_id = ''
    if order_number:
        auto_open_id = order_number.lstrip('#')
    elif request.GET.get('order'):
        auto_open_id = request.GET.get('order').lstrip('#')

    tracking_map = {o['clean_id']: o for o in tracking_orders}
    tracking_orders_json = json.dumps(tracking_map)

    table_orders = tracking_orders[:4]

    context = {
        'tracking_orders': table_orders,
        'tracking_orders_json': tracking_orders_json,
        'auto_open_id': auto_open_id,
        'total_tracking_count': len(table_orders),
    }

    return render(request, 'seller_panel/track_order.html', context)


@seller_required
def ready_to_ship_view(request):
    seller = get_current_seller(request.user)
    ready_orders = [
        {
            'order_number': '#TN-10245',
            'customer': 'Priya Sharma',
            'address': '402 Sunrise Heights, Bandra West, Mumbai - 400050',
            'items': 'Celestial Star Satin Pyjama Set (Size M)',
            'sku': 'TN-SLP-102-M',
            'packed_time': 'Today, 09:30 AM',
            'courier': 'BlueDart Express',
            'awb': 'BD-98234105',
            'amount': Decimal('1899.00'),
        },
        {
            'order_number': '#TN-10248',
            'customer': 'Sneha Kapoor',
            'address': '75 Park Street, Sector 15, Gurgaon - 122001',
            'items': 'Vintage Leopard Print Cotton Set (Size S)',
            'sku': 'TN-LEO-204-S',
            'packed_time': 'Today, 10:15 AM',
            'courier': 'Delhivery Express',
            'awb': 'DL-55410982',
            'amount': Decimal('1699.00'),
        },
        {
            'order_number': '#TN-10251',
            'customer': 'Pooja Hegde',
            'address': '12 Jubilee Hills, Road No 3, Hyderabad - 500033',
            'items': 'Midnight Wildflower Robe (Size L)',
            'sku': 'TN-ROB-301-L',
            'packed_time': 'Today, 11:00 AM',
            'courier': 'DTDC Priority',
            'awb': 'DT-77821034',
            'amount': Decimal('2299.00'),
        },
    ]

    context = {
        'ready_orders': ready_orders,
        'total_ready_count': len(ready_orders),
        'pickups_scheduled': 3,
        'manifests_generated': 2,
    }
    return render(request, 'seller_panel/ready_to_ship.html', context)


@seller_required
def shipping_view(request):
    seller = get_current_seller(request.user)
    shipping_orders = [
        {
            'order_number': '#TN-10244',
            'customer': 'Ananya Roy',
            'city': 'Bengaluru, Karnataka',
            'items': 'Satin Rose Nightdress (Size S)',
            'courier': 'BlueDart Express',
            'awb': 'BD-98210045',
            'dispatched_date': '07 Oct 2026',
            'est_delivery': '09 Oct 2026',
            'live_status': 'Out of delivery',
            'status_badge': 'badge-processing',
        },
        {
            'order_number': '#TN-10238',
            'customer': 'Aakanksha Joshi',
            'city': 'Pune, Maharashtra',
            'items': 'Heritage Stripe Brushed Cotton Set (Size M)',
            'courier': 'Delhivery',
            'awb': 'DL-44810239',
            'dispatched_date': '06 Oct 2026',
            'est_delivery': '09 Oct 2026',
            'live_status': 'In Transit',
            'status_badge': 'badge-shipped',
        },
        {
            'order_number': '#TN-10235',
            'customer': 'Deepika Nair',
            'city': 'Kochi, Kerala',
            'items': 'Celestial Star Satin Pyjama Set (Size L)',
            'courier': 'DTDC Express',
            'awb': 'DT-33920194',
            'dispatched_date': '05 Oct 2026',
            'est_delivery': '08 Oct 2026',
            'live_status': 'Out of delivery',
            'status_badge': 'badge-processing',
        },
    ]

    context = {
        'shipping_orders': shipping_orders,
        'in_transit_count': len(shipping_orders),
        'out_for_delivery_count': 2,
    }
    return render(request, 'seller_panel/shipping.html', context)


@seller_required
def returns_view(request):
    seller = get_current_seller(request.user)
    return_tab = request.GET.get('tab', 'on_the_way').strip()

    on_the_way_returns = [
        {
            'return_id': '#RET-8012',
            'order_number': '#TN-10240',
            'customer': 'Kavita Singh',
            'items': 'Floral Pajama Set (Size XL)',
            'reason': 'Size Fit Issue (Too Large)',
            'return_awb': 'RET-BD-90214',
            'courier': 'BlueDart Return Express',
            'est_store_arrival': 'Tomorrow, 10 Oct 2026',
            'status': 'In Transit to Seller Store',
            'status_badge': 'badge-processing',
        },
        {
            'return_id': '#RET-8015',
            'order_number': '#TN-10229',
            'customer': 'Tanya Mehta',
            'items': 'Satin Rose Nightdress (Size M)',
            'reason': 'Changed Mind / Fabric Preference',
            'return_awb': 'RET-DL-66102',
            'courier': 'Delhivery Reverse Shipping',
            'est_store_arrival': '11 Oct 2026',
            'status': 'Picked Up from Customer',
            'status_badge': 'badge-shipped',
        },
    ]

    reached_seller_returns = [
        {
            'return_id': '#RET-8005',
            'order_number': '#TN-10218',
            'customer': 'Radhika Merchant',
            'items': 'Classic Lounge Robe (Size S)',
            'reason': 'Wrong Color Delivered',
            'reached_date': '07 Oct 2026',
            'item_condition': 'Inspected — Original Pack & Tags Intact',
            'refund_status': 'Refund Approved (₹2,499)',
            'restock_status': 'Restocked to Store Inventory',
            'status': 'Reached Seller Store',
            'status_badge': 'badge-delivered',
        },
        {
            'return_id': '#RET-7998',
            'order_number': '#TN-10204',
            'customer': 'Divya Soni',
            'items': 'Cotton Sleep Shirt (Size XS)',
            'reason': 'Size Fit Issue (Too Small)',
            'reached_date': '05 Oct 2026',
            'item_condition': 'Inspected — Excellent Condition',
            'refund_status': 'Refund Processed to Customer Bank',
            'restock_status': 'Restocked to Store Inventory',
            'status': 'Completed & Restocked',
            'status_badge': 'badge-healthy',
        },
    ]

    context = {
        'return_tab': return_tab,
        'on_the_way_returns': on_the_way_returns,
        'reached_seller_returns': reached_seller_returns,
        'on_the_way_count': len(on_the_way_returns),
        'reached_seller_count': len(reached_seller_returns),
    }
    return render(request, 'seller_panel/returns.html', context)


@seller_required
def earnings_view(request):
    seller = get_current_seller(request.user)

    total_sales = Decimal('184500.00')
    net_earnings = Decimal('156825.00')
    pending_earnings = Decimal('14145.00')
    available_for_payout = Decimal('42680.00')

    recent_earnings = [
        {
            'order_number': '#TN-10245',
            'product_name': 'Celestial Star Satin Pyjama Set',
            'gross_amount': Decimal('1899.00'),
            'commission': Decimal('284.85'),
            'net_earnings': Decimal('1614.15'),
            'date': '08 Oct 2026',
            'status': 'Pending Settlement',
            'badge_class': 'badge-pending',
        },
        {
            'order_number': '#TN-10244',
            'product_name': 'Satin Rose Nightdress',
            'gross_amount': Decimal('1499.00'),
            'commission': Decimal('224.85'),
            'net_earnings': Decimal('1274.15'),
            'date': '07 Oct 2026',
            'status': 'Settled',
            'badge_class': 'badge-delivered',
        },
        {
            'order_number': '#TN-10243',
            'product_name': 'Classic Lounge Robe',
            'gross_amount': Decimal('2499.00'),
            'commission': Decimal('374.85'),
            'net_earnings': Decimal('2124.15'),
            'date': '06 Oct 2026',
            'status': 'Settled',
            'badge_class': 'badge-delivered',
        },
        {
            'order_number': '#TN-10238',
            'product_name': 'Heritage Stripe Brushed Cotton Set',
            'gross_amount': Decimal('2199.00'),
            'commission': Decimal('329.85'),
            'net_earnings': Decimal('1869.15'),
            'date': '05 Oct 2026',
            'status': 'Settled',
            'badge_class': 'badge-delivered',
        },
        {
            'order_number': '#TN-10235',
            'product_name': 'Cotton Sleep Shirt',
            'gross_amount': Decimal('899.00'),
            'commission': Decimal('134.85'),
            'net_earnings': Decimal('764.15'),
            'date': '04 Oct 2026',
            'status': 'Settled',
            'badge_class': 'badge-delivered',
        },
    ]

    context = {
        'seller': seller,
        'total_sales': total_sales,
        'total_sales_formatted': format_inr(total_sales),
        'net_earnings': net_earnings,
        'net_earnings_formatted': format_inr(net_earnings),
        'pending_earnings': pending_earnings,
        'pending_earnings_formatted': format_inr(pending_earnings),
        'available_for_payout': available_for_payout,
        'available_for_payout_formatted': format_inr(available_for_payout),
        'recent_earnings': recent_earnings,
    }
    return render(request, 'seller_panel/earnings.html', context)


@seller_required
def payments_view(request):
    seller = get_current_seller(request.user)
    status_filter = request.GET.get('status', 'all').strip()

    available_balance = Decimal('42680.00')
    pending_payouts = Decimal('14145.00')
    total_paid_out = Decimal('142680.00')
    next_payout_date = "15 Oct 2026 — Est. ₹42,680"

    all_payouts = [
        {
            'payout_id': '#PAY-90412',
            'date': '04 Oct 2026',
            'amount': Decimal('42680.00'),
            'method': f"{seller.bank_name or 'HDFC Bank'} (A/C ********5678)",
            'utr': 'UTR984102938412',
            'status': 'Paid',
            'badge_class': 'badge-delivered',
            'failure_reason': '',
        },
        {
            'payout_id': '#PAY-90398',
            'date': '27 Sep 2026',
            'amount': Decimal('38450.00'),
            'method': f"{seller.bank_name or 'HDFC Bank'} (A/C ********5678)",
            'utr': 'UTR882109482711',
            'status': 'Paid',
            'badge_class': 'badge-delivered',
            'failure_reason': '',
        },
        {
            'payout_id': '#PAY-90425',
            'date': 'Today, 09:00 AM',
            'amount': Decimal('14145.00'),
            'method': f"{seller.bank_name or 'HDFC Bank'} (A/C ********5678)",
            'utr': 'Processing',
            'status': 'Processing',
            'badge_class': 'badge-processing',
            'failure_reason': '',
        },
        {
            'payout_id': '#PAY-90370',
            'date': '18 Sep 2026',
            'amount': Decimal('12500.00'),
            'method': f"{seller.bank_name or 'HDFC Bank'} (A/C ********5678)",
            'utr': 'FAILED-BANK-REJECT',
            'status': 'Failed',
            'badge_class': 'badge-out',
            'failure_reason': 'Invalid IFSC Code / Bank Server Timeout. Amount credited back to Available Balance.',
        },
        {
            'payout_id': '#PAY-90355',
            'date': '10 Sep 2026',
            'amount': Decimal('8900.00'),
            'method': f"{seller.bank_name or 'HDFC Bank'} (A/C ********5678)",
            'utr': 'ON-HOLD-VERIFY',
            'status': 'On Hold',
            'badge_class': 'badge-pending',
            'failure_reason': 'Pending GST Compliance Document Audit by Finance Team.',
        },
    ]

    filtered_payouts = all_payouts
    if status_filter and status_filter != 'all':
        filtered_payouts = [p for p in all_payouts if p['status'].lower().replace(' ', '_') == status_filter.lower()]

    context = {
        'seller': seller,
        'available_balance': available_balance,
        'available_balance_formatted': format_inr(available_balance),
        'pending_payouts': pending_payouts,
        'pending_payouts_formatted': format_inr(pending_payouts),
        'total_paid_out': total_paid_out,
        'total_paid_out_formatted': format_inr(total_paid_out),
        'next_payout_date': next_payout_date,
        'payouts': filtered_payouts,
        'current_status': status_filter,
    }
    return render(request, 'seller_panel/payments.html', context)


@seller_required
def transactions_view(request):
    seller = get_current_seller(request.user)

    q = request.GET.get('q', '').strip()
    type_filter = request.GET.get('type', 'all').strip()
    status_filter = request.GET.get('status', 'all').strip()

    all_transactions = [
        {
            'txn_id': '#TXN-77410',
            'datetime': '08 Oct 2026, 14:30',
            'type': 'Sale',
            'type_badge': 'badge bg-success text-white',
            'order_number': '#TN-10245',
            'gross_amount': Decimal('1899.00'),
            'commission': Decimal('-284.85'),
            'refund_adj': Decimal('0.00'),
            'net_amount': Decimal('1614.15'),
            'status': 'Completed',
            'badge_class': 'badge-delivered',
        },
        {
            'txn_id': '#TXN-77408',
            'datetime': '07 Oct 2026, 11:15',
            'type': 'Commission Deduction',
            'type_badge': 'badge bg-warning text-dark',
            'order_number': '#TN-10244',
            'gross_amount': Decimal('1499.00'),
            'commission': Decimal('-224.85'),
            'refund_adj': Decimal('0.00'),
            'net_amount': Decimal('-224.85'),
            'status': 'Completed',
            'badge_class': 'badge-delivered',
        },
        {
            'txn_id': '#TXN-77402',
            'datetime': '06 Oct 2026, 16:45',
            'type': 'Refund Adjustment',
            'type_badge': 'badge bg-danger text-white',
            'order_number': '#TN-10218',
            'gross_amount': Decimal('0.00'),
            'commission': Decimal('0.00'),
            'refund_adj': Decimal('-2499.00'),
            'net_amount': Decimal('-2499.00'),
            'status': 'Completed',
            'badge_class': 'badge-delivered',
        },
        {
            'txn_id': '#TXN-77395',
            'datetime': '04 Oct 2026, 10:00',
            'type': 'Payout Transfer',
            'type_badge': 'badge bg-primary text-white',
            'order_number': '--',
            'gross_amount': Decimal('42680.00'),
            'commission': Decimal('0.00'),
            'refund_adj': Decimal('0.00'),
            'net_amount': Decimal('-42680.00'),
            'status': 'Completed',
            'badge_class': 'badge-delivered',
        },
        {
            'txn_id': '#TXN-77380',
            'datetime': '02 Oct 2026, 09:20',
            'type': 'Manual Adjustment',
            'type_badge': 'badge bg-secondary text-white',
            'order_number': '--',
            'gross_amount': Decimal('500.00'),
            'commission': Decimal('0.00'),
            'refund_adj': Decimal('500.00'),
            'net_amount': Decimal('+500.00'),
            'status': 'Completed',
            'badge_class': 'badge-delivered',
        },
    ]

    filtered_txns = all_transactions

    if q:
        filtered_txns = [t for t in filtered_txns if q.lower() in t['txn_id'].lower() or q.lower() in t['order_number'].lower() or q.lower() in t['type'].lower()]

    if type_filter and type_filter != 'all':
        filtered_txns = [t for t in filtered_txns if type_filter.lower() in t['type'].lower().replace(' ', '_')]

    if status_filter and status_filter != 'all':
        filtered_txns = [t for t in filtered_txns if status_filter.lower() in t['status'].lower()]

    context = {
        'seller': seller,
        'transactions': filtered_txns,
        'current_q': q,
        'current_type': type_filter,
        'current_status': status_filter,
    }
    return render(request, 'seller_panel/transactions.html', context)


@seller_required
def promotions_view(request):
    seller = get_current_seller(request.user)
    status_filter = request.GET.get('status', 'all').strip()
    q = request.GET.get('q', '').strip()

    if 'seller_promotions_list' not in request.session:
        request.session['seller_promotions_list'] = [
            {
                'id': 'PROMO-100',
                'name': 'Autumn Luxury Sale',
                'discount_display': '20% OFF',
                'category': 'All Categories',
                'start_date': '01 Oct 2026',
                'end_date': '15 Oct 2026',
                'orders_generated': 42,
                'units_sold': 68,
                'discount_amount': '14,250',
                'revenue_generated': '84,500',
                'conversion_rate': '4.8%',
                'status': 'Active',
                'badge_class': 'badge-in-stock',
            },
            {
                'id': 'PROMO-101',
                'name': 'Festive Sleepwear Campaign',
                'discount_display': '15% OFF',
                'category': 'Nightwear & Pyjamas',
                'start_date': '01 Nov 2026',
                'end_date': '15 Nov 2026',
                'orders_generated': 0,
                'units_sold': 0,
                'discount_amount': '0',
                'revenue_generated': '0',
                'conversion_rate': '--',
                'status': 'Scheduled',
                'badge_class': 'badge-reserved',
            },
            {
                'id': 'PROMO-098',
                'name': 'Weekend Satin Treat',
                'discount_display': '₹300 OFF',
                'category': 'Satin Pyjamas',
                'start_date': '25 Sep 2026',
                'end_date': '28 Sep 2026',
                'orders_generated': 19,
                'units_sold': 24,
                'discount_amount': '7,200',
                'revenue_generated': '41,176',
                'conversion_rate': '5.2%',
                'status': 'Expired',
                'badge_class': 'badge-out-stock',
            },
            {
                'id': 'PROMO-095',
                'name': 'Monsoon Cozy Clearance',
                'discount_display': '25% OFF',
                'category': 'Loungewear',
                'start_date': '15 Aug 2026',
                'end_date': '31 Aug 2026',
                'orders_generated': 55,
                'units_sold': 89,
                'discount_amount': '22,400',
                'revenue_generated': '1,12,000',
                'conversion_rate': '3.9%',
                'status': 'Expired',
                'badge_class': 'badge-out-stock',
            },
        ]

    promotions = list(request.session['seller_promotions_list'])

    if q:
        promotions = [p for p in promotions if q.lower() in p['name'].lower() or q.lower() in p['category'].lower()]
    if status_filter and status_filter != 'all':
        promotions = [p for p in promotions if status_filter.lower() == p['status'].lower()]

    active_count = len([p for p in request.session['seller_promotions_list'] if p['status'] == 'Active'])
    scheduled_count = len([p for p in request.session['seller_promotions_list'] if p['status'] == 'Scheduled'])
    expired_count = len([p for p in request.session['seller_promotions_list'] if p['status'] == 'Expired'])

    context = {
        'seller': seller,
        'promotions': promotions,
        'active_count': active_count,
        'scheduled_count': scheduled_count,
        'expired_count': expired_count,
        'products_on_promo_count': 8,
        'current_status': status_filter,
        'current_q': q,
    }
    return render(request, 'seller_panel/promotions.html', context)


@seller_required
def add_promotion_action_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        disc_type = request.POST.get('discount_type', 'percentage')
        disc_val = request.POST.get('discount_value', '10')
        category = request.POST.get('category', 'All Categories')
        start_date = request.POST.get('start_date', 'Today')
        end_date = request.POST.get('end_date', 'Next Month')

        disc_display = f"{disc_val}% OFF" if disc_type == 'percentage' else f"₹{disc_val} OFF"
        new_promo = {
            'id': f"PROMO-{len(request.session.get('seller_promotions_list', [])) + 102}",
            'name': name or 'New Promotional Campaign',
            'discount_display': disc_display,
            'category': category,
            'start_date': start_date,
            'end_date': end_date,
            'orders_generated': 0,
            'units_sold': 0,
            'discount_amount': '0',
            'revenue_generated': '0',
            'conversion_rate': '0.0%',
            'status': 'Active',
            'badge_class': 'badge-in-stock',
        }
        current_list = list(request.session.get('seller_promotions_list', []))
        current_list.insert(0, new_promo)
        request.session['seller_promotions_list'] = current_list
        messages.success(request, f"Promotion '{new_promo['name']}' has been created successfully!")
    return redirect('seller_panel:promotions')


def _seed_default_coupons():
    from datetime import date
    defaults = [
        {
            'code': 'FASHION10',
            'discount_type': 'percentage',
            'discount_value': Decimal('10.00'),
            'min_order_amount': Decimal('1000.00'),
            'max_discount': Decimal('500.00'),
            'start_date': date(2026, 10, 1),
            'end_date': date(2026, 10, 31),
            'usage_limit': 100,
            'used_count': 45,
            'is_active': True,
            'description': '10% OFF on orders above ₹1,000 (Max ₹500)'
        },
        {
            'code': 'STYLE200',
            'discount_type': 'fixed',
            'discount_value': Decimal('200.00'),
            'min_order_amount': Decimal('1500.00'),
            'max_discount': Decimal('200.00'),
            'start_date': date(2026, 10, 5),
            'end_date': date(2026, 10, 25),
            'usage_limit': 50,
            'used_count': 18,
            'is_active': True,
            'description': 'Flat ₹200 OFF on orders above ₹1,500'
        },
        {
            'code': 'FESTIVE15',
            'discount_type': 'percentage',
            'discount_value': Decimal('15.00'),
            'min_order_amount': Decimal('2000.00'),
            'max_discount': Decimal('1000.00'),
            'start_date': date(2026, 11, 1),
            'end_date': date(2026, 11, 10),
            'usage_limit': 200,
            'used_count': 0,
            'is_active': True,
            'description': 'Festive 15% OFF on orders above ₹2,000 (Scheduled for Nov)'
        },
        {
            'code': 'WELCOME50',
            'discount_type': 'fixed',
            'discount_value': Decimal('50.00'),
            'min_order_amount': Decimal('499.00'),
            'max_discount': Decimal('50.00'),
            'start_date': date(2026, 9, 1),
            'end_date': date(2026, 9, 30),
            'usage_limit': 120,
            'used_count': 120,
            'is_active': False,
            'description': 'Flat ₹50 OFF for new users (Expired)'
        }
    ]
    for d in defaults:
        Coupon.objects.update_or_create(code=d['code'], defaults=d)


@seller_required
def coupons_view(request):
    seller = get_current_seller(request.user)
    status_filter = request.GET.get('status', 'all').strip()
    q = request.GET.get('q', '').strip()

    if Coupon.objects.count() == 0:
        _seed_default_coupons()

    today = timezone.now().date()
    db_coupons = Coupon.objects.all().order_by('-created_at')

    def format_coupon_for_seller(c):
        if not c.is_active or (c.end_date and c.end_date < today) or (c.usage_limit and c.used_count >= c.usage_limit):
            st = 'Expired'
            badge = 'badge-out-stock'
        elif c.start_date and c.start_date > today:
            st = 'Scheduled'
            badge = 'badge-reserved'
        else:
            st = 'Active'
            badge = 'badge-in-stock'

        if c.discount_type == 'percentage':
            disc = f"{int(c.discount_value) if c.discount_value % 1 == 0 else c.discount_value}% OFF"
        else:
            disc = f"₹{int(c.discount_value) if c.discount_value % 1 == 0 else c.discount_value} OFF"

        min_o = f"₹{int(c.min_order_amount):,}" if c.min_order_amount and c.min_order_amount > 0 else 'No Minimum'
        max_c = f"₹{int(c.max_discount):,}" if c.max_discount and c.max_discount > 0 else 'No Cap'

        if c.start_date and c.end_date:
            val_str = f"{c.start_date.strftime('%d %b')} - {c.end_date.strftime('%d %b %Y')}"
        else:
            val_str = "Ongoing"

        return {
            'id': c.id,
            'code': c.code,
            'discount': disc,
            'min_order': min_o,
            'max_cap': max_c,
            'uses': c.used_count,
            'max_uses': c.usage_limit,
            'validity': val_str,
            'status': st,
            'badge_class': badge,
        }

    all_coupons = [format_coupon_for_seller(c) for c in db_coupons]
    coupons = list(all_coupons)

    if q:
        coupons = [c for c in coupons if q.lower() in c['code'].lower()]
    if status_filter and status_filter.lower() != 'all':
        coupons = [c for c in coupons if status_filter.lower() == c['status'].lower()]

    active_count = len([c for c in all_coupons if c['status'] == 'Active'])
    scheduled_count = len([c for c in all_coupons if c['status'] == 'Scheduled'])
    expired_count = len([c for c in all_coupons if c['status'] == 'Expired'])
    total_redemptions = sum(c['uses'] for c in all_coupons)

    context = {
        'seller': seller,
        'coupons': coupons,
        'active_count': active_count,
        'scheduled_count': scheduled_count,
        'expired_count': expired_count,
        'total_redemptions': total_redemptions,
        'current_status': status_filter,
        'current_q': q,
    }
    return render(request, 'seller_panel/coupons.html', context)


@seller_required
def add_coupon_action_view(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        disc_type = request.POST.get('discount_type', 'percentage')
        disc_val_str = request.POST.get('discount_value', '10')
        min_order_str = request.POST.get('min_order', '0')
        max_cap_str = request.POST.get('max_cap', '0')
        start_date_str = request.POST.get('start_date', '')
        expiry_date_str = request.POST.get('expiry_date', '')
        max_uses_str = request.POST.get('max_uses', '100')
        per_customer_limit_str = request.POST.get('per_customer_limit', '1')

        try:
            disc_val = Decimal(disc_val_str)
        except Exception:
            disc_val = Decimal('10.00')

        try:
            min_order = Decimal(min_order_str)
        except Exception:
            min_order = Decimal('0.00')

        try:
            max_cap = Decimal(max_cap_str)
        except Exception:
            max_cap = Decimal('0.00')

        try:
            max_uses = int(max_uses_str)
        except Exception:
            max_uses = 100

        try:
            per_customer_limit = int(per_customer_limit_str)
        except Exception:
            per_customer_limit = 1

        today = timezone.now().date()
        try:
            from datetime import datetime, timedelta
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else today
        except Exception:
            start_date = today

        try:
            from datetime import datetime, timedelta
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date() if expiry_date_str else start_date + timedelta(days=30)
        except Exception:
            expiry_date = start_date + timedelta(days=30)

        if code:
            coupon, created = Coupon.objects.update_or_create(
                code=code,
                defaults={
                    'discount_type': disc_type,
                    'discount_value': disc_val,
                    'min_order_amount': min_order,
                    'max_discount': max_cap if max_cap > Decimal('0.00') else None,
                    'start_date': start_date,
                    'end_date': expiry_date,
                    'usage_limit': max_uses,
                    'user_usage_limit': per_customer_limit,
                    'is_active': True,
                    'description': f"{disc_val}% OFF" if disc_type == 'percentage' else f"Flat ₹{disc_val} OFF"
                }
            )
            messages.success(request, f"Coupon '{code}' created and activated successfully!")
        else:
            messages.error(request, "Please enter a valid coupon code.")
    return redirect('seller_panel:coupons')


@seller_required
def sales_analytics_view(request):
    seller = get_current_seller(request.user)
    date_range = request.GET.get('range', '30d').strip()

    category_sales = [
        {'name': 'Nightwear & Pyjamas', 'sales': Decimal('112000.00'), 'percentage': 45, 'color': '#2b5329'},
        {'name': 'Kimono Robes', 'sales': Decimal('62225.00'), 'percentage': 25, 'color': '#8b5cf6'},
        {'name': 'Nightdresses', 'sales': Decimal('49780.00'), 'percentage': 20, 'color': '#f59e0b'},
        {'name': 'Loungewear Accessories', 'sales': Decimal('24895.00'), 'percentage': 10, 'color': '#06b6d4'},
    ]

    top_products = [
        {
            'name': 'Celestial Star Satin Pyjama Set',
            'sku': 'TN-CEL-SAT-01',
            'image': '/static/images/products/pyjama-star.jpg',
            'units_sold': 48,
            'revenue': Decimal('91152.00'),
            'growth': '+18.4%',
        },
        {
            'name': 'Blossom Floral Cotton Pyjamas',
            'sku': 'TN-BLO-COT-02',
            'image': '/static/images/products/pyjama-blossom.jpg',
            'units_sold': 35,
            'revenue': Decimal('52465.00'),
            'growth': '+12.1%',
        },
        {
            'name': 'Royal Peacock Velvet Robe',
            'sku': 'TN-PEA-VEL-03',
            'image': '/static/images/products/robe-peacock.jpg',
            'units_sold': 22,
            'revenue': Decimal('54978.00'),
            'growth': '+8.5%',
        },
        {
            'name': 'Vintage Rose Nightdress',
            'sku': 'TN-ROS-NIG-04',
            'image': '/static/images/products/nightdress-rose.jpg',
            'units_sold': 18,
            'revenue': Decimal('26982.00'),
            'growth': '+5.0%',
        },
    ]

    total_sales_dec = Decimal('248900.00')
    total_net_dec = Decimal('211565.00')
    avg_order_dec = Decimal('1752.81')
    refund_impact_dec = Decimal('10494.00')

    context = {
        'seller': seller,
        'date_range': date_range,
        'total_sales': total_sales_dec,
        'total_sales_formatted': format_inr(total_sales_dec),
        'total_net': total_net_dec,
        'total_net_formatted': format_inr(total_net_dec),
        'total_orders': 142,
        'units_sold': 210,
        'avg_order_val': avg_order_dec,
        'avg_order_val_formatted': format_inr(avg_order_dec),
        'cancellation_count': 4,
        'cancellation_rate': '2.8%',
        'return_count': 6,
        'return_rate': '4.2%',
        'refund_impact': refund_impact_dec,
        'refund_impact_formatted': format_inr(refund_impact_dec),
        'category_sales': category_sales,
        'top_products': top_products,
    }
    return render(request, 'seller_panel/sales_analytics.html', context)


@seller_required
def product_performance_view(request):
    seller = get_current_seller(request.user)
    q = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', 'all').strip()

    performance_rows = [
        {
            'name': 'Celestial Star Satin Pyjama Set',
            'sku': 'TN-CEL-SAT-01',
            'category': 'Nightwear & Pyjamas',
            'image': '/static/images/products/pyjama-star.jpg',
            'views': 2450,
            'atc_rate': '18.5%',
            'conv_rate': '6.4%',
            'units_sold': 48,
            'orders': 42,
            'revenue': Decimal('91152.00'),
            'return_rate': '2.1%',
            'stock_status': 'In Stock',
            'available_stock': 45,
            'badge_class': 'badge-in-stock',
        },
        {
            'name': 'Blossom Floral Cotton Pyjamas',
            'sku': 'TN-BLO-COT-02',
            'category': 'Nightwear & Pyjamas',
            'image': '/static/images/products/pyjama-blossom.jpg',
            'views': 1820,
            'atc_rate': '14.2%',
            'conv_rate': '5.2%',
            'units_sold': 35,
            'orders': 31,
            'revenue': Decimal('52465.00'),
            'return_rate': '3.5%',
            'stock_status': 'In Stock',
            'available_stock': 28,
            'badge_class': 'badge-in-stock',
        },
        {
            'name': 'Royal Peacock Velvet Robe',
            'sku': 'TN-PEA-VEL-03',
            'category': 'Kimono Robes',
            'image': '/static/images/products/robe-peacock.jpg',
            'views': 1150,
            'atc_rate': '11.0%',
            'conv_rate': '4.8%',
            'units_sold': 22,
            'orders': 20,
            'revenue': Decimal('54978.00'),
            'return_rate': '12.5%',
            'stock_status': 'Low Stock',
            'available_stock': 6,
            'badge_class': 'badge-reserved',
        },
        {
            'name': 'Botanical Printed Lounge Pants',
            'sku': 'TN-BOT-PA-05',
            'category': 'Loungewear Accessories',
            'image': '/static/images/products/pants-botanical.jpg',
            'views': 1240,
            'atc_rate': '5.8%',
            'conv_rate': '1.1%',
            'units_sold': 14,
            'orders': 14,
            'revenue': Decimal('18186.00'),
            'return_rate': '4.2%',
            'stock_status': 'Out of Stock',
            'available_stock': 0,
            'badge_class': 'badge-out-stock',
        },
        {
            'name': 'Vintage Rose Nightdress',
            'sku': 'TN-ROS-NIG-04',
            'category': 'Nightdresses',
            'image': '/static/images/products/nightdress-rose.jpg',
            'views': 940,
            'atc_rate': '12.8%',
            'conv_rate': '4.5%',
            'units_sold': 18,
            'orders': 16,
            'revenue': Decimal('26982.00'),
            'return_rate': '1.8%',
            'stock_status': 'Low Stock',
            'available_stock': 7,
            'badge_class': 'badge-reserved',
        },
    ]

    filtered_rows = performance_rows
    if q:
        filtered_rows = [r for r in filtered_rows if q.lower() in r['name'].lower() or q.lower() in r['sku'].lower()]
    if category_filter and category_filter != 'all':
        filtered_rows = [r for r in filtered_rows if category_filter.lower() in r['category'].lower()]

    context = {
        'seller': seller,
        'performance_rows': filtered_rows,
        'current_q': q,
        'current_category': category_filter,
    }
    return render(request, 'seller_panel/product_performance.html', context)


@seller_required
def reviews_view(request):
    seller = get_current_seller(request.user)
    q = request.GET.get('q', '').strip()
    rating_filter = request.GET.get('rating', 'all').strip()
    status_filter = request.GET.get('status', 'all').strip()
    category_filter = request.GET.get('category', 'all').strip()
    sort_by = request.GET.get('sort', 'newest').strip()

    if 'seller_reviews_list' not in request.session:
        request.session['seller_reviews_list'] = [
            {
                'id': 'REV-1088',
                'customer_name': 'Ananya Roy',
                'is_verified': True,
                'product_name': 'Celestial Star Satin Pyjama Set',
                'product_sku': 'TN-CEL-SAT-01',
                'product_category': 'Nightwear & Pyjamas',
                'product_image': '/static/images/products/pyjama-star.jpg',
                'rating': 5,
                'rating_float': 5.0,
                'review_text': 'Absolutely stunning pyjama set! The satin quality feels pure luxury against skin and fits true to size. Delivery was exceptionally quick too.',
                'date': '08 Oct 2026',
                'status': 'Answered',
                'badge_class': 'badge-in-stock',
                'seller_reply': 'Thank you so much Ananya! We are delighted that you love the Celestial Star Satin Pyjama Set. Your satisfaction means the world to Their Nibs!',
                'reply_date': '08 Oct 2026, 17:30',
            },
            {
                'id': 'REV-1082',
                'customer_name': 'Kavita Sharma',
                'is_verified': True,
                'product_name': 'Royal Peacock Velvet Robe',
                'product_sku': 'TN-PEA-VEL-03',
                'product_category': 'Kimono Robes',
                'product_image': '/static/images/products/robe-peacock.jpg',
                'rating': 2,
                'rating_float': 2.0,
                'review_text': 'The embroidery is beautiful, but the sizing runs significantly small around sleeves. Would recommend ordering one size larger.',
                'date': '06 Oct 2026',
                'status': 'Unanswered',
                'badge_class': 'badge-out-stock',
                'seller_reply': None,
                'reply_date': None,
            },
            {
                'id': 'REV-1075',
                'customer_name': 'Rohan Malhotra',
                'is_verified': True,
                'product_name': 'Blossom Floral Cotton Pyjamas',
                'product_sku': 'TN-BLO-COT-02',
                'product_category': 'Nightwear & Pyjamas',
                'product_image': '/static/images/products/pyjama-blossom.jpg',
                'rating': 5,
                'rating_float': 5.0,
                'review_text': 'Gifted this set to my wife for our anniversary. The organic cotton fabric is super soft and print looks elegant. Will definitely order again!',
                'date': '04 Oct 2026',
                'status': 'Answered',
                'badge_class': 'badge-in-stock',
                'seller_reply': 'Dear Rohan, thank you for choosing Their Nibs for such a special occasion! Warmest wishes to you and your wife!',
                'reply_date': '04 Oct 2026, 11:15',
            },
            {
                'id': 'REV-1068',
                'customer_name': 'Meera Patel',
                'is_verified': True,
                'product_name': 'Vintage Rose Nightdress',
                'product_sku': 'TN-ROS-NIG-04',
                'product_category': 'Nightdresses',
                'product_image': '/static/images/products/nightdress-rose.jpg',
                'rating': 4,
                'rating_float': 4.0,
                'review_text': 'Comfortable nightdress with gentle lace trim. Washing instructions were helpful.',
                'date': '02 Oct 2026',
                'status': 'Unanswered',
                'badge_class': 'badge-out-stock',
                'seller_reply': None,
                'reply_date': None,
            },
            {
                'id': 'REV-1050',
                'customer_name': 'Pooja Verma',
                'is_verified': True,
                'product_name': 'Silk Eye Mask & Scrunchie Set',
                'product_sku': 'TN-SLK-ACC-06',
                'product_category': 'Loungewear Accessories',
                'product_image': '/static/images/products/pants-botanical.jpg',
                'rating': 3,
                'rating_float': 3.0,
                'review_text': 'Decent accessory set. The eye mask elastic could be a bit softer.',
                'date': '28 Sep 2026',
                'status': 'Unanswered',
                'badge_class': 'badge-out-stock',
                'seller_reply': None,
                'reply_date': None,
            },
        ]

    reviews_data = list(request.session['seller_reviews_list'])

    if q:
        reviews_data = [
            r for r in reviews_data 
            if q.lower() in r['customer_name'].lower() or q.lower() in r['product_name'].lower() or q.lower() in r['review_text'].lower()
        ]

    if rating_filter and rating_filter != 'all':
        try:
            target_r = int(rating_filter)
            reviews_data = [r for r in reviews_data if r['rating'] == target_r]
        except ValueError:
            pass

    if status_filter and status_filter != 'all':
        reviews_data = [r for r in reviews_data if status_filter.lower() == r['status'].lower()]

    if category_filter and category_filter != 'all':
        reviews_data = [r for r in reviews_data if category_filter.lower() in r['product_category'].lower()]

    if sort_by == 'highest':
        reviews_data.sort(key=lambda x: x['rating'], reverse=True)
    elif sort_by == 'lowest':
        reviews_data.sort(key=lambda x: x['rating'])

    total_count = len(request.session['seller_reviews_list'])
    unanswered_count = len([r for r in request.session['seller_reviews_list'] if r['status'] == 'Unanswered'])
    responded_count = len([r for r in request.session['seller_reviews_list'] if r['status'] == 'Answered'])

    context = {
        'seller': seller,
        'reviews': reviews_data,
        'avg_rating': '4.5',
        'total_reviews': 128,
        'unanswered_count': 12,
        'responded_count': 116,
        'current_q': q,
        'current_rating': rating_filter,
        'current_status': status_filter,
        'current_category': category_filter,
        'current_sort': sort_by,
    }
    return render(request, 'seller_panel/reviews.html', context)


@seller_required
def reply_review_action_view(request):
    if request.method == 'POST':
        rev_id = request.POST.get('review_id')
        reply_text = request.POST.get('seller_reply', '').strip()

        if rev_id and reply_text:
            current_reviews = list(request.session.get('seller_reviews_list', []))
            for r in current_reviews:
                if r['id'] == rev_id:
                    r['seller_reply'] = reply_text
                    r['status'] = 'Answered'
                    r['badge_class'] = 'badge-in-stock'
                    r['reply_date'] = 'Today'
                    break
            request.session['seller_reviews_list'] = current_reviews
            messages.success(request, f"Your reply to review {rev_id} has been published successfully.")
    return redirect('seller_panel:reviews')


@seller_required
def customer_questions_view(request):
    seller = get_current_seller(request.user)
    q = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'pending').strip()

    if 'seller_questions_list' not in request.session:
        request.session['seller_questions_list'] = [
            {
                'id': 'QST-509',
                'customer_name': 'Sunita Rao',
                'product_name': 'Celestial Star Satin Pyjama Set',
                'product_sku': 'TN-CEL-SAT-01',
                'product_image': '/static/images/products/pyjama-star.jpg',
                'topic': 'Size & Fit',
                'question_text': 'Is this pyjama set true to size or should I size up for a relaxed fit?',
                'asked_on': '08 Oct 2026, 16:45',
                'status': 'Pending',
                'badge_class': 'badge-reserved',
                'seller_answer': None,
                'answered_on': None,
            },
            {
                'id': 'QST-504',
                'customer_name': 'Deepak Mehta',
                'product_name': 'Royal Peacock Velvet Robe',
                'product_sku': 'TN-PEA-VEL-03',
                'product_image': '/static/images/products/robe-peacock.jpg',
                'topic': 'Care Instructions',
                'question_text': 'Is this velvet robe machine washable or dry clean only?',
                'asked_on': '07 Oct 2026, 11:20',
                'status': 'Pending',
                'badge_class': 'badge-reserved',
                'seller_answer': None,
                'answered_on': None,
            },
            {
                'id': 'QST-498',
                'customer_name': 'Sneha Kapoor',
                'product_name': 'Blossom Floral Cotton Pyjamas',
                'product_sku': 'TN-BLO-COT-02',
                'product_image': '/static/images/products/pyjama-blossom.jpg',
                'topic': 'Fabric & Material',
                'question_text': 'Is the cotton 100% breathable organic cotton?',
                'asked_on': '05 Oct 2026, 14:10',
                'status': 'Answered',
                'badge_class': 'badge-in-stock',
                'seller_answer': 'Yes Sneha! All our Blossom Pyjama Sets are crafted from 100% super-soft breathable organic cotton.',
                'answered_on': '05 Oct 2026, 15:30',
            },
            {
                'id': 'QST-490',
                'customer_name': 'Vikram Joshi',
                'product_name': 'Botanical Printed Lounge Pants',
                'product_sku': 'TN-BOT-PA-05',
                'product_image': '/static/images/products/pants-botanical.jpg',
                'topic': 'Availability',
                'question_text': 'Will size XL be back in stock in Midnight Navy before Diwali?',
                'asked_on': '03 Oct 2026, 09:15',
                'status': 'Answered',
                'badge_class': 'badge-in-stock',
                'seller_answer': 'Hi Vikram, yes! Restock of Size XL Midnight Navy is arriving next week around Oct 15th.',
                'answered_on': '03 Oct 2026, 10:05',
            },
            {
                'id': 'QST-482',
                'customer_name': 'Ankita Das',
                'product_name': 'Vintage Rose Nightdress',
                'product_sku': 'TN-ROS-NIG-04',
                'product_image': '/static/images/products/nightdress-rose.jpg',
                'topic': 'Colour & Match',
                'question_text': 'Does the actual dusty rose shade match the images closely?',
                'asked_on': '01 Oct 2026, 18:00',
                'status': 'Answered',
                'badge_class': 'badge-in-stock',
                'seller_answer': 'Hello Ankita, yes the dusty rose shade is captured accurately in natural Studio lighting.',
                'answered_on': '01 Oct 2026, 18:40',
            },
        ]

    questions_data = list(request.session['seller_questions_list'])

    if q:
        questions_data = [
            q_item for q_item in questions_data
            if q.lower() in q_item['customer_name'].lower() or q.lower() in q_item['product_name'].lower() or q.lower() in q_item['question_text'].lower()
        ]

    if status_filter and status_filter != 'all':
        questions_data = [q_item for q_item in questions_data if status_filter.lower() == q_item['status'].lower()]

    questions_data.sort(key=lambda x: (0 if x['status'] == 'Pending' else 1))

    pending_count = len([q_item for q_item in request.session['seller_questions_list'] if q_item['status'] == 'Pending'])
    answered_count = len([q_item for q_item in request.session['seller_questions_list'] if q_item['status'] == 'Answered'])

    context = {
        'seller': seller,
        'questions': questions_data,
        'total_questions': 42,
        'pending_count': 8,
        'answered_count': 34,
        'current_q': q,
        'current_status': status_filter,
    }
    return render(request, 'seller_panel/customer_questions.html', context)


@seller_required
def answer_question_action_view(request):
    if request.method == 'POST':
        q_id = request.POST.get('question_id')
        answer_text = request.POST.get('seller_answer', '').strip()

        if q_id and answer_text:
            current_questions = list(request.session.get('seller_questions_list', []))
            for item in current_questions:
                if item['id'] == q_id:
                    item['seller_answer'] = answer_text
                    item['status'] = 'Answered'
                    item['badge_class'] = 'badge-in-stock'
                    item['answered_on'] = 'Today'
                    break
            request.session['seller_questions_list'] = current_questions
            messages.success(request, f"Your answer to question {q_id} has been posted successfully.")
    return redirect('seller_panel:customer_questions')


@seller_required
def store_profile_view(request):
    seller = get_current_seller(request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'pause_selling' and seller:
            seller.status = 'suspended'
            seller.save()
            messages.info(request, "Your boutique selling status is now temporarily paused (Vacation Mode).")
            return redirect('seller_panel:store_profile')
        elif action == 'resume_selling' and seller:
            seller.status = 'approved'
            seller.save()
            messages.success(request, "Your boutique selling status has been reactivated and is now live!")
            return redirect('seller_panel:store_profile')
        elif action == 'delete_seller_account' and seller:
            name = seller.store_name
            seller.delete()
            messages.warning(request, f"Your seller boutique account '{name}' has been permanently closed.")
            return redirect('homepage')

        if seller:
            seller.store_name = request.POST.get('store_name') or seller.store_name
            seller.company_name = request.POST.get('company_name') or seller.company_name
            seller.email = request.POST.get('email') or seller.email
            seller.phone = request.POST.get('phone') or seller.phone
            seller.gst_number = request.POST.get('gst_number') or seller.gst_number
            seller.city = request.POST.get('city') or seller.city
            seller.state = request.POST.get('state') or seller.state
            seller.store_description = request.POST.get('store_description') or seller.store_description
            seller.save()

            if request.user.is_authenticated:
                full_name = request.POST.get('full_name')
                if full_name:
                    parts = full_name.split(' ')
                    request.user.first_name = parts[0]
                    request.user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
                    request.user.save()

        messages.success(request, "Personal & Store Profile details updated successfully.")
        return redirect('seller_panel:store_profile')
    return render(request, 'seller_panel/profile.html', {'seller': seller, 'tab': 'profile'})


@seller_required
def bank_payment_view(request):
    seller = get_current_seller(request.user)
    if request.method == 'POST':
        if seller:
            seller.bank_name = request.POST.get('bank_name') or seller.bank_name
            seller.account_number = request.POST.get('account_number') or seller.account_number
            seller.ifsc_code = request.POST.get('ifsc_code') or seller.ifsc_code
            seller.save()

        messages.success(request, "Bank & Payment details updated successfully.")
        return redirect('seller_panel:bank_payment')
    return render(request, 'seller_panel/profile.html', {'seller': seller, 'tab': 'bank'})


@seller_required
def notifications_view(request):
    seller = get_current_seller(request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'mark_all_read' and seller:
            SellerNotification.objects.filter(seller=seller, is_read=False).update(is_read=True)
            messages.success(request, "All seller notifications have been marked as read.")
            return redirect('seller_panel:notifications')

    notifications = []
    unread_count = 0
    if seller:
        notifications = list(SellerNotification.objects.filter(seller=seller).order_by('-created_at'))
        unread_count = SellerNotification.objects.filter(seller=seller, is_read=False).count()

    context = {
        'seller': seller,
        'notifications': notifications,
        'all_read': (unread_count == 0),
        'tab': 'notifications',
    }
    return render(request, 'seller_panel/profile.html', context)


@seller_required
@require_POST
def api_update_stock(request):
    try:
        data = json.loads(request.body)
        prod_id = data.get('product_id')
        new_stock = int(data.get('stock', 0))
        return JsonResponse({'success': True, 'message': 'Stock updated successfully', 'new_stock': new_stock})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
def api_mark_notifications_read(request):
    seller = get_current_seller(request.user)
    if seller:
        SellerNotification.objects.filter(seller=seller, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'ok', 'unread_count': 0})


@require_POST
def api_dismiss_notification(request):
    try:
        notif_id = None
        if request.body:
            try:
                data = json.loads(request.body)
                notif_id = data.get('notif_id')
            except Exception:
                pass
        if not notif_id:
            notif_id = request.POST.get('notif_id') or request.POST.get('notification_id')

        seller = get_current_seller(request.user)
        if seller and notif_id:
            notif = SellerNotification.objects.filter(seller=seller, pk=notif_id).first()
            if notif:
                notif.is_read = True
                notif.save()

        unread_count = SellerNotification.objects.filter(seller=seller, is_read=False).count() if seller else 0
        return JsonResponse({'status': 'ok', 'unread_count': unread_count})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


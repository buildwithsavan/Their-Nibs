import os, django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theirnibs.settings')
django.setup()

from admin_panel.models import Product, Category, Subcategory, Brand, Seller

brand = Brand.objects.first()
seller = Seller.objects.first()

cat_womens, _ = Category.objects.get_or_create(slug='womens', defaults={'name': 'Womens', 'description': 'Womens Nightwear & Pyjamas'})
cat_mens, _ = Category.objects.get_or_create(slug='mens', defaults={'name': 'Mens', 'description': 'Mens Pyjamas'})

sub_trad, _ = Subcategory.objects.get_or_create(slug='traditional-long-pyjamas', defaults={'name': 'Traditional Long Pyjamas', 'category': cat_womens})
sub_nightshirt, _ = Subcategory.objects.get_or_create(slug='nightdresses-shirts', defaults={'name': 'Nightdresses & Shirts', 'category': cat_womens})
sub_mens_pj, _ = Subcategory.objects.get_or_create(slug='mens-pyjamas', defaults={'name': 'Mens Pyjamas', 'category': cat_mens})

print("Adding/Updating Nightwear products...")

p1, created1 = Product.objects.update_or_create(
    slug='womens-monochrome-gingham-cotton-pyjama-set',
    defaults={
        'name': "Women's Monochrome Gingham Cotton Pyjama Set",
        'sku': 'TN-WOM-GM-01',
        'price': Decimal('42.00'),
        'gender': 'women',
        'category': cat_womens,
        'subcategory': sub_trad,
        'brand': brand,
        'seller': seller,
        'image_url': '/static/images/products/womens-black-white-gingham-pyjama-set.jpg',
        'stock': 12,
        'size': 'XS, S, M, L, XL',
        'material': 'Cotton',
        'color': 'Black',
        'tags': 'New In, Nightwear, Gingham, Cotton, Pyjamas, Traditional Long Pyjamas',
        'status': 'active',
        'is_featured': True,
        'description': 'Crafted from our signature ultra-soft brushed cotton flannel, this monochrome black and white gingham pyjama set features a tailored revere collar, front chest pocket, button-down front, and relaxed comfortable trousers.'
    }
)
print(f"Product 1: {p1.name} (Created: {created1}, Image: {p1.image_url})")

p2, created2 = Product.objects.update_or_create(
    slug='womens-pink-harlequin-check-frill-nightshirt',
    defaults={
        'name': "Women's Pink Harlequin Check Frill Nightshirt",
        'sku': 'TN-WOM-HL-02',
        'price': Decimal('38.00'),
        'gender': 'women',
        'category': cat_womens,
        'subcategory': sub_nightshirt,
        'brand': brand,
        'seller': seller,
        'image_url': '/static/images/products/womens-pink-harlequin-check-frill-nightshirt.jpg',
        'stock': 10,
        'size': 'XS, S, M, L',
        'material': 'Cotton',
        'color': 'Pink',
        'tags': 'New In, Nightwear, Nightdresses & Shirts, Harlequin, Check, Cotton',
        'status': 'active',
        'is_featured': True,
        'description': 'Delightfully charming and cosy, our pink and ruby red harlequin check nightshirt features a vintage-inspired ruffled Peter Pan collar, buttoned placket, and gently elasticated ruffle cuffs tailored from pure breathable cotton.'
    }
)
print(f"Product 2: {p2.name} (Created: {created2}, Image: {p2.image_url})")

p3 = Product.objects.filter(slug='mens-tartan-cosy-claus-brushed-cotton-pyjama-set').first()
if p3:
    p3.image_url = '/static/images/products/mens-tartan-cosy-claus-highres.jpg'
    current_tags = p3.tags or ''
    if 'Nightwear' not in current_tags:
        p3.tags = current_tags + ', Nightwear'
    p3.save()
    print(f"Updated Men's Tartan Cosy Claus: {p3.image_url}")
else:
    print("Warning: mens-tartan-cosy-claus-brushed-cotton-pyjama-set not found")

p4 = Product.objects.filter(slug='mens-cotton-traditional-pyjamas-navy-peacock').first()
if p4:
    p4.image_url = '/static/images/products/mens-navy-peacock-satin-highres.jpg'
    current_tags = p4.tags or ''
    if 'Nightwear' not in current_tags:
        p4.tags = current_tags + ', Nightwear'
    p4.save()
    print(f"Updated Men's Navy Peacock: {p4.image_url}")
else:
    print("Warning: mens-cotton-traditional-pyjamas-navy-peacock not found")

print("All Nightwear and Men's products updated successfully!")

import os, django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theirnibs.settings')
django.setup()

from admin_panel.models import Product, Category, Subcategory, Brand, Seller

brand = Brand.objects.first()
seller = Seller.objects.first()

cat_acc = Category.objects.get(slug='accessories')
sub_eyemask = Subcategory.objects.get(slug='eye-masks')
sub_shower = Subcategory.objects.get(slug='shower-caps')
sub_scrunchies = Subcategory.objects.get(slug='scrunchies')

print("Adding and updating Accessories products...")

em1, c1 = Product.objects.update_or_create(
    slug='green-peacock-feather-satin-eye-mask',
    defaults={
        'name': "Green Peacock Feather Satin Eye Mask",
        'sku': 'TN-ACC-MASK-10',
        'price': Decimal('16.00'),
        'gender': 'women',
        'category': cat_acc,
        'subcategory': sub_eyemask,
        'brand': brand,
        'seller': seller,
        'image_url': '/static/images/products/satin-frill-eye-mask-green-peacock.jpg',
        'stock': 15,
        'size': 'One Size',
        'material': 'Satin',
        'color': 'Green',
        'tags': 'Accessories, Eye Masks, Peacock, Satin, New In',
        'status': 'active',
        'is_featured': True,
        'description': 'Luxuriously padded satin sleep eye mask with delicate ruffle trim and emerald green peacock feather print for a restful, dreamy slumber.'
    }
)
print(f"Eye Mask 1: {em1.name} (Created: {c1})")

em2, c2 = Product.objects.update_or_create(
    slug='dusky-mauve-stripe-silk-sleep-eye-mask',
    defaults={
        'name': "Dusky Mauve Stripe Silk Sleep Eye Mask",
        'sku': 'TN-ACC-MASK-11',
        'price': Decimal('18.00'),
        'gender': 'women',
        'category': cat_acc,
        'subcategory': sub_eyemask,
        'brand': brand,
        'seller': seller,
        'image_url': '/static/images/products/dusky-mauve-stripe-silk-eye-mask.jpg',
        'stock': 12,
        'size': 'One Size',
        'material': 'Silk',
        'color': 'Mauve',
        'tags': 'Accessories, Eye Masks, Silk, Stripe, Dusky Mauve, New In',
        'status': 'active',
        'is_featured': True,
        'description': 'Crafted from 100% mulberry silk in our bestselling dusky mauve stripe pattern, this cushioned eye mask gently blocks out light while protecting delicate facial skin.'
    }
)
print(f"Eye Mask 2: {em2.name} (Created: {c2})")

sc1, c3 = Product.objects.update_or_create(
    slug='retro-geometric-silk-hair-scarf-scrunchie-set',
    defaults={
        'name': "Retro Geometric Silk Hair Scarf & Scrunchie Set",
        'sku': 'TN-ACC-SCRUNCH-12',
        'price': Decimal('18.00'),
        'gender': 'women',
        'category': cat_acc,
        'subcategory': sub_scrunchies,
        'brand': brand,
        'seller': seller,
        'image_url': '/static/images/products/retro-geo-silk-scarf-scrunchie.jpg',
        'stock': 14,
        'size': 'One Size',
        'material': 'Silk',
        'color': 'Pink',
        'tags': 'Accessories, Scrunchies, Silk, Scarf, Retro Geometric, New In',
        'status': 'active',
        'is_featured': True,
        'description': 'Versatile vintage-inspired silk hair wrap scarf and matching scrunchie set in our retro striped border print, designed to protect hair from breakage while lounging in luxury.'
    }
)
print(f"Scrunchies: {sc1.name} (Created: {c3})")

sh1 = Product.objects.filter(slug='boutique-satin-waterproof-shower-cap').first()
if sh1:
    sh1.name = "Celestial Star Satin Waterproof Shower Cap"
    sh1.image_url = '/static/images/products/luxury-shower-cap-celestial-navy.jpg'
    sh1.tags = 'Accessories, Shower Caps, Celestial, Star, Satin, Waterproof, New In'
    sh1.description = 'Keep your hair effortlessly dry and styled with our luxury double-lined waterproof shower cap in midnight navy celestial star print with delicate ruffle trim.'
    sh1.save()
    print(f"Shower Cap 1 (Updated): {sh1.name}")
else:
    sh1 = Product.objects.create(
        name="Celestial Star Satin Waterproof Shower Cap",
        slug='boutique-satin-waterproof-shower-cap',
        sku='TN-ACC-CAP-07',
        price=Decimal('14.00'),
        gender='women',
        category=cat_acc,
        subcategory=sub_shower,
        brand=brand,
        seller=seller,
        image_url='/static/images/products/luxury-shower-cap-celestial-navy.jpg',
        stock=14,
        size='One Size',
        material='Satin',
        color='Navy',
        tags='Accessories, Shower Caps, Celestial, Star, Satin, Waterproof, New In',
        status='active',
        is_featured=True,
        description='Keep your hair effortlessly dry and styled with our luxury double-lined waterproof shower cap in midnight navy celestial star print with delicate ruffle trim.'
    )
    print(f"Shower Cap 1 (Created): {sh1.name}")

sh2, c5 = Product.objects.update_or_create(
    slug='teal-peacock-feather-luxury-shower-cap',
    defaults={
        'name': "Teal Peacock Feather Luxury Shower Cap",
        'sku': 'TN-ACC-CAP-08',
        'price': Decimal('14.00'),
        'gender': 'women',
        'category': cat_acc,
        'subcategory': sub_shower,
        'brand': brand,
        'seller': seller,
        'image_url': '/static/images/products/luxury-shower-cap-peacock-teal.jpg',
        'stock': 12,
        'size': 'One Size',
        'material': 'Satin',
        'color': 'Teal',
        'tags': 'Accessories, Shower Caps, Peacock, Satin, Waterproof, New In',
        'status': 'active',
        'is_featured': True,
        'description': 'Vibrant teal and royal blue peacock feather waterproof shower cap featuring our signature Their Nibs label and ruffled elasticated hem.'
    }
)
print(f"Shower Cap 2: {sh2.name} (Created: {c5})")

sh3, c6 = Product.objects.update_or_create(
    slug='vintage-floral-double-lined-shower-cap',
    defaults={
        'name': "Vintage Floral Double-Lined Shower Cap",
        'sku': 'TN-ACC-CAP-09',
        'price': Decimal('14.00'),
        'gender': 'women',
        'category': cat_acc,
        'subcategory': sub_shower,
        'brand': brand,
        'seller': seller,
        'image_url': '/static/images/products/luxury-shower-cap-vintage-floral.jpg',
        'stock': 10,
        'size': 'One Size',
        'material': 'Satin',
        'color': 'Pink',
        'tags': 'Accessories, Shower Caps, Floral, Vintage, Waterproof, New In',
        'status': 'active',
        'is_featured': True,
        'description': 'Soft blush pink English garden floral waterproof shower cap with comfortable elasticated ruffle trim, perfect for elevated bath-time rituals.'
    }
)
print(f"Shower Cap 3: {sh3.name} (Created: {c6})")

print("All accessories products added/updated successfully!")

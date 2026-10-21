import os, django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theirnibs.settings')
django.setup()

from admin_panel.models import Product, Category, Subcategory, Brand, Seller

brand = Brand.objects.first()
seller = Seller.objects.first()


cat_kids, _ = Category.objects.get_or_create(name='Kids', defaults={'slug': 'kids', 'description': 'Kids and Tweens Pyjamas'})
cat_mens, _ = Category.objects.get_or_create(name='Mens', defaults={'slug': 'mens', 'description': 'Mens Pyjamas & Loungewear'})
cat_acc, _ = Category.objects.get_or_create(name='Accessories', defaults={'slug': 'accessories', 'description': 'Luxury Accessories'})
cat_gift, _ = Category.objects.get_or_create(name='Gifting', defaults={'slug': 'gifting', 'description': 'Curated Gifts'})


sub_kids_pj, _ = Subcategory.objects.get_or_create(name='Kids Pyjamas', category=cat_kids, defaults={'slug': 'kids-pyjamas'})
sub_tween, _ = Subcategory.objects.get_or_create(name='Tween Pyjamas & Nightwear', category=cat_kids, defaults={'slug': 'tween-pyjamas'})
sub_family, _ = Subcategory.objects.get_or_create(name='Matching Family Pyjamas', category=cat_kids, defaults={'slug': 'matching-family'})
sub_all_kids, _ = Subcategory.objects.get_or_create(name='All Kids & Tweens', category=cat_kids, defaults={'slug': 'all-kids-tweens'})

sub_mens_pj, _ = Subcategory.objects.get_or_create(name='Mens Pyjamas', category=cat_mens, defaults={'slug': 'mens-pyjamas'})
sub_mens_fam, _ = Subcategory.objects.get_or_create(name='Matching Family Pyjamas', category=cat_mens, defaults={'slug': 'mens-matching-family'})

sub_makeup, _ = Subcategory.objects.get_or_create(name='Make-up Bags', category=cat_acc, defaults={'slug': 'makeup-bags'})
sub_eyemask, _ = Subcategory.objects.get_or_create(name='Eye Masks', category=cat_acc, defaults={'slug': 'eye-masks'})
sub_shower, _ = Subcategory.objects.get_or_create(name='Shower Caps', category=cat_acc, defaults={'slug': 'shower-caps'})
sub_scrunchies, _ = Subcategory.objects.get_or_create(name='Scrunchies', category=cat_acc, defaults={'slug': 'scrunchies'})

sub_her, _ = Subcategory.objects.get_or_create(name='Gifts For Her', category=cat_gift, defaults={'slug': 'gifts-for-her'})
sub_him, _ = Subcategory.objects.get_or_create(name='Gifts For Him', category=cat_gift, defaults={'slug': 'gifts-for-him'})
sub_gkids, _ = Subcategory.objects.get_or_create(name='Gifts For Kids', category=cat_gift, defaults={'slug': 'gifts-for-kids'})
sub_voucher, _ = Subcategory.objects.get_or_create(name='E-Gift Card', category=cat_gift, defaults={'slug': 'gift-cards'})

products_data = [
    {
        'name': 'Kids Midnight Whiskers Traditional Pyjama Set',
        'slug': 'kids-midnight-whiskers-traditional-pyjama-set',
        'sku': 'TN-KID-WHISK-01',
        'price': Decimal('32.00'),
        'gender': 'kids',
        'category': cat_kids,
        'subcategory': sub_kids_pj,
        'image_url': '/static/images/products/touch-tween-whiskers.png',
        'stock': 8,
        'size': 'XS, S, M, L, XL',
        'material': 'Satin',
        'tags': 'New In, Kids, Whiskers, Pyjamas',
        'description': 'Designed for sweet dreams, our kids midnight whiskers pyjama set features a relaxed button-front shirt with contrast piping and soft elasticated trousers.'
    },
    {
        'name': 'Kids Autumn Woodland Berries Cotton Pyjamas',
        'slug': 'kids-autumn-woodland-berries-cotton-pyjamas',
        'sku': 'TN-KID-BERRY-02',
        'price': Decimal('28.00'),
        'gender': 'kids',
        'category': cat_kids,
        'subcategory': sub_kids_pj,
        'image_url': '/static/images/products/womens-woodland-berries.png',
        'stock': 6,
        'size': 'XS, S, M, L',
        'material': 'Cotton',
        'tags': 'New In, Kids, Cotton, Berries',
        'description': 'Playful British woodland prints rendered on breathable, lightweight 100% cotton for cosy bedtime evenings.'
    },
    {
        'name': 'Tween Midnight Whiskers Satin Nightwear Set',
        'slug': 'tween-midnight-whiskers-satin-nightwear-set',
        'sku': 'TN-TWEEN-WHISK-03',
        'price': Decimal('34.00'),
        'gender': 'kids',
        'category': cat_kids,
        'subcategory': sub_tween,
        'image_url': '/static/images/products/touch-tween-whiskers.png',
        'stock': 5,
        'size': 'S, M, L, XL',
        'material': 'Satin',
        'tags': 'New In, Tween, Satin, Whiskers',
        'description': 'Soft sheen silky satin designed specifically for older kids and tweens with signature hand-drawn cat and moon illustrations.'
    },
    {
        'name': 'Matching Family Celestial Star Navy Pyjamas',
        'slug': 'matching-family-celestial-star-navy-pyjamas',
        'sku': 'TN-FAM-STAR-04',
        'price': Decimal('38.00'),
        'gender': 'kids',
        'category': cat_kids,
        'subcategory': sub_family,
        'image_url': '/static/images/products/womens-celestial-satin.png',
        'stock': 10,
        'size': 'XS, S, M, L, XL',
        'material': 'Satin',
        'tags': 'New In, Family, Celestial, Matching',
        'description': 'Coordinate family bedtime in style with our matching Celestial Star print set, designed in deep midnight navy with golden star accents.'
    },
    {
        'name': 'Luxury Velvet Quilted Make-up Bag',
        'slug': 'luxury-velvet-quilted-makeup-bag',
        'sku': 'TN-ACC-BAG-05',
        'price': Decimal('18.00'),
        'gender': 'unisex',
        'category': cat_acc,
        'subcategory': sub_makeup,
        'image_url': '/static/images/products/touch-gift-box.png',
        'stock': 12,
        'size': 'One Size',
        'material': 'Velvet',
        'tags': 'New In, Accessories, Make-up Bag',
        'description': 'Plush quilted velvet pouch with gold-tone hardware and waterproof lining, perfect for cosmetic essentials at home or on holiday.'
    },
    {
        'name': 'Midnight Whiskers Silk Touch Eye Mask',
        'slug': 'midnight-whiskers-silk-touch-eye-mask',
        'sku': 'TN-ACC-MASK-06',
        'price': Decimal('14.00'),
        'gender': 'unisex',
        'category': cat_acc,
        'subcategory': sub_eyemask,
        'image_url': '/static/images/products/touch-gift-box.png',
        'stock': 15,
        'size': 'One Size',
        'material': 'Silk',
        'tags': 'New In, Accessories, Eye Mask',
        'description': 'Cushioned silk sleep mask with gentle ruched strap ensuring total darkness and ultimate bedtime comfort.'
    },
    {
        'name': 'Boutique Satin Waterproof Shower Cap',
        'slug': 'boutique-satin-waterproof-shower-cap',
        'sku': 'TN-ACC-CAP-07',
        'price': Decimal('12.00'),
        'gender': 'unisex',
        'category': cat_acc,
        'subcategory': sub_shower,
        'image_url': '/static/images/products/touch-gift-box.png',
        'stock': 14,
        'size': 'One Size',
        'material': 'Satin',
        'tags': 'New In, Accessories, Shower Cap',
        'description': 'Elegant waterproof shower turban designed to protect hair volume and blowouts in luxurious Their Nibs print.'
    },
    {
        'name': 'Pure Silk Hair Scrunchie 3-Pack Gift Set',
        'slug': 'pure-silk-hair-scrunchie-3-pack-gift-set',
        'sku': 'TN-ACC-SCRUNCH-08',
        'price': Decimal('10.00'),
        'gender': 'unisex',
        'category': cat_acc,
        'subcategory': sub_scrunchies,
        'image_url': '/static/images/products/touch-gift-box.png',
        'stock': 20,
        'size': 'One Size',
        'material': 'Silk',
        'tags': 'New In, Accessories, Scrunchies',
        'description': 'Gentle friction-free pure silk scrunchies that prevent hair creases and breakage, presented in a luxury boxed set.'
    },
]

for pdata in products_data:
    slug = pdata['slug']
    prod, created = Product.objects.get_or_create(
        slug=slug,
        defaults={
            'sku': pdata['sku'],
            'name': pdata['name'],
            'price': pdata['price'],
            'final_price': pdata['price'],
            'gender': pdata['gender'],
            'category': pdata['category'],
            'subcategory': pdata['subcategory'],
            'image_url': pdata['image_url'],
            'stock': pdata['stock'],
            'size': pdata['size'],
            'material': pdata['material'],
            'tags': pdata['tags'],
            'description': pdata['description'],
            'brand': brand,
            'seller': seller,
            'status': 'active',
            'is_featured': True
        }
    )
    if not created:
        prod.price = pdata['price']
        prod.final_price = pdata['price']
        prod.category = pdata['category']
        prod.subcategory = pdata['subcategory']
        prod.gender = pdata['gender']
        prod.status = 'active'
        prod.save()
    print(f'Product {prod.name}: ID {prod.id}, created={created}')

print('Seeding completed successfully!')

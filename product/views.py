from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import Q
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist
from django.conf import settings
from admin_panel.models import Product, Subcategory, Category, Occasion, ProductVariant, Brand, Seller
import json
import os

def womens_new_in_view(request, collection_slug=None):
    
    slug = (collection_slug or '').strip().lower()
    category_param = request.GET.get('category', '').strip().lower()
    gender_param = request.GET.get('gender', '').strip().lower()
    price_under = request.GET.get('price_under', '').strip()
    search_q = (request.GET.get('q', '') or request.GET.get('search', '')).strip()
    style_slug_filter = None
    fabric_slug_filter = None
    print_slug_filter = None

    if slug == 'search' or category_param == 'search' or search_q:
        category_param = 'search'
    elif slug and slug not in ['new-in-1', 'new-in']:
        if slug.startswith('gifts-under-'):
            price_under = slug.replace('gifts-under-', '')
            category_param = 'gifting'
        elif slug in ['matching-family', 'mens-matching-family', 'kids-matching-family']:
            category_param = 'matching-family'
        elif slug in ['kids', 'kids-pyjamas', 'tween-pyjamas', 'all-kids-tweens']:
            category_param = slug
        elif slug in ['mens', 'mens-pyjamas']:
            category_param = slug
        elif slug in ['accessories', 'makeup-bags', 'eye-masks', 'shower-caps', 'scrunchies']:
            category_param = slug
        elif slug in ['gifting', 'gifts-for-her', 'gifts-for-him', 'gifts-for-kids', 'gift-cards']:
            category_param = slug
        elif slug in ['traditional-long-pyjamas', 'oversized-pyjamas', 'short-pyjamas', 'capri-pyjamas', 'boxy-pyjamas', 'dressing-gowns-robes', 'nightdresses-shirts', 'bridal-party']:
            style_slug_filter = slug
        elif slug in ['cotton', 'brushed-cotton', 'cotton-voile', 'cotton-gauze', 'satin', 'linen-blend', 'jersey']:
            fabric_slug_filter = slug
        elif slug in ['animal-feather', 'celestial', 'gingham-checked', 'floral', 'striped']:
            print_slug_filter = slug
        elif slug in ['christmas-pyjamas', 'christmas']:
            print_slug_filter = 'christmas'
        elif slug == 'best-sellers':
            category_param = 'best-sellers'
        elif slug in ['shop-all-pyjama-sets', 'pyjama-sets', 'nightwear', 'all-nightwear']:
            category_param = 'all-pyjamas'
        else:
            category_param = slug

    collection_title = "New In"
    collection_desc = "Explore our latest sleepwear arrivals, featuring beautifully designed long pyjamas, short pyjamas, and our bestselling oversized pyjamas in dreamy hand-drawn prints."

    if category_param in ['matching-family', 'mens-matching-family', 'kids-matching-family']:
        family_filter = (
            Q(tags__icontains='Matching Family') |
            Q(name__icontains='Matching Family') |
            Q(name__icontains='Cosy Claus') |
            Q(name__icontains='Noel Mushroom') |
            Q(name__icontains='Red Tartan') |
            Q(name__icontains='Navy Penguins') |
            Q(name__icontains='Mushrooms and Bows')
        )
        if category_param == 'kids-matching-family':
            qs = Product.objects.filter(family_filter, gender='kids', status__in=['active', 'out_of_stock'])
        elif category_param == 'mens-matching-family':
            qs = Product.objects.filter(family_filter, gender='men', status__in=['active', 'out_of_stock'])
        else:
            qs = Product.objects.filter(family_filter, status__in=['active', 'out_of_stock'])


        qs = qs.exclude(category__slug='accessories').exclude(name__icontains='mask').exclude(name__icontains='pillow').exclude(name__icontains='scrunchie').exclude(name__icontains='cosmetic').exclude(name__icontains='bag').exclude(name__icontains='cap').exclude(name__icontains='card').select_related('brand', 'category', 'subcategory', 'occasion')
        collection_title = "Matching Family Pyjamas"
        collection_desc = "Coordinate in luxury comfort with our signature hand-drawn British matching family pyjama sets for mum, dad, and the little ones."

    elif category_param in ['kids', 'kids-pyjamas', 'tween-pyjamas', 'all-kids-tweens'] or gender_param == 'kids':
        qs = Product.objects.filter(
            Q(gender='kids') | Q(category__slug='kids') | Q(tags__icontains='kids') | Q(tags__icontains='tween'),
            status__in=['active', 'out_of_stock']
        ).exclude(gender='women').exclude(gender='men').exclude(gender='unisex').select_related('brand', 'category', 'subcategory', 'occasion')
        if category_param == 'kids-pyjamas':
            qs = qs.filter(Q(subcategory__slug='kids-pyjamas') | Q(name__icontains='pyjama') | Q(name__icontains='kids'))
            collection_title = "Kids Pyjamas"
        elif category_param == 'tween-pyjamas':
            qs = qs.filter(Q(subcategory__slug='tween-pyjamas') | Q(name__icontains='tween'))
            collection_title = "Tween Pyjamas & Nightwear"
        else:
            collection_title = "Kids Collection"
        collection_desc = "Discover our comfortable, playful British-designed pyjama sets for kids and tweens, crafted from breathable cotton and softest fabrics."

    elif category_param in ['mens', 'mens-pyjamas'] or gender_param in ['men', 'mens']:
        qs = Product.objects.filter(
            Q(gender='men') | Q(category__slug='mens'),
            status__in=['active', 'out_of_stock']
        ).exclude(gender='women').exclude(gender='kids').select_related('brand', 'category', 'subcategory', 'occasion')
        collection_title = "Mens Pyjamas" if 'pyjama' in category_param else "Mens Collection"
        collection_desc = "Sophisticated British sleepwear for men, crafted in signature hand-drawn prints, tailored relaxed cuts, and premium fabrics."

    elif category_param in ['accessories', 'makeup-bags', 'eye-masks', 'shower-caps', 'scrunchies']:
        qs = Product.objects.filter(
            Q(category__slug='accessories') | Q(tags__icontains='accessories'),
            status__in=['active', 'out_of_stock']
        ).select_related('brand', 'category', 'subcategory', 'occasion')
        if category_param == 'makeup-bags':
            qs = qs.filter(Q(subcategory__slug='makeup-bags') | Q(name__icontains='make-up') | Q(name__icontains='makeup'))
            collection_title = "Make-up Bags"
        elif category_param == 'eye-masks':
            qs = qs.filter(Q(subcategory__slug='eye-masks') | Q(name__icontains='mask'))
            collection_title = "Eye Masks"
        elif category_param == 'shower-caps':
            qs = qs.filter(Q(subcategory__slug='shower-caps') | Q(name__icontains='shower'))
            collection_title = "Shower Caps"
        elif category_param == 'scrunchies':
            qs = qs.filter(Q(subcategory__slug='scrunchies') | Q(name__icontains='scrunchie'))
            collection_title = "Scrunchies"
        else:
            collection_title = "Accessories"
        collection_desc = "Complete your relaxation ritual with our luxury make-up bags, silk eye masks, and sleep accessories."

    elif category_param in ['gifting', 'gifts-for-her', 'gifts-for-him', 'gifts-for-kids', 'gift-cards']:
        if category_param == 'gifts-for-her':
            qs = Product.objects.filter(gender='women', status__in=['active', 'out_of_stock'])
            collection_title = "Gifts For Her"
        elif category_param == 'gifts-for-him':
            qs = Product.objects.filter(gender='men', status__in=['active', 'out_of_stock']).exclude(gender='women').exclude(tags__icontains='Matching Family')
            collection_title = "Gifts For Him"
        elif category_param == 'gifts-for-kids':
            qs = Product.objects.filter(gender='kids', status__in=['active', 'out_of_stock']).exclude(gender='women').exclude(gender='men')
            collection_title = "Gifts For Kids"
        elif category_param == 'gift-cards':
            qs = Product.objects.filter(Q(slug__icontains='voucher') | Q(name__icontains='voucher') | Q(name__icontains='gift'), status__in=['active', 'out_of_stock'])
            collection_title = "E-Gift Cards"
        else:
            qs = Product.objects.filter(Q(category__slug='gifting') | Q(tags__icontains='gifting') | Q(is_featured=True), status__in=['active', 'out_of_stock'])
            collection_title = "Gifting Collection"
        qs = qs.select_related('brand', 'category', 'subcategory', 'occasion')
        collection_desc = "Thoughtfully curated gifts for her, him, and the little ones, wrapped in signature Their Nibs packaging."

    elif category_param == 'best-sellers':
        qs = Product.objects.filter(status__in=['active', 'out_of_stock']).select_related('brand', 'category', 'subcategory', 'occasion').order_by('-is_featured', '-stock', '-created_at')
        collection_title = "Best Sellers"
        collection_desc = "Our all-time best loved luxury pyjama sets and nightwear."

    elif category_param in ['halloween', 'halloween-pyjamas', 'spooky'] or slug == 'halloween':
        qs = Product.objects.filter(
            Q(tags__icontains='Halloween') |
            Q(tags__icontains='Midnight Whiskers') |
            Q(category__slug='halloween') |
            Q(slug__icontains='whiskers') |
            Q(name__icontains='whiskers'),
            status__in=['active', 'out_of_stock']
        ).select_related('brand', 'category', 'subcategory', 'occasion')
        collection_title = "Halloween Pyjamas & Nightwear"
        collection_desc = "Step into our enchanting Halloween collection featuring spooky black cats, celestial starry skies, and whimsical midnight sleepwear designed to bring playful luxury to crisp autumn nights."

    elif category_param == 'all-pyjamas':
        qs = Product.objects.filter(status__in=['active', 'out_of_stock']).select_related('brand', 'category', 'subcategory', 'occasion')
        if slug in ['nightwear', 'all-nightwear']:
            collection_title = "Nightwear"
            collection_desc = "Discover our luxurious collection of nightwear, including traditional pyjama sets, cosy nightshirts, and signature hand-drawn prints."
        else:
            collection_title = "Shop All Pyjama Sets"
            collection_desc = "Explore every signature Their Nibs pyjama design across long, short, boxy, and oversized sets."

    elif category_param == 'search' or slug == 'search' or search_q:
        if search_q:
            terms = search_q.split()
            s_query = Q()
            for t in terms:
                s_query &= (
                    Q(name__icontains=t) |
                    Q(tags__icontains=t) |
                    Q(description__icontains=t) |
                    Q(material__icontains=t) |
                    Q(color__icontains=t) |
                    Q(image_url__icontains=t) |
                    Q(slug__icontains=t) |
                    Q(category__name__icontains=t) |
                    Q(subcategory__name__icontains=t) |
                    Q(occasion__name__icontains=t)
                )
            qs = Product.objects.filter(s_query, status__in=['active', 'out_of_stock']).select_related('brand', 'category', 'subcategory', 'occasion').distinct()
            collection_title = f'Search: "{search_q}"'
            collection_desc = f'Found {qs.count()} item(s) matching your search for "{search_q}".'
        else:
            qs = Product.objects.filter(status__in=['active', 'out_of_stock']).select_related('brand', 'category', 'subcategory', 'occasion')
            collection_title = "Search Our Collection"
            collection_desc = "Discover our signature pyjama sets, luxury sleepwear, and gifts."

    else:
        qs = Product.objects.filter(
            gender__in=['women', 'unisex'],
            status__in=['active', 'out_of_stock']
        ).exclude(gender='men').exclude(tags__icontains='Matching Family').select_related('brand', 'category', 'subcategory', 'occasion')
        new_in_tagged = qs.filter(Q(tags__icontains='New In') | Q(is_featured=True) | Q(slug__icontains='whiskers'))
        if new_in_tagged.exists() and not (style_slug_filter or fabric_slug_filter or print_slug_filter or category_param == 'search' or search_q):
            qs = new_in_tagged

    if style_slug_filter:
        title_words = style_slug_filter.replace('-', ' ').title()
        collection_title = title_words
        collection_desc = f"Shop our authentic British-designed {title_words.lower()} crafted in soft, breathable fabrics."
        qs = qs.filter(
            Q(subcategory__slug__icontains=style_slug_filter) |
            Q(subcategory__name__icontains=style_slug_filter) |
            Q(name__icontains=style_slug_filter.replace('-', ' '))
        )

    if fabric_slug_filter:
        fab_name = fabric_slug_filter.replace('-', ' ').title()
        collection_title = f"{fab_name} Pyjamas"
        collection_desc = f"Delightfully breathable and soft {fab_name.lower()} sleepwear from Their Nibs."
        qs = qs.filter(Q(material__icontains=fab_name) | Q(name__icontains=fab_name))

    if print_slug_filter:
        if print_slug_filter == 'christmas':
            collection_title = "Christmas Pyjamas"
            collection_desc = "Festive luxury sleepwear and matching family prints for magical winter nights."
            qs = Product.objects.filter(status__in=['active', 'out_of_stock']).select_related('brand', 'category', 'subcategory', 'occasion')
            xmas_filter = qs.filter(Q(tags__icontains='Christmas') | Q(name__icontains='Christmas') | Q(occasion__name__icontains='Christmas') | Q(tags__icontains='Festive') | Q(tags__icontains='Matching'))
            if xmas_filter.exists():
                qs = xmas_filter
        elif print_slug_filter == 'striped':
            collection_title = "Striped Print Nightwear"
            collection_desc = "Hand-drawn British stripe and striped print designs on premium pyjamas."
            qs = qs.filter(Q(tags__icontains='stripe') | Q(name__icontains='stripe') | Q(description__icontains='stripe'))
        elif print_slug_filter == 'celestial':
            collection_title = "Celestial Print Nightwear"
            collection_desc = "Hand-drawn British celestial, star and moon print designs on premium pyjamas."
            qs = qs.filter(Q(tags__icontains='celestial') | Q(name__icontains='celestial') | Q(name__icontains='moon') | Q(name__icontains='star') | Q(description__icontains='celestial') | Q(description__icontains='star'))
        elif print_slug_filter == 'floral':
            collection_title = "Floral Print Nightwear"
            collection_desc = "Hand-drawn British floral, wildflower and botanical print designs on premium pyjamas."
            qs = qs.filter(Q(tags__icontains='floral') | Q(name__icontains='floral') | Q(name__icontains='flower') | Q(name__icontains='botanical') | Q(name__icontains='wisteria') | Q(description__icontains='floral'))
        elif print_slug_filter in ['gingham-checked', 'gingham-check']:
            collection_title = "Gingham & Check Print Nightwear"
            collection_desc = "Hand-drawn British gingham and check print designs on premium pyjamas."
            qs = qs.filter(Q(tags__icontains='gingham') | Q(tags__icontains='check') | Q(name__icontains='gingham') | Q(name__icontains='check') | Q(description__icontains='gingham') | Q(description__icontains='check'))
        elif print_slug_filter in ['animal-feather', 'animal']:
            collection_title = "Animal & Feather Print Nightwear"
            collection_desc = "Hand-drawn British animal, feather and nature print designs on premium pyjamas."
            qs = qs.filter(
                Q(tags__icontains='animal') | Q(tags__icontains='feather') | Q(tags__icontains='bird') | Q(tags__icontains='bee') |
                Q(name__icontains='animal') | Q(name__icontains='feather') | Q(name__icontains='peacock') | Q(name__icontains='hummingbird') |
                Q(name__icontains='bee') | Q(name__icontains='leopard') | Q(name__icontains='tiger') | Q(name__icontains='butterfly') |
                Q(description__icontains='animal') | Q(description__icontains='feather')
            )
        else:
            pr_name = print_slug_filter.replace('-', ' ').title()
            collection_title = f"{pr_name} Print Nightwear"
            collection_desc = f"Hand-drawn British {pr_name.lower()} print designs on premium pyjamas."
            qs = qs.filter(Q(tags__icontains=pr_name) | Q(name__icontains=pr_name) | Q(description__icontains=pr_name) | Q(occasion__name__icontains=pr_name))

    if price_under:
        try:
            p_val = float(price_under)
            qs = qs.filter(final_price__lte=p_val)
            collection_title = f"Gifts Under ₹{price_under}"
        except ValueError:
            pass

    style_param = request.GET.get('style', '').strip()
    size_param = request.GET.get('size', '').strip()
    fabric_param = request.GET.get('fabric', '').strip()
    color_param = request.GET.get('color', '').strip()
    print_param = request.GET.get('print', '').strip()
    availability_param = request.GET.get('availability', '').strip()
    sort_param = request.GET.get('sort', 'manual').strip()

    if style_param:
        qs = qs.filter(
            Q(subcategory__slug__iexact=style_param) |
            Q(subcategory__name__icontains=style_param)
        )

    if size_param:
        size_code = size_param.split('/')[0].strip()
        qs = qs.filter(
            Q(variants__size__icontains=size_code, variants__is_available=True) |
            Q(size__icontains=size_code)
        ).distinct()

    if fabric_param:
        qs = qs.filter(material__icontains=fabric_param)

    if color_param:
        qs = qs.filter(
            Q(color__icontains=color_param) |
            Q(variants__color__icontains=color_param)
        ).distinct()

    if print_param:
        qs = qs.filter(
            Q(occasion__name__icontains=print_param) |
            Q(tags__icontains=print_param)
        )

    if availability_param == 'in_stock' or availability_param == 'in-stock':
        qs = qs.filter(stock__gt=0)
    elif availability_param == 'out_of_stock' or availability_param == 'out-of-stock':
        qs = qs.filter(stock__lte=0)

    if sort_param in ['price-ascending', 'price-low']:
        qs = qs.order_by('final_price')
    elif sort_param in ['price-descending', 'price-high']:
        qs = qs.order_by('-final_price')
    elif sort_param in ['created-descending', 'newest']:
        qs = qs.order_by('-created_at')
    elif sort_param in ['created-ascending', 'oldest']:
        qs = qs.order_by('created_at')
    elif sort_param in ['title-ascending', 'name-asc']:
        qs = qs.order_by('name')
    elif sort_param in ['title-descending', 'name-desc']:
        qs = qs.order_by('-name')
    elif sort_param == 'best-selling':
        qs = qs.order_by('-stock', '-created_at')
    else:
        qs = qs.order_by('-is_featured', '-created_at')

    all_womens = Product.objects.filter(gender__in=['women', 'unisex'], status__in=['active', 'out_of_stock'])

    style_facets = []
    for sc in Subcategory.objects.filter(category__slug='womens').order_by('name'):
        count = all_womens.filter(subcategory=sc).count()
        if count > 0:
            style_facets.append({'name': sc.name, 'slug': sc.slug, 'count': count})

    fabric_names = ['Satin', 'Cotton', 'Brushed Cotton', 'Velvet', 'Cotton Voile', 'Linen Blend']
    fabric_facets = []
    for fab in fabric_names:
        count = all_womens.filter(material__icontains=fab).count()
        if count > 0:
            fabric_facets.append({'name': fab, 'count': count})

    size_facets = [
        {'name': 'XS / 8', 'code': 'XS', 'count': all_womens.filter(size__icontains='XS').count()},
        {'name': 'S / 10', 'code': 'S', 'count': all_womens.filter(size__icontains='S').count()},
        {'name': 'M / 12', 'code': 'M', 'count': all_womens.filter(size__icontains='M').count()},
        {'name': 'L / 14-16', 'code': 'L', 'count': all_womens.filter(size__icontains='L').count()},
        {'name': 'XL / 18-20', 'code': 'XL', 'count': all_womens.filter(size__icontains='XL').count()},
    ]

    color_names = [
        ('Cream', '#fdfbf7'),
        ('Champagne', '#f7e7ce'),
        ('Fig', '#4a154b'),
        ('Navy', '#1a2a3a'),
        ('Pink', '#f9c5d1'),
        ('Black', '#1a1a1a'),
        ('Duck Egg Blue', '#9ec8c6'),
        ('Mauve', '#9d7e8a'),
        ('Emerald Green', '#047857'),
        ('Sage Green', '#84a98c'),
    ]
    color_facets = []
    for cname, chex in color_names:
        count = all_womens.filter(color__icontains=cname).count()
        if count > 0:
            color_facets.append({'name': cname, 'hex': chex, 'count': count})


    print_facets = []
    for occ in Occasion.objects.all().order_by('name'):
        count = all_womens.filter(occasion=occ).count()
        if count > 0:
            print_facets.append({'name': occ.name, 'count': count})

    in_stock_count = all_womens.filter(stock__gt=0).count()
    out_of_stock_count = all_womens.filter(stock__lte=0).count()

    active_filters_count = sum(1 for val in [style_param, size_param, fabric_param, color_param, print_param, availability_param] if val)

    gallery_map = {
        14: [
            '/static/images/products/45_Vintage_Horizons_Boxy_Pyjama_Set_005_5_UNCROPPED.jpg',
            '/static/images/products/45_Vintage_Horizons_Boxy_Pyjama_Set_036_5_UNCROPPED.jpg',
            '/static/images/products/45_Vintage_Horizons_Boxy_Pyjama_Set_031_5_UNCROPPED.jpg',
            '/static/images/products/45_Vintage_Horizons_Boxy_Pyjama_Set_021_5_UNCROPPED.jpg',
        ],
        16: [
            '/static/images/products/49_Womens_Velvet_Fig_with_Contrast_Trim_Grandpa_Robe_with_hood_003_5_UNCROPPED.jpg',
            '/static/images/products/49_Womens_Velvet_Fig_with_Contrast_Trim_Grandpa_Robe_with_hood_040_5_UNCROPPED.jpg',
            '/static/images/products/49_Womens_Velvet_Fig_with_Contrast_Trim_Grandpa_Robe_with_hood_033_5_UNCROPPED.jpg',
            '/static/images/products/49_Womens_Velvet_Fig_with_Contrast_Trim_Grandpa_Robe_with_hood_020_5_UNCROPPED.jpg',
        ],
        13: [
            '/static/images/products/46_Vintage_Horizons_Satin_Kimono_Robe_003_5_UNCROPPED.jpg',
            '/static/images/products/46_Vintage_Horizons_Satin_Kimono_Robe_010_5_UNCROPPED.jpg',
            '/static/images/products/46_Vintage_Horizons_Satin_Kimono_Robe_023_5_UNCROPPED.jpg',
            '/static/images/products/46_Vintage_Horizons_Satin_Kimono_Robe_003_5_UNCROPPED.jpg',
        ],
        15: [
            '/static/images/products/47_Womens_Cotton_Ecru_Retro_Sky_Pyjama_set_002_5_UNCROPPED_0e8aacee-65d8-423f-8241-9605e47a4b6c.jpg',
            '/static/images/products/47_Womens_Cotton_Ecru_Retro_Sky_Pyjama_set_032_5_UNCROPPED.jpg',
            '/static/images/products/47_Womens_Cotton_Ecru_Retro_Sky_Pyjama_set_002_5_UNCROPPED_0e8aacee-65d8-423f-8241-9605e47a4b6c.jpg',
            '/static/images/products/47_Womens_Cotton_Ecru_Retro_Sky_Pyjama_set_032_5_UNCROPPED.jpg',
        ],
        17: [
            '/static/images/products/53_Womens_Velvet_Navy_Solid_with_Neo_Classical_Trim_Grandpa_Robe_with_hood_006_5_UNCROPPED.jpg',
            '/static/images/products/53_Womens_Velvet_Navy_Solid_with_Neo_Classical_Trim_Grandpa_Robe_with_hood_049_5_UNCROPPED.jpg',
            '/static/images/products/53_Womens_Velvet_Navy_Solid_with_Neo_Classical_Trim_Grandpa_Robe_with_hood_006_5_UNCROPPED.jpg',
            '/static/images/products/53_Womens_Velvet_Navy_Solid_with_Neo_Classical_Trim_Grandpa_Robe_with_hood_049_5_UNCROPPED.jpg',
        ],
        18: [
            '/static/images/products/52_Womens_Velvet_Pink_Harvest_with_pink_Trim_Grandpa_Robe_with_hood_016_5_UNCROPPED.jpg',
            '/static/images/products/52_Womens_Velvet_Pink_Harvest_with_pink_Trim_Grandpa_Robe_with_hood_038_5_UNCROPPED.jpg',
            '/static/images/products/52_Womens_Velvet_Pink_Harvest_with_pink_Trim_Grandpa_Robe_with_hood_016_5_UNCROPPED.jpg',
            '/static/images/products/52_Womens_Velvet_Pink_Harvest_with_pink_Trim_Grandpa_Robe_with_hood_038_5_UNCROPPED.jpg',
        ],
        19: [
            '/static/images/products/51_Womens_Satin_Joy_oh_Joy_Oversize_Pyjama_set_009_5_UNCROPPED.jpg',
            '/static/images/products/51_Womens_Satin_Joy_oh_Joy_Oversize_Pyjama_set_036_5_UNCROPPED.jpg',
            '/static/images/products/51_Womens_Satin_Joy_oh_Joy_Oversize_Pyjama_set_009_5_UNCROPPED.jpg',
            '/static/images/products/51_Womens_Satin_Joy_oh_Joy_Oversize_Pyjama_set_036_5_UNCROPPED.jpg',
        ],
        20: [
            '/static/images/products/57_Womens_Satin_Harlequin_Pyjama_Set_006_5_UNCROPPED.jpg',
            '/static/images/products/57_Womens_Satin_Harlequin_Pyjama_Set_038_5_UNCROPPED.jpg',
            '/static/images/products/57_Womens_Satin_Harlequin_Pyjama_Set_006_5_UNCROPPED.jpg',
            '/static/images/products/57_Womens_Satin_Harlequin_Pyjama_Set_038_5_UNCROPPED.jpg',
        ],
    }

    products_list = list(qs)
    for p in products_list:
        p.gallery_urls = gallery_map.get(p.id, [p.image_url, p.image_url, p.image_url, p.image_url])
        p.sizes_list = ['XS / 8', 'S / 10', 'M / 12', 'L / 14-16', 'XL / 18-20', 'XXL / 20-22', '3XL / 22-24']

    sort_names_map = {
        'manual': 'Featured',
        'featured': 'Featured',
        'best-selling': 'Best selling',
        'title-ascending': 'Alphabetically, A-Z',
        'name-asc': 'Alphabetically, A-Z',
        'title-descending': 'Alphabetically, Z-A',
        'name-desc': 'Alphabetically, Z-A',
        'price-ascending': 'Price, low to high',
        'price-low': 'Price, low to high',
        'price-descending': 'Price, high to low',
        'price-high': 'Price, high to low',
        'created-descending': 'Date, new to old',
        'newest': 'Date, new to old',
        'created-ascending': 'Date, old to new',
        'oldest': 'Date, old to new',
    }
    sort_display_name = sort_names_map.get(sort_param, 'Featured')

    context = {
        'products': products_list,
        'total_count': len(products_list),
        'style_facets': style_facets,
        'fabric_facets': fabric_facets,
        'size_facets': size_facets,
        'color_facets': color_facets,
        'print_facets': print_facets,
        'in_stock_count': in_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'style_param': style_param,
        'size_param': size_param,
        'fabric_param': fabric_param,
        'color_param': color_param,
        'print_param': print_param,
        'availability_param': availability_param,
        'sort_param': sort_param,
        'sort_display_name': sort_display_name,
        'active_filters_count': active_filters_count,
        'collection_title': collection_title,
        'collection_desc': collection_desc,
        'category_param': category_param,
        'collection_slug': collection_slug or category_param or 'new-in-1',
        'search_query': search_q,
        'is_mens': (
            category_param in ['mens', 'mens-pyjamas'] or
            'mens' in str(collection_slug or '').lower() or
            gender_param in ['men', 'mens']
        ) and not ('family' in str(collection_slug or '').lower()),
        'is_mens_or_kids': (
            category_param in ['mens', 'mens-pyjamas', 'mens-matching-family', 'kids', 'kids-pyjamas', 'tween-pyjamas', 'matching-family', 'all-kids-tweens'] or
            'mens' in str(collection_slug or '').lower() or
            'kids' in str(collection_slug or '').lower() or
            'matching-family' in str(collection_slug or '').lower() or
            gender_param in ['men', 'mens', 'kids']
        ),
        'show_editorial_banner': not (
            category_param in ['mens', 'mens-pyjamas', 'mens-matching-family', 'kids', 'kids-pyjamas', 'tween-pyjamas', 'matching-family', 'all-kids-tweens'] or
            'mens' in str(collection_slug or '').lower() or
            'kids' in str(collection_slug or '').lower() or
            'matching-family' in str(collection_slug or '').lower() or
            gender_param in ['men', 'mens', 'kids']
        ),
    }

    target_key = (collection_slug or category_param or 'new-in-1').strip().lower()

    slug_to_template_map = {
        
        'search': ('product', 'base_collection'),

        'halloween': ('halloween', 'halloween_pyjamas'),
        'halloween-pyjamas': ('halloween', 'halloween_pyjamas'),
        'spooky': ('halloween', 'halloween_pyjamas'),

        'new-in': ('womens', 'new_in'),
        'new-in-1': ('womens', 'new_in'),
        'best-sellers': ('womens', 'best_seller'),
        'best-seller': ('womens', 'best_seller'),
        'shop-all-pyjama-sets': ('womens', 'shop_all_pyjama_sets'),
        'all-pyjamas': ('womens', 'shop_all_pyjama_sets'),
        'pyjama-sets': ('womens', 'shop_all_pyjama_sets'),
        'nightwear': ('womens', 'shop_all_pyjama_sets'),
        'all-nightwear': ('womens', 'shop_all_pyjama_sets'),
        'gift-cards': ('womens', 'gift_cards'),
        'traditional-long-pyjamas': ('womens', 'traditional_long_pyjamas'),
        'oversized-pyjamas': ('womens', 'oversized_pyjamas'),
        'short-pyjamas': ('womens', 'short_pyjamas'),
        'capri-pyjamas': ('womens', 'capri_pyjamas'),
        'boxy-pyjamas': ('womens', 'boxy_pyjamas'),
        'dressing-gowns-robes': ('womens', 'dressing_gowns_robes'),
        'nightdresses-shirts': ('womens', 'nightdresses_shirts'),
        'cotton': ('womens', 'cotton'),
        'brushed-cotton': ('womens', 'brushed_cotton'),
        'cotton-voile': ('womens', 'cotton_voile'),
        'cotton-gauze': ('womens', 'cotton_gauze'),
        'satin': ('womens', 'satin'),
        'linen-blend': ('womens', 'linen_blend'),
        'jersey': ('womens', 'jersey'),
        'christmas-pyjamas': ('womens', 'christmas_pyjamas'),
        'christmas': ('womens', 'christmas_pyjamas'),
        'matching-family': ('womens', 'matching_family'),
        'animal-feather': ('womens', 'animal_feather'),
        'celestial': ('womens', 'celestial'),
        'gingham-checked': ('womens', 'gingham_checked'),
        'floral': ('womens', 'floral'),
        'striped': ('womens', 'striped'),
        'bridal-party': ('womens', 'bridal_party'),

        
        'mens': ('mens', 'mens_pyjamas'),
        'mens-pyjamas': ('mens', 'mens_pyjamas'),
        'mens-matching-family': ('mens', 'matching_family'),
        'all-mens': ('mens', 'all_mens'),

        
        'kids': ('kids', 'kids_pyjamas'),
        'kids-pyjamas': ('kids', 'kids_pyjamas'),
        'tween-pyjamas': ('kids', 'tween_pyjamas'),
        'kids-matching-family': ('kids', 'matching_family'),
        'all-kids-tweens': ('kids', 'all_kids_tweens'),

        
        'accessories': ('accessories', 'makeup_bags'),
        'makeup-bags': ('accessories', 'makeup_bags'),
        'eye-masks': ('accessories', 'eye_masks'),
        'shower-caps': ('accessories', 'shower_caps'),
        'scrunchies': ('accessories', 'scrunchies'),

        
        'gifting': ('gift', 'gifts_for_her'),
        'gifts-for-her': ('gift', 'gifts_for_her'),
        'gifts-for-him': ('gift', 'gifts_for_him'),
        'gifts-for-kids': ('gift', 'gifts_for_kids'),
        'gifts-under-1000': ('gift', 'gifts_under_1000'),
        'gifts-under-500': ('gift', 'gifts_under_500'),
        'gifts-under-250': ('gift', 'gifts_under_250'),
        'gifts-under-150': ('gift', 'gifts_under_150'),
    }

    cat_folder, sub_folder = slug_to_template_map.get(target_key, ('womens', 'new_in'))
    template_candidates = [
        f"product/{cat_folder}/{sub_folder}/index.html",
        f"product/{cat_folder}/{sub_folder}.html",
        f"{cat_folder}/{sub_folder}/index.html",
        "product/base_collection.html",
        "womens_new_in.html",
    ]

    chosen_template = "womens_new_in.html"
    for cand in template_candidates:
        try:
            get_template(cand)
            chosen_template = cand
            break
        except TemplateDoesNotExist:
            continue

    return render(request, chosen_template, context)


def search_view(request):
    
    return womens_new_in_view(request, collection_slug='search')


def search_api_view(request):
    
    q = (request.GET.get('q', '') or request.GET.get('search', '')).strip()
    if not q:
        return JsonResponse({'results': [], 'total_count': 0, 'query': ''})

    terms = q.split()
    s_query = Q()
    for t in terms:
        s_query &= (
            Q(name__icontains=t) |
            Q(tags__icontains=t) |
            Q(description__icontains=t) |
            Q(material__icontains=t) |
            Q(color__icontains=t) |
            Q(image_url__icontains=t) |
            Q(slug__icontains=t) |
            Q(category__name__icontains=t) |
            Q(subcategory__name__icontains=t) |
            Q(occasion__name__icontains=t)
        )

    qs = Product.objects.filter(s_query, status__in=['active', 'out_of_stock']).select_related('brand', 'category', 'subcategory', 'occasion').distinct().order_by('-is_featured', '-stock', '-created_at')

    total_count = qs.count()
    limited_qs = qs[:8]

    results = []
    for p in limited_qs:
        results.append({
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'url': f'/product/{p.slug}/',
            'image_url': p.image_url or '/static/images/products/touch-gift-box.png',
            'price': float(p.price) if p.price else 0,
            'final_price': float(p.final_price) if p.final_price else 0,
            'is_out_of_stock': p.stock <= 0 or p.status == 'out_of_stock',
            'material': p.material or '',
            'color': p.color or '',
            'category': p.category.name if p.category else '',
        })

    return JsonResponse({
        'results': results,
        'total_count': total_count,
        'query': q,
    })


def product_detail_view(request, slug):
    
    norm_slug = slug.strip().replace(' ', '-').lower()
    product = Product.objects.filter(slug=slug).first() or Product.objects.filter(slug=norm_slug).first()
    if not product:
        product = Product.objects.filter(slug__iexact=norm_slug).first()
    if not product:
        product = Product.objects.filter(slug__icontains=norm_slug).first()
    if not product:
        product = Product.objects.filter(status__in=['active', 'out_of_stock']).first()

    card_image = request.GET.get('image', '').strip()
    primary_image = None
    if card_image and card_image.startswith('/static/'):
        primary_image = card_image
    elif product and product.image_url:
        primary_image = product.image_url
    else:
        primary_image = '/static/images/products/mens-navy-contrast-gauze.png'

    gallery = [primary_image]

    if product and product.image_url and '/static/images/catalog/' in product.image_url:
        try:
            rel_path = product.image_url.replace('/static/', '', 1).lstrip('/\\')
            disk_path = os.path.join(settings.BASE_DIR, 'static', rel_path)
            folder_path = os.path.dirname(disk_path)
            curr_filename = os.path.basename(disk_path)
            if os.path.exists(folder_path):
                raw_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]

                files = sorted(raw_files, key=lambda x: (int(os.path.splitext(x)[0]) if os.path.splitext(x)[0].isdigit() else 999, x))
                rel_dir = os.path.dirname(product.image_url).replace('\\', '/')
                for f in files:
                    full_url = f"{rel_dir}/{f}"
                    if full_url != primary_image and full_url not in gallery:
                        gallery.append(full_url)
        except Exception:
            pass
    elif product and 'mens-navy-contrast-gauze' in getattr(product, 'slug', ''):
        gallery = [
            primary_image,
            '/static/images/products/mens-midnight-whiskers.png',
            '/static/images/products/mens-midnight-whiskers-b.png',
        ]
    elif product and 'mens-midnight-whiskers' in getattr(product, 'slug', ''):
        gallery = [
            primary_image,
            '/static/images/products/mens-midnight-whiskers-b.png',
            '/static/images/products/mens-midnight-whiskers-c.png',
        ]

    finishing_touches = [
        {
            'id': 'touch-box',
            'name': 'Luxury Gift Box',
            'price': '249.00',
            'currency': '₹',
            'image': '/static/images/products/touch-gift-box.png',
        },
        {
            'id': 'touch-voucher',
            'name': 'Their Nibs Gift E-Voucher',
            'price': '299.00',
            'currency': '₹',
            'image': '/static/images/products/touch-gift-voucher.png',
        },
    ]

    sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL']

    category_slug = product.category.slug if (product and product.category and product.category.slug) else 'womens'

    category_name = "Women's Pyjamas"
    category_url = "/collections/new-in-1/"

    if product:
        prod_cat_slug = getattr(product.category, 'slug', '') if product.category else ''
        prod_gender = (getattr(product, 'gender', '') or '').lower()
        prod_tags = getattr(product, 'tags', '') or ''
        prod_name = getattr(product, 'name', '') or ''

        if prod_gender == 'kids' or prod_cat_slug == 'kids':
            category_name = "Kids & Tweens"
            category_url = "/collections/kids/"
        elif prod_gender in ['men', 'mens'] or prod_cat_slug in ['mens', 'men']:
            category_name = "Mens Pyjamas"
            category_url = "/collections/mens/"
        elif 'Matching Family' in prod_tags or 'Matching Family' in prod_name or 'Family' in prod_name:
            category_name = "Matching Family Pyjamas"
            category_url = "/collections/matching-family/"
        elif prod_cat_slug == 'accessories':
            category_name = "Accessories"
            category_url = "/collections/accessories/"
        else:
            category_name = "Women's Pyjamas"
            category_url = "/collections/new-in-1/"

    subcategory_name = None
    subcategory_url = None
    if product and product.subcategory:
        subcategory_name = product.subcategory.name
        subcategory_url = f"/collections/{product.subcategory.slug}/"

    referer = request.META.get('HTTP_REFERER', '')
    back_url = subcategory_url or category_url
    if referer and request.get_host() in referer and referer != request.build_absolute_uri():
        back_url = referer

    context = {
        'product': product,
        'gallery': gallery,
        'sizes': sizes,
        'finishing_touches': finishing_touches,
        'stock': product.stock if (product and product.stock is not None) else 0,
        'category_slug': category_slug,
        'category_name': category_name,
        'category_url': category_url,
        'subcategory_name': subcategory_name,
        'subcategory_url': subcategory_url,
        'back_url': back_url,
    }
    return render(request, 'product_detail.html', context)


collection_view = womens_new_in_view

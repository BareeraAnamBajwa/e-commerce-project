from django.db import OperationalError
from .models import SiteSettings, FooterLink, Product

def site_settings(request):
    try:
        site_settings_obj = SiteSettings.load()
    except OperationalError:
        # Table doesn't exist yet, return empty settings
        site_settings_obj = None
    
    try:
        footer_links = FooterLink.objects.filter(is_active=True)
    except OperationalError:
        # Table doesn't exist yet, return empty list
        footer_links = []
    
    try:
        trending_items = Product.objects.all()[:4]
    except OperationalError:
        trending_items = []
    
    return {
        'site_settings': site_settings_obj,
        'footer_links': footer_links,
        'trending_items': trending_items,
    }


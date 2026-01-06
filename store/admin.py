from django.contrib import admin
from .models import Product, Category , Features , ProductImage , SubCategory , cart , Address, Slider, Promotion, Review, Brand, SiteSettings, FooterLink
# Register your models here.
# admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Features)
admin.site.register(ProductImage)
admin.site.register(SubCategory)
admin.site.register(cart)
admin.site.register(Address)
admin.site.register(Slider)
admin.site.register(Promotion)
admin.site.register(Review)
admin.site.register(Brand)
admin.site.register(SiteSettings)
admin.site.register(FooterLink)
from django.contrib import admin
from .models import Product, Category , Features , ProductImage , SubCategory , cart , Address, Slider, Promotion, Review, Brand, SiteSettings, FooterLink

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'original_price',
        'price',
        'calculated_discount_percent',
    )

    readonly_fields = (
        'calculated_discount_percent',
        'final_price',
    )

    fieldsets = (
        (None, {
            'fields': (
                'name',
                # 'sku',
                'category',
                'warranty',
                'availability',
            )
        }),
        ('Pricing (Admin Input)', {
            'fields': (
                'original_price',
                'price',
                'discount',
            )
        }),
        ('Calculated (System)', {
            'fields': (
                'calculated_discount_percent',
                'final_price',
            )
        }),
        ('Other', {
            'fields': (
                'features',
                'image',
                'image_url',
            )
        }),
    )


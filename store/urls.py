from django.urls import path

from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path("", views.index, name="index"),
    path("about_us/", views.about_us_view, name="about_us"),
    path("checkout_cart/", views.checkout_cart_view, name="checkout_cart"),
    path("checkout_complete/", views.checkout_complete_view, name="checkout_complete"),
    path("checkout_info/", views.checkout_info_view, name="checkout_info"),
    path("checkout_payment/", views.checkout_payment_view, name="checkout_payment"),
    path("contact_us/", views.contact_us_view, name="contact_us"),
    path("faq/", views.faq_view, name="faq"),
    path("index_fixed/", views.index_fixed_view, name="index_fixed"),
    path("index_inverse_header/",views.index_inverse_header_view,name="index_inverse_header"),
    path("my_account/", views.my_account_view, name="my_account"),
    path("<int:product_id>/", views.product_detail_view, name="product_detail"),
    path("product/", views.product_view, name="product"),
    path("search_results/", views.search_results_view, name="search_results"),
    path("cart/update/<int:cart_id>/", views.update_cart_quantity, name="update_cart_quantity"),
    path("cart/remove/<int:cart_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("product/<int:product_id>/review/", views.submit_review, name="submit_review"),
    path("add_product/", views.add_product_view, name="add_product"),
]
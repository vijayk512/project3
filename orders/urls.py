from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("menu", views.menu_view, name="menu"),
    path("hours", views.hours_view, name="hours"),
    path("contact_us", views.contact_us_view, name="contact_us"),
    path("orders", views.orders_view, name="orders"),
    path("checkout/<int:order_id>", views.checkout_view, name="checkout"),
    path("thank-you", views.thank_you_view, name="thank-you")
]

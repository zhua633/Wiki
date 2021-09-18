from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("item/<str:entry>", views.item, name="item"),
    path("NoEntry", views.NoEntry, name="NoEntry")

]

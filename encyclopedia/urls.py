from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("item/<str:entry>", views.item, name="item"),
    path("NoEntry", views.NoEntry, name="NoEntry"),
    path("searchresults",views.searchresults,name="searchresults"),
    path("NewPage", views.NewPage, name="NewPage"),
    path("RandomPage",views.RandomPage,name="RandomPage"),
    path("item/<str:entry>/EditPage",views.EditPage,name="EditPage")
]

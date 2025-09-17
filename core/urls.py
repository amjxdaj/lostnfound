from django.urls import path
from . import views

urlpatterns = [
    path('lost/new/', views.report_lost, name='report_lost'),
    path('found/new/', views.report_found, name='report_found'),
    path('lost/', views.lost_list, name='lost_list'),
    path('found/', views.found_list, name='found_list'),
    path('notifications/', views.notifications, name='notifications'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('base/', views.base, name='base'),
    path("notifications/mark-all-read/", views.mark_all_read, name="mark_all_read"),
    path("notifications/clear-all/", views.clear_all_notifications, name="clear_all_notifications"),
    path("notifications/<int:note_id>/mark-read/", views.mark_read, name="mark_read"),
    path("profile/", views.profile, name="profile"),
    path("lost/<int:item_id>/delete/", views.delete_lost_item, name="delete_lost_item"),
    path("found/<int:item_id>/delete/", views.delete_found_item, name="delete_found_item"),
    path("lost/<int:item_id>/", views.lost_detail, name="lost_detail"),
    path("found/<int:item_id>/", views.found_detail, name="found_detail"),

]

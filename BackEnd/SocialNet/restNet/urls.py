"""Modules with urls for rest api functions"""

from django.conf.urls import url
from restNet import views

urlpatterns = [
    url(r"^sign_up/$", views.sign_up),
    url(r"^sign_in/$", views.sign_in),
    url(r"^create_post/$", views.create_post),
    url(r"^get_posts/$", views.get_posts),
    url(r"^delete_post/$", views.delete_post),
    url(r"^edit_post/$", views.edit_post),
    url(r"^update_like/$", views.update_like)
]
from django.urls import path
from apps.accounts.views import sign_up_view, sign_in_view

urlpatterns = [
    path('sign-up/', sign_up_view, name='sign_up'),
    path('sign-in/', sign_in_view, name='sign_in'),
]

from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.api.accounnts_api.urls')),  # Authentication API
    path('projects/', include('apps.api.project_api.urls')),  # Projects API
    path('customers/', include('apps.api.customer_api.urls')),  # Customers API
    path('employees/', include('apps.api.employ_api.urls')),  # Employees API
    path('payments/', include('apps.api.payments_api.urls')),  # Payments API
    path('complains/', include('apps.api.complain_api.urls')), # Complains API
    path('chat/', include('apps.api.chat_api.urls')),  # Chat API
]



# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenRefreshView
# from django.urls import path,include
# from apps.accounts import views
# from apps.api.accounnts_api.views import SignUp_In


# router =DefaultRouter()

# router.register(r'auth', SignUp_In,basename='auth')

# urlpatterns=[
#     path('',include(router.urls)),
#     path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),

# ]
# # urlpatterns= router.urls
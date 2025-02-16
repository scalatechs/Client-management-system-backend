from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from django.urls import path,include
from apps.accounts import views
from apps.api.accounnts_api.views import SignUp_In


router =DefaultRouter()

router.register(r'', SignUp_In,basename='auth')

urlpatterns=[
    path('',include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),

]
# urlpatterns= router.urls
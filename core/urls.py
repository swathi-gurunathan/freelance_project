from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfileViewSet, ProjectViewSet, ProposalViewSet,
    MessageViewSet, ReviewViewSet, RegisterView, CreatePaymentIntentView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
]
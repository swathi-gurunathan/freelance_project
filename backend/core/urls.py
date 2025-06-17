from rest_framework.routers import DefaultRouter
from .views import SkillViewSet, ProfileViewSet, ProjectViewSet, ProposalViewSet, MessageViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'skills', SkillViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = router.urls
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TestViewSet, QuestionViewSet, ChoiceViewSet, SubmissionViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
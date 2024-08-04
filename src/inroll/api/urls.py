from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    CandidateViewSet,
    RecruiterViewSet, 
    TestViewSet, 
    QuestionViewSet, 
    ChoiceViewSet, 
    SubmissionViewSet,
    CandidateAssignedTests,
    RecruiterAvailableTests,
    CandidateSubmissions,
    GetRoutes,
    CorrectChoices,
)

router = DefaultRouter()
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'candidates', CandidateViewSet)
router.register(r'recruiters', RecruiterViewSet)

custom_urlpatterns = [
    path('questions/<int:pk>/correct-choices/', CorrectChoices.as_view(), name="correct-choices"),
]

custom_urlpatterns = format_suffix_patterns(custom_urlpatterns)

urlpatterns = [
    path('', GetRoutes.as_view(), name="root"),
    path('', include(router.urls)),
    path('', include(custom_urlpatterns)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('candidates/<int:candidate_id>/assigned-tests/', CandidateAssignedTests.as_view(), name='candidate-assigned-tests'),
    path('recruiters/<int:recruiter_id>/available-tests/', RecruiterAvailableTests.as_view(), name='recruiter-available-tests'),
    path('candidates/<int:candidate_id>/submissions/', CandidateSubmissions.as_view(), name='candidate-submissions'),
]
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    CandidateViewSet, RecruiterViewSet, CandidateAssignedTests, RecruiterAvailableTests, 
    TestViewSet, MultipleChoiceQuestionViewSet, OpenEndedQuestionViewSet,
    ChoiceViewSet, SubmissionViewSet, ChoiceAnswerViewSet, OpenEndedAnswerViewSet, CorrectChoices,
    CandidateSubmissions,
    GetRoutes,
    AssignTest,
    GetSubmission,
)

router = DefaultRouter()
router.register(r'tests', TestViewSet)
router.register(r'mc-questions', MultipleChoiceQuestionViewSet)
router.register(r'oe-questions', OpenEndedQuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'candidates', CandidateViewSet)
router.register(r'recruiters', RecruiterViewSet)
router.register(r'choice-answers', ChoiceAnswerViewSet)
router.register(r'oe-answers', OpenEndedAnswerViewSet)

custom_urlpatterns = [
    path('questions/<int:pk>/correct-choices/', CorrectChoices.as_view(), name="correct-choices"),
    path('candidates/<int:id>/assigned-tests/', CandidateAssignedTests.as_view(), name='candidate-assigned-tests'),
    path('candidates/<int:id>/submissions/', CandidateSubmissions.as_view(), name='candidate-submissions'),
    path('recruiters/<int:id>/available-tests/', RecruiterAvailableTests.as_view(), name='recruiter-available-tests'),
    path('assign-test', AssignTest.as_view(), name='assign-test'),
    path('get-submission/', GetSubmission.as_view(), name='get-submission')
]

custom_urlpatterns = format_suffix_patterns(custom_urlpatterns)

urlpatterns = [
    path('', GetRoutes.as_view(), name="root"),
    path('', include(router.urls)),
    path('', include(custom_urlpatterns)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
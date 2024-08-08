from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    Candidate, Recruiter, 
    Test, OpenEndedQuestion, MultipleChoiceQuestion, 
    Choice, Submission, ChoiceAnswer, OpenEndedAnswer, 
    UserTestMap,
)
from .serializers import (
    CandidateSerializer, RecruiterSerializer, 
    TestSerializer, MultipleChoiceQuestionSerializer, OpenEndedQuestionSerializer,
    ChoiceSerializer, SubmissionSerializer, ChoiceAnswerSerializer, OpenEndedAnswerSerializer,
)
from django.shortcuts import get_object_or_404

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class RecruiterViewSet(viewsets.ModelViewSet):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class MultipleChoiceQuestionViewSet(viewsets.ModelViewSet):
    queryset = MultipleChoiceQuestion.objects.all()
    serializer_class = MultipleChoiceQuestionSerializer

class OpenEndedQuestionViewSet(viewsets.ModelViewSet):
    queryset = OpenEndedQuestion.objects.all()
    serializer_class = OpenEndedQuestionSerializer

class CorrectChoices(APIView):
    def get(self, request, pk, format=None):
        question = get_object_or_404(MultipleChoiceQuestion, pk=pk)
        correct_choices = question.choices.filter(is_true=True)
        serializer = ChoiceSerializer(correct_choices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

# Do not forget to update this view in order to show all possible endpoints at root
class GetRoutes(APIView):
    def get(self, request):
        prefix = "http://localhost:8000/api/"
        apiroutes = [
            prefix+"tests/",
            prefix+"mc-questions/",
            prefix+"mc-questions/<int:pk>/correct-choices/",
            prefix+"oe-questions/",
            prefix+"choices/",
            prefix+"choice-answers/",
            prefix+"oe-answers",
            prefix+"submissions/",
            prefix+"candidates/",
            prefix+"candidates/<int:candidate_id>/assigned-tests/",
            prefix+"candidates/<int:candidate_id>/submissions/",
            prefix+"recruiters",
            prefix+"recruiters/<int:recruiter_id>/available-tests/",
            prefix+"token/",
            prefix+"token/refresh/",
        ]
        return Response(apiroutes)

class ChoiceAnswerViewSet(viewsets.ModelViewSet):
    queryset = ChoiceAnswer.objects.all()
    serializer_class = ChoiceAnswerSerializer

class OpenEndedAnswerViewSet(viewsets.ModelViewSet):
    queryset = OpenEndedAnswer.objects.all()
    serializer_class = OpenEndedAnswerSerializer

#Function for viewing all assigned tests for a specific candidate
class CandidateAssignedTests(APIView):
    def get(self, request, id, format=None):
        candidate = get_object_or_404(Candidate, id=id)
        assigned_test_ids = UserTestMap.objects.filter(candidate=candidate).values_list('test_id', flat=True)
        assigned_tests = Test.objects.filter(id__in=assigned_test_ids)

        serializer = TestSerializer(assigned_tests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Listing all available tests for recruiter without giving questions
class RecruiterAvailableTests(APIView):
    def get(self, request, id, format=None):
        recruiter = get_object_or_404(Recruiter, id=id)
        available_tests = Test.objects.filter(recruiter=recruiter)
        serializer = TestSerializer(available_tests, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

#Listing all of the submissions of a candidate
class CandidateSubmissions(APIView):
    def get(self, request, id, format=None):
        candidate = get_object_or_404(Candidate, id=id)
        submissions = Submission.objects.filter(candidate=candidate)
        serializer = SubmissionSerializer(submissions, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

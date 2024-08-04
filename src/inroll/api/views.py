from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Candidate, Recruiter, Test, Question, Choice, Submission, ChoiceAnswer, OpenEndedAnswer, UserTestMap
from .serializers import CandidateSerializer, RecruiterSerializer, TestSerializer, QuestionSerializer, ChoiceSerializer, SubmissionSerializer, ChoiceAnswerSerializer, OpenEndedAnswerSerializer
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

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class ChoiceAnswerViewSet(viewsets.ModelViewSet):
    queryset = ChoiceAnswer.objects.all()
    serializer_class = ChoiceAnswerSerializer

class OpenEndedAnswerViewSet(viewsets.ModelViewSet):
    queryset = OpenEndedAnswer.objects.all()
    serializer_class = OpenEndedAnswerSerializer

#Function for viewing all assigned tests for a specific candidate
class CandidateAssignedTests(APIView):
    def get(self, request, candidate_id):
        candidate = get_object_or_404(Candidate, id=candidate_id)
        assigned_test_ids = UserTestMap.objects.filter(candidate=candidate).values_list('test_id', flat=True)
        assigned_tests = Test.objects.filter(id__in=assigned_test_ids)

        serializer = TestSerializer(assigned_tests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Listing all available tests for recruiter without giving questions
class RecruiterAvailableTests(APIView):
    def get(self, request, recruiter_id):
        recruiter = get_object_or_404(Recruiter, id=recruiter_id)
        available_tests = Test.objects.filter(recruiter=recruiter)
        serializer = TestSerializer(available_tests, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

#Listing all of the submissions of a candidate
class CandidateSubmissions(APIView):
    def get(self, request, candidate_id):
        candidate = get_object_or_404(Candidate, id=candidate_id)
        submissions = Submission.objects.filter(candidate=candidate)
        serializer = SubmissionSerializer(submissions, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
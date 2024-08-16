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
    AssignTestSerializer,
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        test_id = serializer.validated_data.get('test')
        candidate_id = serializer.validated_data.get('candidate')
        test = get_object_or_404(Test, id=test_id)
        candidate = get_object_or_404(Candidate, id=candidate_id)

        submission, created = Submission.objects.get_or_create(test=test, candidate=candidate)

        if created:
            return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)
        else:
            return Response(SubmissionSerializer(submission).data, status=status.HTTP_200_OK)

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
            prefix+"get-submission/?candidate=<int:candidate_id>&test=<int:test_id>",
            prefix+"candidates/",
            prefix+"candidates/<int:id>/assigned-tests/",
            prefix+"candidates/<int:id>/submissions/",
            prefix+"recruiters",
            prefix+"recruiters/<int:id>/available-tests/",
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


class AssignTest(APIView):
    def post(self, request, format=None):
        serializer = AssignTestSerializer(data=request.data)
        if serializer.is_valid():
            candidate_id = serializer.validated_data['candidate'].id
            test_id = serializer.validated_data['test'].id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class GetSubmission(APIView):
    def get(self, request, format=None):
        candidate_id = request.query_params.get('candidate')
        test_id = request.query_params.get('test')

        if not candidate_id or not test_id:
            return Response(
                {'detail' : 'ID missing'},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        candidate = get_object_or_404(Candidate, id=candidate_id)
        test = get_object_or_404(Test, id=test_id)

        submission = Submission.objects.filter(candidate=candidate, test=test).first() # Might need a better solution

        if not submission:
            return Response(
                {'detail' : 'Submission does not exist'},
                status = status.HTTP_404_NOT_FOUND
            )

        serializer = SubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_200_OK)
            

        
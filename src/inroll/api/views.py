from rest_framework import viewsets
from .models import User, Test, Question, Choice, Submission, ChoiceAnswer, OpenEndedAnswer
from .serializers import UserSerializer, TestSerializer, QuestionSerializer, ChoiceSerializer, SubmissionSerializer, ChoiceAnswerSerializer, OpenEndedAnswerSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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

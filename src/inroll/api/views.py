from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User, Test, Question, Choice, Submission, Answer
from .serializers import UserSerializer, TestSerializer, QuestionSerializer, ChoiceSerializer, SubmissionSerializer, AnswerSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class CorrectChoicesAPIView(APIView):
    def get(self, request, pk, format=None):
        question = get_object_or_404(Question, pk=pk)
        correct_choices = question.choices.filter(is_true=True)
        serializer = ChoiceSerializer(correct_choices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

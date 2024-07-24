from rest_framework import serializers
from .models import User, Test, Question, Choice, Submission, ChoiceAnswer, OpenEndedAnswer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role']

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'content', 'is_true']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'test', 'body', 'question_type', 'choices']

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'type', 'questions']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'user']

class ChoiceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceAnswer
        fields = ['id', 'submission', 'choice']

class OpenEndedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenEndedAnswer
        fields = ['id', 'submission', 'question', 'response']
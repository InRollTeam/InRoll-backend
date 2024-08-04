from rest_framework import serializers
from .models import Test, Question, Choice, Submission, ChoiceAnswer, OpenEndedAnswer, Candidate, Recruiter, Answer

# Test related serializers
class ChoiceSerializer(serializers.ModelSerializer):
    is_true = serializers.BooleanField(write_only=True)

    class Meta:
        model = Choice
        fields = ['id', 'question', 'body', 'is_true']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'test', 'body', 'question_type', 'choices']

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ['id', 'recruiter', 'duration', 'until_date', 'title', 'body', 'questions']

# Answer serializers
class ChoiceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceAnswer
        fields = ['id', 'submission', 'question', 'choice']

class OpenEndedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenEndedAnswer
        fields = ['id', 'submission', 'question', 'response']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'submission', 'question']

    def to_representation(self, instance):
        if isinstance(instance, ChoiceAnswer):
            return ChoiceAnswerSerializer(instance).data
        elif isinstance(instance, OpenEndedAnswer):
            return OpenEndedAnswerSerializer(instance).data
        return super().to_representation(instance)

class SubmissionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Submission
        fields = ['id', 'user', 'answers']

# User serializers
class CandidateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Candidate
        fiels = ['id', 'password', 'email', 'phone_number', 'first_name', 'last_name']

class RecruiterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Recruiter
        fiels = ['id', 'password', 'email', 'phone_number', 'first_name', 'last_name', 'company_name']
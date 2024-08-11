from rest_framework import serializers
from .models import (
    Candidate, Recruiter,
    Test, MultipleChoiceQuestion, OpenEndedQuestion, 
    Choice, Submission, ChoiceAnswer, OpenEndedAnswer, 
    UserTestMap,
)

# Test related serializers
class ChoiceSerializer(serializers.ModelSerializer):
    is_true = serializers.BooleanField(write_only=True)

    class Meta:
        model = Choice
        fields = ['id', 'question', 'body', 'is_true']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = ['id', 'test', 'body']

class MultipleChoiceQuestionSerializer(QuestionSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = MultipleChoiceQuestion
        fields = QuestionSerializer.Meta.fields + ['choices']

class OpenEndedQuestionSerializer(QuestionSerializer):
    class Meta:
        model = OpenEndedQuestion
        fields = QuestionSerializer.Meta.fields

class TestSerializer(serializers.ModelSerializer):
    multiple_choice_questions = MultipleChoiceQuestionSerializer(many=True, read_only=True)
    open_ended_questions = OpenEndedQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'recruiter', 'duration', 'until_date', 'title', 'body', 'multiple_choice_questions', 'open_ended_questions']

# Answer serializers
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = ['id', 'submission', 'question']

class ChoiceAnswerSerializer(AnswerSerializer):
    class Meta(AnswerSerializer.Meta):
        model = ChoiceAnswer
        fields = AnswerSerializer.Meta.fields + ['choice']

class OpenEndedAnswerSerializer(AnswerSerializer):
    class Meta(AnswerSerializer.Meta):
        model = OpenEndedAnswer
        fields = AnswerSerializer.Meta.fields + ['response']

class SubmissionSerializer(serializers.ModelSerializer):
    choice_answers = ChoiceAnswerSerializer(many=True, read_only=True)
    open_ended_answers = OpenEndedAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'candidate', 'test', 'date', 'choice_answers', 'open_ended_answers']

# User serializers
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = None
        fields = ['id', 'password', 'email', 'phone_number', 'first_name', 'last_name']

    def validate(self, data):
        email = data.get('email')
        phone_number = data.get('phone_number')
        if Recruiter.objects.filter(email=email).exists() or Candidate.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'This email is already in use.'})
        if Recruiter.objects.filter(phone_number=phone_number).exists() or Candidate.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({'phone_number': 'This phone number is already in use.'})
        return data

class CandidateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Candidate
        fields = UserSerializer.Meta.fields

class RecruiterSerializer(UserSerializer):
    class Meta:
        model = Recruiter
        fields = UserSerializer.Meta.fields + ['company_name']


class AssignTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTestMap
        fields = ['candidate', 'test', 'duration']
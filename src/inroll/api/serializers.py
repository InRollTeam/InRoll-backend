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
    order = serializers.IntegerField(read_only=True)

    class Meta:
        model = None
        fields = ['id', 'test', 'body', 'order']

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
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'recruiter', 'duration', 'until_date', 'title', 'body', 'questions']

    def get_questions(self, obj):
        multiple_choice_questions = MultipleChoiceQuestionSerializer(obj.multiple_choice_questions.all(), many=True).data
        open_ended_questions = OpenEndedQuestionSerializer(obj.open_ended_questions.all(), many=True).data
        unordered_questions = multiple_choice_questions + open_ended_questions
        ordered_questions = sorted(unordered_questions, key=lambda question: question['order'])

        return ordered_questions

    def create(self, validated_data):
        questions_data = self.initial_data.get('questions')
        test = Test.objects.create(**validated_data)
        
        for index, question_data in enumerate(questions_data, start=1):
            question_data['order'] = index
            choices_data = question_data.pop('choices', None)
            
            if choices_data:
                multiple_choice_question = MultipleChoiceQuestion.objects.create(test=test, **question_data)
                for choice_data in choices_data:
                    Choice.objects.create(question=multiple_choice_question, **choice_data)
            else:
                OpenEndedQuestion.objects.create(test=test, **question_data)
                
        return test

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
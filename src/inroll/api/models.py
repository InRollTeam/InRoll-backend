from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# We will use django-phonenumber-field library for phone_number instead of IntegerField
# We will use django-tinymce library for body attributes instead of TextArea (it has HTMLField)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, phone_number=None, first_name=None, last_name=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            role=role,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role='admin', phone_number=None, first_name=None, last_name=None):
        user = self.create_user(
            email,
            password=password,
            role=role,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone_number = models.PositiveBigIntegerField(unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        abstract = True

    def __str__(self):
        return self.email
    
class Recruiter(User):
    company_name = models.CharField(max_length=255)

class Candidate(User):
    pass

class Test(models.Model):
    recruiter = models.ForeignKey(Recruiter, related_name="created_tests", on_delete=models.CASCADE)
    duration = models.DurationField()
    until_date = models.DateTimeField()
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.title
    
class UserTestMap(models.Model):
    candidate = models.ForeignKey(Candidate, related_name="assigned_tests", on_delete=models.CASCADE)
    test = models.ForeignKey(Test, related_name="candidates", on_delete=models.CASCADE)
    duration = models.DurationField()

class Question(models.Model):
    MULTIPLE_CHOICE = 'MC'
    OPEN_ENDED = 'OE'
    QUESTION_TYPE_CHOICES = [
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (OPEN_ENDED, 'Open Ended'),
    ]

    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    body = models.TextField()
    question_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPE_CHOICES,
        default=MULTIPLE_CHOICE,
    )

    def __str__(self):
        return self.body

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    body = models.TextField()
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.body

class Submission(models.Model):
    candidate = models.ForeignKey(Candidate, related_name="made_submissions", on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    date = models.DateTimeField()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class ChoiceAnswer(Answer):
    submission = models.ForeignKey(Submission, related_name='choice_answers', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.submission} - {self.choice.question} - {self.choice}"
    
class OpenEndedAnswer(Answer):
    submission = models.ForeignKey(Submission, related_name='open_ended_answers', on_delete=models.CASCADE)
    response = models.TextField()

    def __str__(self):
        return f"{self.submission} - {self.question} - {self.response}"
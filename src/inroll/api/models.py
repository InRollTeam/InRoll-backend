from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=255)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Test(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.body

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    content = models.TextField()
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.content

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Answer(models.Model):
    submission = models.ForeignKey(Submission, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.submission} - {self.question} - {self.choice}"

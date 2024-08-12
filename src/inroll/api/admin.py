from django.contrib import admin
from .models import MultipleChoiceQuestion, OpenEndedQuestion

# Register your models here.
admin.site.register(MultipleChoiceQuestion)
admin.site.register(OpenEndedQuestion)
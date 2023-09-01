from django.db import models

class Questions(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Date Published")

class Choices(models.Model):
    question = models.ForeignKey(Questions, on_delete = models.CASCADE)
    choice_test = models.CharField(max_length=200)
    
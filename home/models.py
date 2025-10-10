from django.db import models

import random
from datetime import datetime

def generate_user_id():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # 14 digits
    random_part = random.randint(100, 999)               # 3 digits
    return int(f"{timestamp}{random_part}")              # Returns 17-digit integer

class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True, default=generate_user_id)
    user_name = models.CharField(max_length=50, unique=True)
    user_password = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50, unique=True)
    user_role = models.CharField(max_length=20)
    user_status = models.CharField(max_length=20) # either active or inactive # new change
    class Meta:
        db_table = 'table_users'
        managed = False


class Author(models.Model):
    author_id = models.BigIntegerField(primary_key=True, default=generate_user_id) 
    author_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    author_name = models.CharField(max_length=50)
    author_full_name = models.CharField(max_length=50)
    author_email = models.CharField(max_length=50)
    author_subject_a = models.CharField(max_length=50, blank=True)
    author_subject_b = models.CharField(max_length=50, blank=True)
    author_subject_c = models.CharField(max_length=50, blank=True)
    author_subject_d = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'table_authors'
        managed = False


class Participant(models.Model):
    participant_id = models.BigIntegerField(primary_key=True, default=generate_user_id)
    participant_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    participant_name = models.CharField(max_length=50)
    participant_full_name = models.CharField(max_length=50)
    participant_email = models.CharField(max_length=50)
    preferred_subject_a = models.CharField(max_length=50, blank=True)
    preferred_subject_b = models.CharField(max_length=50, blank=True)
    preferred_subject_c = models.CharField(max_length=50, blank=True)
    preferred_subject_d = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'table_participants'
        managed = False

class Quiz(models.Model):
    quiz_id = models.BigIntegerField(primary_key=True, default=generate_user_id)
    quiz_author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='quiz_author_id')
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        db_table = 'table_quizzes'
        managed = False


class Question(models.Model):
    question_id = models.BigIntegerField(primary_key=True, default=generate_user_id)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, db_column='quiz_id')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1)

    class Meta:
        db_table = 'table_questions'
        managed = False


class QuizParticipant(models.Model):
    qp_id = models.BigIntegerField(primary_key=True, default=generate_user_id)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, db_column='quiz_id')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, db_column='participant_id')
    joined_date = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0.0)

    class Meta:
        db_table = 'table_quiz_participants'
        managed = False


class Rating(models.Model):
    rating_id = models.BigIntegerField(primary_key=True, default=generate_user_id)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, db_column='quiz_id')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, db_column='participant_id')
    rating_value = models.IntegerField(default=0)  # 1–5
    feedback = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'table_ratings'
        managed = False
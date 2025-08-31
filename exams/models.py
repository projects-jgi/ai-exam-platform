from django.db import models
from core.models import User, StudentGroup

class Exam(models.Model):
    EXAM_STATUS = (
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type__in': ['faculty', 'hod', 'admin']})
    allowed_groups = models.ManyToManyField(StudentGroup, related_name='exams')
    
    # Timing controls
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(help_text="Exam duration in minutes")
    
    # Exam settings
    max_attempts = models.PositiveIntegerField(default=1)
    shuffle_questions = models.BooleanField(default=False)
    show_results_after = models.BooleanField(default=False)
    is_proctored = models.BooleanField(default=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=EXAM_STATUS, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    class Meta:
        ordering = ['-created_at']


class Question(models.Model):
    QUESTION_TYPES = (
        ('mcq', 'Multiple Choice (MCQ)'),
        ('coding', 'Coding Problem'),
        ('descriptive', 'Descriptive Answer'),
        ('file_upload', 'File Upload'),
    )
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    
    # For coding questions
    code_template = models.TextField(blank=True, help_text="Initial code template for coding questions")
    test_cases = models.JSONField(blank=True, null=True, help_text="JSON structure for test cases")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}..."

    class Meta:
        ordering = ['order']


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options', limit_choices_to={'question_type': 'mcq'})
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Option {self.order}: {self.option_text[:30]}..."

    class Meta:
        ordering = ['order']


class ExamAttempt(models.Model):
    ATTEMPT_STATUS = (
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('timed_out', 'Timed Out'),
        ('violation', 'Violation Detected'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'}, related_name='exam_attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    attempt_number = models.PositiveIntegerField(default=1)
    
    # Timing tracking
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    actual_duration = models.PositiveIntegerField(null=True, blank=True, help_text="Actual time taken in minutes")
    
    # Proctoring data
    violation_count = models.PositiveIntegerField(default=0)
    screen_switch_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=ATTEMPT_STATUS, default='in_progress')
    
    # Results
    score = models.FloatField(null=True, blank=True)
    max_score = models.PositiveIntegerField(null=True, blank=True)
    
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                  limit_choices_to={'user_type__in': ['faculty', 'hod']}, related_name='reviewed_attempts')
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.email} - {self.exam.title} - Attempt {self.attempt_number}"

    class Meta:
        unique_together = ['student', 'exam', 'attempt_number']


class Answer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    # Different answer types
    mcq_answer = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    descriptive_answer = models.TextField(blank=True)
    code_answer = models.TextField(blank=True)
    file_answer = models.FileField(upload_to='exam_answers/', null=True, blank=True)
    
    # Grading
    is_correct = models.BooleanField(null=True, blank=True)
    points_awarded = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer for {self.question} by {self.attempt.student.email}"

    class Meta:
        unique_together = ['attempt', 'question']
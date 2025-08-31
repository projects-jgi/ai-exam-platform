from rest_framework import serializers
from .models import Exam, Question, Option, ExamAttempt, Answer

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct', 'order']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'exam', 'question_text', 'question_type', 'points', 'order', 
                 'code_template', 'test_cases', 'options', 'created_at']

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    created_by_name = serializers.SerializerMethodField(read_only=True)
    
    def get_created_by_name(self, obj):
        """Return creator's full name or email if name not available"""
        return obj.created_by.get_full_name() or obj.created_by.email
    
    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'created_by', 'created_by_name', 
                 'start_time', 'end_time', 'duration_minutes', 'max_attempts',
                 'shuffle_questions', 'show_results_after', 'is_proctored',
                 'status', 'questions', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'status']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'attempt', 'question', 'mcq_answer', 'descriptive_answer',
                 'code_answer', 'file_answer', 'points_awarded', 'feedback', 'submitted_at']
        read_only_fields = ['attempt', 'points_awarded', 'feedback']

class ExamAttemptSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    student_name = serializers.SerializerMethodField(read_only=True)
    
    def get_student_name(self, obj):
        """Return student's full name or email if name not available"""
        return obj.student.get_full_name() or obj.student.email
    
    class Meta:
        model = ExamAttempt
        fields = ['id', 'student', 'student_name', 'exam', 'attempt_number',
                 'start_time', 'end_time', 'actual_duration', 'violation_count',
                 'screen_switch_count', 'status', 'score', 'max_score', 'answers']
        read_only_fields = ['student', 'score', 'max_score']
from django.contrib import admin
from .models import Exam, Question, Option, ExamAttempt, Answer

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'start_time', 'end_time', 'status', 'is_proctored']
    list_filter = ['status', 'is_proctored', 'created_by', 'allowed_groups']
    filter_horizontal = ['allowed_groups']  # Better widget for selecting groups
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    
    # Display related questions in admin
    def questions_count(self, obj):
        return obj.questions.count()
    questions_count.short_description = 'Questions'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['exam', 'question_type', 'points', 'order', 'created_at']
    list_filter = ['question_type', 'exam', 'exam__created_by']
    search_fields = ['question_text', 'exam__title']
    ordering = ['exam', 'order']
    
    # Display options count for MCQ questions
    def options_count(self, obj):
        if obj.question_type == 'mcq':
            return obj.options.count()
        return 'N/A'
    options_count.short_description = 'Options'


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['question', 'option_text', 'is_correct', 'order']
    list_filter = ['question__exam', 'is_correct']
    search_fields = ['option_text', 'question__question_text']
    list_editable = ['is_correct', 'order']  # Edit directly from list view


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'attempt_number', 'status', 'score', 'violation_count']
    list_filter = ['status', 'exam', 'student__studentprofile__group']
    search_fields = ['student__email', 'exam__title']
    readonly_fields = ['start_time', 'actual_duration']
    
    # Add action for bulk status update
    actions = ['mark_as_reviewed']
    
    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(status='submitted', reviewed_by=request.user)
        self.message_user(request, f"{updated} attempts marked as reviewed.")
    mark_as_reviewed.short_description = "Mark selected attempts as reviewed"


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):  # Fixed: Changed admin.Model to admin.ModelAdmin
    list_display = ['attempt', 'question', 'points_awarded', 'submitted_at']
    list_filter = ['question__question_type', 'attempt__exam']
    search_fields = ['attempt__student__email', 'question__question_text']
    readonly_fields = ['submitted_at']
    
    # Make it easy to filter by exam
    def exam_name(self, obj):
        return obj.attempt.exam.title
    exam_name.short_description = 'Exam'
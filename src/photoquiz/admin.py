from django.contrib import admin
from photoquiz.models import Quiz, Event, Answer


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description', 'created_at',)
    
class EventAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'image_url', 'question',)
    
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('event', 'answer_text', 'is_correct', 'correct_answer_text', )

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Answer, AnswerAdmin)

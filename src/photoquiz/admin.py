

from django.contrib import admin 
from . import models



    
class AnswerInlineModel(admin.TabularInline):
    model = models.Answer
    fields = [
        'event',
        'answer_text',
        'is_correct',
        'correct_answer_text'
    ]
    
class EventInlineModel(admin.TabularInline):
    model = models.Event
    fields = [
        'question',
        'image_url',    
        
    ]
    inlines = [AnswerInlineModel]
    
    


@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'slug',
        'created_at'
    ]
    list_display_links = ['title']
    inlines = [
        EventInlineModel,
     
        ]
    
    

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'quiz',
        'question',
        'image_url',
        
    ]
    inlines = [
        AnswerInlineModel,
    ]
@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'event', 
        'answer_text', 
        'is_correct',
        'correct_answer_text'
    ]


from django.db import models
from django.utils.text import slugify



class Quiz(models.Model):
    title = models.CharField(max_length=100, verbose_name= 'Title')
    slug = models.SlugField(blank=True)
    description = models.CharField(max_length= 250, verbose_name= 'Description')
    time_limit_minutes = models.PositiveBigIntegerField(default=10, verbose_name= 'Time Limit (minutes)')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = 'Quiz'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def total_questions(self):
        return self.events.count()
    
    def calculate_average_score(self, correct_answers):
        if self.total_questions() > 0:
            return (correct_answers/self.total_questions()) * 100
        return 0
        
            
        
    
class Event(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='events')
    image_url = models.URLField(verbose_name='Image Url')
    question = models.CharField(max_length= 250, verbose_name = 'Question')
    
    class Meta:
        verbose_name = 'Event'
        
    def __str__(self):
        return self.question
    
class Answer(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name = 'answers')
    answer_text = models.CharField(max_length=100, verbose_name= 'Answer')
    is_correct = models.BooleanField(default=False, verbose_name='Is Correct')
    correct_answer_text = models.TextField(default=False, verbose_name='Caption') # ajout la légende correspondant à l'image proposée

    class Meta:
        verbose_name = 'Answer'
        
    def __str__(self):
        return self.answer_text    

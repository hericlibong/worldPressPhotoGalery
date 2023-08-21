from typing import Any, Dict
from django.shortcuts import redirect, render, get_object_or_404
from .models import Quiz, Answer
from .forms import QuizForm
from django.core.paginator import Paginator
from django.views.generic import ListView
from photoquiz.models import Quiz



class QuizListView(ListView):
    model = Quiz
    template_name = 'photoquiz/quiz_list.html'
    context_object_name = 'quizzes'
    
    def get_queryset(self):
        return Quiz.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_images = {}
        
        for quiz in context['quizzes']:
            if quiz.events.exists():
                event = quiz.events.first()  # Prenez la première instance d'événement liée au quiz
                event_images[quiz.id] = event.image_url
                
        context['event_images'] = event_images       
        return context
                
    
    




def quiz_detail_view(request, slug, event_number=1):
    quiz = get_object_or_404(Quiz, slug=slug)
    events = quiz.events.all()
    
    paginator = Paginator(events, per_page = 1)
    event_page = int(event_number)
    current_event_page = paginator.get_page(event_page)
    current_event = current_event_page[0]
    
    total_questions = quiz.total_questions()

    if request.method == 'POST':
        form = QuizForm(event_list = [current_event], data=request.POST)
        if form.is_valid():
            selected_answer_id = form.cleaned_data[f'event_{current_event.id}']
            selected_answer = get_object_or_404(Answer, id=selected_answer_id)

            if selected_answer.is_correct:
                success_message = "Well Done !! "
                correct_answer_text = selected_answer.correct_answer_text  # Légende de la réponse correcte
                current_event.success_message = success_message
                current_event.correct_answer_text = correct_answer_text
                
                if 'correct_answers' not in request.session:
                    request.session['correct_answers'] = 0
                request.session['correct_answers'] += 1   
                
            else:
                error_message = "Dommage, ce n'est pas la bonne réponse."
                current_event.error_message = error_message
                correct_answer = current_event.answers.get(is_correct=True)  # Obtenir la réponse correcte
                current_event.correct_answer_text = correct_answer.correct_answer_text 
            current_event.submitted = True  # Marquer l'événement comme soumis
            current_event.save()  # Enregistrer les modifications dans la base de données    

    else:

        form = QuizForm(event_list=[current_event])

    
    context = {
        'quiz':quiz,
        'current_event_page': current_event_page,
        'current_event':current_event,
        'form':form,
        'event_page':event_page,
        'total_pages':paginator.num_pages,
        }

    return render(request, 'photoquiz/quiz_detail.html', context)


def quiz_final_view(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug)

    # ... (autres parties de la vue)

    # Calcul de la note moyenne (average_score)
    correct_answers = request.session.get('correct_answers', 0)
    average_score = quiz.calculate_average_score(correct_answers)

    # Messages en fonction de la note moyenne
    if average_score < 50:
        message = "Vous pouvez faire mieux !"
    elif average_score == 50:
        message = "Juste la moyenne !"
    elif 50 < average_score < 70:
        message = "Pas mal, continuez à vous améliorer !"
    else:
        message = "Excellent travail, vous êtes un expert !"

    context = {
        'quiz': quiz,
        'average_score': average_score,
        'message': message,
    }

    return render(request, 'photoquiz/quiz_final.html', context)









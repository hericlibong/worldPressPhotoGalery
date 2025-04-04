from django import forms
from photoquiz.models import Answer

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        event_list = kwargs.pop('event_list')
        super(QuizForm, self).__init__(*args, **kwargs)

        for event in event_list:
            self.fields[f'event_{event.id}'] = forms.ChoiceField(
                choices=[(answer.id, answer.answer_text) for answer in event.answers.all()],
                widget=forms.RadioSelect,
                label=event.question
            )

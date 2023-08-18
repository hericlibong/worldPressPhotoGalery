from django import forms

class ImageSearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=False, label='Keyword')
    search_field = forms.ChoiceField(choices=[
        ('caption', 'Caption'), 
        ('media', 'Media'),
        ('credits', 'Credits'),
        ('author', 'Author'),
    ], required=False, label='Search On :')
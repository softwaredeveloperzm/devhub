from django import forms
from .models import questions, Comment 
from ckeditor.fields import RichTextFormField



class QuestionForm(forms.ModelForm):
    class Meta:
        model = questions
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):    
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')


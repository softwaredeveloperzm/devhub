from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import questions
from .forms import QuestionForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.db.models import F
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .utils import get_client_ip
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import timedelta

def all_questions(request):

    #Get Total number of users available
    total_users = User.objects.count()
    print(total_users)
    # Get the search term from the query parameters
    q = request.GET.get('q', None)

    if q:
        # If there's a search term, filter the questions based on the title
        question_list = questions.objects.filter(title__icontains=q).order_by('-date_created')
    else:
        # If no search term, get all questions ordered by date_created
        question_list = questions.objects.order_by('-date_created')

    count = question_list.count()

    # Get the current page number from the query parameters, default to 1 if not provided
    page = request.GET.get('page', 1)

    # Number of questions to show per page
    questions_per_page = 10
    paginator = Paginator(question_list, questions_per_page)

    try:
        questions_paginated = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions_paginated = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        questions_paginated = paginator.page(paginator.num_pages)

    # Your existing logic for processing questions and updating counts
    for question in questions_paginated:
        user_ip = get_client_ip(request)
        if user_ip not in question.ip_address:
            question.ip_address += f"{user_ip},"
            question.views_count += 1
            question.save()

    return render(request, 'base/questions.html', {'questions': questions_paginated, 'total_users': total_users, 'total_questions': count, 'search_term': q})



def question_detail(request, slug):
    question = get_object_or_404(questions, slug=slug)
    comments = question.comments.all() 
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.questions = question  # Set the question for the new comment
            new_comment.save()
            comment_form = CommentForm()  # Reset the form after successful submission
            return redirect('question_detail', slug=slug)

    else:
        comment_form = CommentForm()

    return render(request, 'base/question_detail.html', {'question': question, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})
    
@login_required(login_url='users:signin')
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('base:all_questions')
    else:
        form = QuestionForm

    return render(request, 'base/ask.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class QuestionUpdateView(UpdateView):
    model = questions
    form_class = QuestionForm
    template_name = 'base/question_update.html'  # Create this template for the update view
    def get_success_url(self):
            question = get_object_or_404(questions, slug=self.kwargs['slug'])
            return reverse_lazy('base:question_detail', kwargs={'slug': question.slug})
    def get_object(self, queryset=None):
        obj = super(QuestionUpdateView, self).get_object(queryset=queryset)
        if obj.user != self.request.user:
            # If the logged-in user is not the owner of the question, deny access
            raise PermissionDenied
        return obj
    

def delete_question(request, slug):
    # Use the correct model name (questions) instead of 'Question'
    question = get_object_or_404(questions, slug=slug)

    if request.method == 'POST':
        question.delete()
        return redirect('base:all_questions')


def like_view(request, pk):
    post = get_object_or_404(questions, id=request.POST.get('question_id'))
    liked = False
    if post.likes.filter(id.request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('base:question_details'))


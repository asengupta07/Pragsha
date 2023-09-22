
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from .forms import AnswerForm

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'quora/question_list.html', {'questions': questions})

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm()
    return render(request, 'quora/question_detail.html', {'question': question, 'answers': answers, 'form': form})

# Create your views here.

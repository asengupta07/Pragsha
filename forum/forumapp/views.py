

from django.shortcuts import render, redirect
from .models import Thread, Post
from django.contrib.auth.decorators import login_required
from .utils import is_spam

def forum(request):
    threads = Thread.objects.all()
    return render(request, 'forumapp/forumIndex.html', {'threads': threads})

@login_required
def create_thread(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        thread = Thread.objects.create(title=title, created_by=request.user)
        Post.objects.create(thread=thread, author=request.user, content=content)
        return redirect('forumapp')
    return render(request, 'forumapp/create_thread.html')

@login_required
def thread_detail(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    posts = Post.objects.filter(thread=thread)
    return render(request, 'forumapp/thread_detail.html', {'thread': thread, 'posts': posts})



def create_post(request):
    if request.method == 'POST':
        content = request.POST['content']
        
        
        if is_spam(request, content):
            
            pass
        else:
            
            Post.objects.create(content=content)
        
        return redirect('forum')
    
    return render(request, 'forumapp/create_post.html') # arnab we need to make a create_post.html

# Create your views here.

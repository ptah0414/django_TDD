from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from board.forms import PostForm
from board.models import Post
from django.contrib import messages


@login_required(login_url='/accounts/login')
def create(request):
    if request.method == 'GET':
        postForm = PostForm()
        return render(request, 'board/create.html', {'postForm': postForm})

    elif request.method == 'POST':
        postForm = PostForm(request.POST)
        context = {'postForm': postForm, 'has_error': False}
        post = Post()
        post.title = request.POST.get('title')
        if len(post.title) < 5:
            messages.add_message(request, messages.ERROR, '제목은 5글자 이상이어야 합니다.')
            context['has_error'] = True
        post.contents = request.POST.get('contents')
        post.writer = request.user
        if context['has_error']:
            return render(request, 'board/create.html', context, status=400)
        post.save()
        return redirect('/board/read' + str(post.id))


def read(request, bid):
    post = Post.objects.get(id=bid)

    context = {'post': post}
    return render(request, 'board/read.html', context)
from django.shortcuts import render,  get_object_or_404
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.

def post_list(request):
    posts = Post.objects.all()

    context = {
        "posts": posts
    }

    return render(request, "blog/post_list.html", context)





def post_detail(request, pk):
    post = get_object_or_404(Post,pk=pk)

    context={
        "post":post
    }

    return render (request, "blog/post_detail.html",context)





@login_required
def post_create(request):

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, "Post created successfully!")

            return redirect("post_list")

    else:
        form = PostForm()

    return render(request, "blog/post_form.html", {
        "form": form
    })







@login_required
def post_update(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        

        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=post.pk)

    else:
        form = PostForm(instance=post)

    context = {
        "form": form
    }

    return render(request, "blog/post_form.html", context)








@login_required
def post_delete(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == "POST":
        post.delete()

        messages.success(request, "Post deleted successfully!")

        return redirect("post_list")

    return render(request, "blog/post_confirm_delete.html", {"post": post})
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
from .forms import PostForm, CreateUserForm
from .models import Post

def user_create(request):
    form = CreateUserForm(request.POST)
    print request.POST
    if form.is_valid():
        print "valid"
        # instance = form.save(commit=False)
        # instance.user = request.user
        form.save()
        messages.success(request, "User Successfuly Created")
        return redirect("list")
    context = {
        "form": form,
    }
    return render(request, "user_create.html", context)

def post_create(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfuly Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_detail(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft:
        if not request.user.is_authenticated():
            raise Http404
    context = {
        "title": "Detail",
        "instance": instance,
    }
    return render(request, "post_detail.html", context)

def post_list(request):
    queryset = Post.objects.active()
    dashboard = Post.objects.dashboard(user=request.user)
    query = request.GET.get("query")
    if query:
        queryset = queryset.filter(
        Q(title__icontains=query)|
        Q(content__icontains=query)
        ).distinct()
    context = {
        "object_list": queryset,
        "title": "List"
    }
    return render(request, "post_list.html", context)

def post_update(request, slug=None):
    if not request.user.is_authenticated():
        messages.error(request, "Please log in to update a post")
        return redirect('/login')
    instance = get_object_or_404(Post, slug=slug)
    if not request.user == instance.user:
        messages.error(request, "Please log in as the correct user to update a post")
        return redirect('/login')
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfuly Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, slug=None):
    if not request.user.is_authenticated():
        messages.error(request, "Please log in to update a post")
        return redirect('/login')
    instance = get_object_or_404(Post, slug=slug)
    if not request.user == instance.user:
        messages.error(request, "Please log in as the correct user to delete a post")
        return redirect('/login')
    instance.delete()
    messages.success(request, "Successfuly Deleted")
    return redirect("list")

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormMixin

from .forms import CreateArticleForm, CommentForm
from .models import Article, Comment
from datetime import datetime


class WelcomePage(View):
    def get(self, request, *args, **kwargs):
        return render(request, "main/base.html")


class AllPublication(ListView):
    model = Article
    template_name = 'main/publications.html'
    paginate_by = 15

    def get_queryset(self):
        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
            object_list = Article.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            ).order_by('-pub_date')
            return object_list
        object_list = Article.objects.all().order_by('-pub_date')
        return object_list


class OnePublication(FormMixin, DetailView):
    model = Article
    template_name = 'main/post_detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.article_comment.order_by('-comment_date')
        return context

    def get_success_url(self):
        return reverse('main:detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.article = self.get_object()
        form.comment_author = self.request.user
        form.comment_date = datetime.now()
        form.save()
        return super().form_valid(form)


class MySignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('main:login')
    template_name = 'main/signup.html'


class PersonalPage(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()

        publications = Article.objects.filter(author=request.user).order_by('-pub_date')
        context = {'publications': publications}
        return render(request, "main/person.html", context)


class CreatePublicationView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        form = CreateArticleForm()
        context = {"form": form}
        return render(request, "main/create_article.html", context)

    def post(self, request, *args, **kwargs):
        data = request.POST
        author = get_object_or_404(User, id=request.user.id)
        form = CreateArticleForm(data or None)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = author
            article.pub_date = datetime.now()
            article.save()
            return redirect('main:person')

        context = {"form": form}
        return render(request, "main/create_article.html", context)


class ArticleEdit(UpdateView):
    model = Article
    template_name = 'main/edit.html'
    fields = ['title', 'body']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)


class ArticleDelete(DeleteView):
    model = Article
    template_name = 'main/delete.html'
    success_url = reverse_lazy('main:person')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)


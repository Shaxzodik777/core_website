from django.shortcuts import render, redirect
from .models import Article, Category, Comment, Like, Dislike
from .forms import LoginForm, RegistrationForm, CommentForm, ArticleForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.models import User
from django .db.models import Q
# DetailView
# Create your views here.

# Мухаммедов Миразиз, Корчиев Шахзод, Алимов Абдулсаид

def home_view(request):
    articles = Article.objects.all()
    # categories = Category.objects.all()
    context = {
        'articles': articles,
        # 'categories': categories
    }
    return render(request, 'core/index.html', context)


class HomeView(ListView):
    template_name = 'core/index.html'
    context_object_name = 'articles'
    model = Article

class SearchResults(HomeView):
    def get_queryset(self):
        print(self.request.GET)
        query = self.request.GET.get('q')
        return Article.objects.filter(
            Q(title__iregex=query) | Q(short_description__iregex=query)
        )


def get_articles_by_category(request, category_id):
    articles = Article.objects.filter(category__id=category_id)
    context = {

        'articles': articles
    }
    return render(request, 'core/index.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    try:
        article.likes
    except Exception as e:
        Like.objects.create(article=article)

    try:
        article.dislikes
    except Exception as e:
        Dislike.objects.create(article=article)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.article = article
            form.save()
            try:
                form.likes
            except Exception as e:
                Like.objects.create(comment=form)

            try:
                form.dislikes
            except Exception as e:
                Dislike.objects.create(comment=form)
            return redirect('article_detail', article.pk)
    else:
        form = CommentForm()

    # comments = Comment.objects.filter(article=article)
    # comments = article.comment_set.all()
    comments = article.comments.all()
    total_comments_likes = {comment.pk:comment.likes.user.all().count() for comment in comments}
    total_comments_dislikes = {comment.pk:comment.dislikes.user.all().count() for comment in comments}
    total_likes = article.likes.user.all().count()
    total_dislikes = article.dislikes.user.all().count()
    context = {
        'article': article,
        'form': form,
        'comments': comments,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_comments_likes': total_comments_likes,
        'total_comments_dislikes': total_comments_dislikes
    }
    return render(request, 'core/detail.html', context)


def about_view(request):
    return render(request, 'core/about.html')


def contacts_view(request):
    return render(request, 'core/contacts.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'core/login.html', context)


def registration_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'core/registration.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def create_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False) # Article, pk
            form.author = request.user
            form.save()
            return redirect('article_detail', form.pk)
    else:
        form = ArticleForm()

    context = {
        'form': form
    }
    return render(request, 'core/article_form.html', context)


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'core/article_form.html'
    form_class = ArticleForm
    # lookup_field = 'article_id'


class ArticleDeleteView(DeleteView):
    model = Article  # Article -> article
    template_name = 'core/article_confirm_delete.html'
    success_url = '/'  # для перенаправления после удаления объекта


# obj_type = article/comment
def add_vote(request, obj_type, obj_id, action):
    from django.shortcuts import get_object_or_404

    obj = None
    if obj_type == 'article':
        obj = get_object_or_404(Article, pk=obj_id)
    elif obj_type == 'comment':
        obj = get_object_or_404(Comment, pk=obj_id)

    try:
        obj.likes
    except Exception as e:
        if obj.__class__ is Article:
            Like.objects.create(article=obj)
        else:
            Like.objects.create(comment=obj)

    try:
        obj.dislikes
    except Exception as e:
        if obj.__class__ is Article:
            Dislike.objects.create(article=obj)
        else:
            Dislike.objects.create(comment=obj)

    if action == 'add_like':
        if request.user in obj.likes.user.all():
            obj.likes.user.remove(request.user.pk)
        else:
            obj.likes.user.add(request.user.pk)
            obj.dislikes.user.remove(request.user.pk)
    elif action == 'add_dislike':
        if request.user in obj.dislikes.user.all():
            obj.dislikes.user.remove(request.user.pk)
        else:
            obj.dislikes.user.add(request.user.pk)
            obj.likes.user.remove(request.user.pk)
    # http://127.0.0.1:8000/articles/1
    return redirect(request.environ['HTTP_REFERER'])


def author_articles(request, username):
    user = User.objects.get(username=username)
    articles = Article.objects.filter(author = user)
    total_comments = sum([article.comments.all().count() for article in articles])
    total_likes = sum([article.likes.user.all().count() for article in articles])
    total_dislikes = sum([article.dislikes.user.all().count() for article in articles])
    context = {
        'article': articles,
        'total_articles': articles.count,
        'total_comments': total_comments,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
    }
    return render(request, 'core/author.html', context)
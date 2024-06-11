from django import template
from core.models import Category


# создаем регистратор тегов
register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def is_category_current(request, category_id):
    return str(category_id) in request.path


@register.simple_tag()
def is_vote_exists(request, article, vote_type):
    user = request.user
    if vote_type == 'like':
        voted_users = article.likes.user.all()
    elif vote_type == 'dislike':
        voted_users = article.dislikes.user.all()
    else:
        voted_users = []
    return user in voted_users



@register.simple_tag()
def is_vote_exists_2(request, comment, vote_type):
    user = request.user
    if vote_type == 'like':
        voted_users = comment.likes.user.all()
    elif vote_type == 'dislike':
        voted_users = comment.dislikes.user.all()
    else:
        voted_users = []
    return user in voted_users




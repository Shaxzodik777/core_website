from django.urls import path

from . import views


# categories/<id>
urlpatterns = [
    # path('', views.home_view, name='home'),
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about_view, name='about'),
    path('contacts/', views.contacts_view, name='contacts'),

    path('categories/<int:category_id>', views.get_articles_by_category, name='category_articles'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),

    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.user_logout, name='logout'),

    path('article/create/', views.create_article_view, name='create'),
    path('article/<int:pk>/update/', views.ArticleUpdateView.as_view(), name='update'),
    path('article/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='delete'),

    path('<str:obj_type>/<int:obj_id>/<str:action>/', views.add_vote, name='add_vote'),
    path('author/<str:username>', views.author_articles, name='author_articles'),
    path('search/', views.SearchResults.as_view(), name='search')
]

# 1.  Разработать простое веб-приложение на фреймворке
# Django, которое позволит пользователям регистрироваться, авторизовываться
# и вести список личных задач (to-do list). Приложение должно предоставлять
# возможности для создания, просмотра, редактирования и удаления задач.
# Также необходима функциональность поиска среди своих задач.
# Технические требования
# 1.  Бэкенд
# •  Язык программирования: Python 3.8+
# •  Веб-фреймворк: Django 3.2+
# •  База данных: SQLite в разработке
# •  Аутентификация и авторизация: использовать стандартные механизмы Django
# 2.  Фронтенд
# •  HTML, CSS (Bootstrap или любой другой CSS фреймворк)
# 3.  Функциональные требования
# •  Регистрация/авторизация пользователей
# •  Создание, просмотр, редактирование и удаление задач
# •  Возможность отмечать задачи выполненными
# •  Поиск по задачам
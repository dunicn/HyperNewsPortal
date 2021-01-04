from django.urls import path
from . import views
from .views import CreateNewsView

urlpatterns = [
    path('', views.home_page, name="home-page"),
    path('news/<int:post_id>/', views.news_page, name="news-page"),
    path('news/', views.main_page, name="list-page"),
    # path('news/create', views.create_news, name="create-page"),
    path('news/create/', CreateNewsView.as_view(), name="create-page"),
]

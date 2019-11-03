from django.urls import path
from . import views

app_name = 'posts-api'

urlpatterns = [
    path('',views.PostListAPIView.as_view(),name='list'),
    path('create/',views.PostCreateAPIView.as_view(),name='create'),
    path('<id>/',views.PostDetailAPIView.as_view(),name='detail'),
    path('<id>/edit/',views.PostUpdateAPIView.as_view(),name='edit'),
    path('<id>/delete/',views.PostDeleteAPIView.as_view(),name='delete'),


]

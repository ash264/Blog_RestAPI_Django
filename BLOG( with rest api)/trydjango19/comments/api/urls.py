from django.urls import path
from .views import (
			CommentListAPIView,
			CommentDetailAPIView,
			CommentCreateAPIView,
			# CommentEditAPIView,
		)

app_name = 'comments-api'

urlpatterns = [
    path('',CommentListAPIView.as_view(),name='list'),
    path('create/',CommentCreateAPIView.as_view(),name='create'),
    path('<id>/',CommentDetailAPIView.as_view(),name='thread'),
    # path('<id>/edit/',CommentEditAPIView.as_view(),name='edit'),
    # path('<id>/delete/',comment_delete,name='comment_delete'),


]

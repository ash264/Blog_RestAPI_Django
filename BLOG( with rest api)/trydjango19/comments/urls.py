from django.urls import path
from .views import (
		comment_thread,
		comment_delete,
	)

app_name = 'comments'

urlpatterns = [
    path('<id>/',comment_thread,name='thread'),
    path('<id>/delete/',comment_delete,name='comment_delete'),


]

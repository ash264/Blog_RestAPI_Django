from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.http import HttpResponse,  HttpResponseRedirect
from .models import Post
# Create your views here.
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator
from urllib.parse import quote
from django.utils import timezone
from django.db.models import Q

from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from comments.forms import CommentForm


def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance= form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, 'Created successfully.')
		return redirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request,'post_form.html',context)


def post_detail(request,id):
	today = timezone.now().date()
	instance = get_object_or_404(Post, slug=id)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote(instance.content)
	initial_data = {
		"content_type": instance.get_content_type,
		"object_id": instance.id,
	}
	form = CommentForm(request.POST or None,initial= initial_data) 

	if form.is_valid(): #and request.user.is_authenticated():
		c_type = form.cleaned_data["content_type"]
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data["object_id"]
		content_data = form.cleaned_data["content"]
		parent_obj = None
		
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		new_comment,created = Comment.objects.get_or_create(
								user = request.user,
								content_type = content_type,
								object_id = obj_id,
								content = content_data,
								parent = parent_obj,
							)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context ={
		"title": instance.title,
		"instance":instance,
		"share_string":share_string,
		"today": today,
		"comments":comments,
		"comment_form":form,

	}
	return render(request,'post_detail.html',context)

def post_list(request):
	queryset = Post.objects.active()
	if request.user.is_staff or request.user.is_superuser:
		queryset = Post.objects.all()

	query = request.GET.get('q')
	if query:
		queryset = queryset.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query) 
			).distinct()

	paginator = Paginator(queryset, 2) # Show 2 contacts per page
	page = request.GET.get('page')
	queryset = paginator.get_page(page)

	context ={
		"title": "List",
		"object_list": queryset,
	}
	return render(request,'post_list.html',context)
	

# def listing(request):
#     contact_list = Contacts.objects.all()
#     paginator = Paginator(contact_list, 25) # Show 25 contacts per page

#     page = request.GET.get('page')
#     contacts = paginator.get_page(page)
#     return render(request, 'list.html', {'contacts': contacts})

def post_update(request,id):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=id)

	form = PostForm(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
		instance= form.save(commit=False)
		instance.save()
		messages.success(request, 'Edited successfully.',extra_tags='html_safe')
		return redirect(instance.get_absolute_url())

	context ={
		"title": instance.title,
		"instance":instance,
		"form":form,
	}
	return render(request,'post_form.html',context)

def post_delete(request,id):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=id)
	instance.delete()
	messages.success(request, 'Deleted successfully.')
	return redirect('posts:list')


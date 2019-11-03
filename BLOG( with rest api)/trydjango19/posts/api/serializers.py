from rest_framework.serializers import (
	ModelSerializer, 
	HyperlinkedIdentityField,
	SerializerMethodField,
	)

from posts.models import Post

from comments.api.serializers import CommentSerializer
from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer


post_detail_url = HyperlinkedIdentityField(
			view_name='posts-api:detail',
			lookup_field='id',
		)

class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			# 'id',
			'title',
			# 'slug',
			'content',
			'publish',
			# 'image',
		]


class PostDetailSerializer(ModelSerializer):
	user = UserDetailSerializer(read_only=True)
	url = post_detail_url
	# user = SerializerMethodField()
	image = SerializerMethodField()
	html = SerializerMethodField()
	comments = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			'url',
			'id',
			'user',
			'title',
			'slug',
			'content',
			'publish',
			# 'user',
			'image',
			'html',
			'comments',
		]

	# def get_user(self,obj):
	# 	return str(obj.user.username)

	def get_html(self, obj):
		return obj.get_markdown()

	def get_image(self,obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image

	def get_comments(self,obj):
		content_type = obj.get_content_type
		object_id = obj.id
		c_qs = Comment.objects.filter_by_instance(obj)
		comments = CommentSerializer(c_qs, many=True).data
		return comments


class PostListSerializer(ModelSerializer):
	user = UserDetailSerializer(read_only=True)
	url = post_detail_url
	# delete_url = HyperlinkedIdentityField(
	# 		view_name='posts-api:delete',
	# 		lookup_field='id',

	# 	)
	# user = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			'url',
			# 'id',
			'user',
			'title',
			# 'slug',
			'content',
			'publish',
			# 'image',
			# 'delete_url',
		]
	# def get_user(self,obj):
	# 	return str(obj.user.username)



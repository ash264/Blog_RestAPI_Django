from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView, DestroyAPIView

from posts.models import Post
from .serializers import PostListSerializer, PostCreateUpdateSerializer, PostDetailSerializer

from rest_framework.permissions import (
		AllowAny,
		IsAuthenticated,
		IsAdminUser,
		IsAuthenticatedOrReadOnly,

	)

from .permissions import IsOwnerOrReadOnly
from django.db.models import Q

from rest_framework.filters import (
		SearchFilter,
		OrderingFilter,

	)

from rest_framework.pagination import (
		LimitOffsetPagination,
		PageNumberPagination,

	)
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination


class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer

	# permission_classes = [IsAuthenticated, IsAdminUser]	# checks if user is authenticated + other user checks

	def perform_create(self, serializer):
		serializer.save(user= self.request.user)



class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'id'
	permission_classes = [AllowAny]


class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = 'id'
	permission_classes = [IsOwnerOrReadOnly]

	def perform_update(self, serializer):
		serializer.save(user= self.request.user)
		# email send_email


class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'id'
	permission_classes = [IsOwnerOrReadOnly]



class PostListAPIView(ListAPIView):
	serializer_class = PostListSerializer
	filter_backends = [SearchFilter,OrderingFilter]
	search_fields = ['title','content','user__first_name']
	# pagination_class = LimitOffsetPagination
	# pagination_class = PageNumberPagination
	pagination_class = PostPageNumberPagination
	permission_classes = [AllowAny]

	def get_queryset(self, *args,**kwargs):
		queryset_list = Post.objects.all()
		query = self.request.GET.get('q')
		if query:
			queryset_list = queryset_list.filter(
				Q(title__icontains=query) |
				Q(content__icontains=query) |
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query) 
				).distinct()

		return queryset_list








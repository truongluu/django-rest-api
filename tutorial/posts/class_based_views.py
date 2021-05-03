from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import mixins
from shared.permissions import IsOwnerOrReadOnly


class PostList(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'description']

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        queryset = Post.objects.all()
        if not self.request.user.is_anonymous:
            user_id = self.request.user.id
            queryset = Post.objects.filter(owner=user_id)
        return queryset

    """
    List all posts, or create a new snippet.
    """

    def get(self, request, format=None):
        posts = self.get_queryset()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    """
    Retrieve, update or delete a post instance.
    """

    # def check_object_permissions(self, request, obj):
    #     return super().check_object_permissions(request, obj)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

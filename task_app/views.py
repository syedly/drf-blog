from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import*
from rest_framework.permissions import IsAuthenticated

class SignupView(generics.CreateAPIView):
    query_set = User.objects.all()
    serializer_class = SignupSerializer
    
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            "message": "login successfully!"
        })
        
class ShowAllNotes(generics.ListAPIView):
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all()

class Notes(generics.ListCreateAPIView):
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset:
            return Response({
                'data': {},
                'message': "No notes found for this user."
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
class NotesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        object = get_object_or_404(Note, pk=self.kwargs.get('pk'))
        if object.user != self.request.user:
            raise PermissionError("you have no access of these notes!")
        return object 
    

class BlogCreateVIew(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class ShowAllBlogs(generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    queryset = Blog.objects.all()
    
class DetailBlogView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    
    def get_object(self):
        object = get_object_or_404(Blog, pk=self.kwargs.get('pk'))
        if object.user != self.request.user:
            raise PermissionError("you have no access of these Blogs!")
        return object
    
class SpecificBlog(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]  
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    
    def get_object(self):
        blog = get_object_or_404(Blog, pk=self.kwargs.get('pk'))
        return blog
    
class CommentView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        blog_id = self.kwargs.get('pk')
        return Comment.objects.filter(blog__id=blog_id)

    def perform_create(self, serializer):
        blog_id = self.kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=blog_id)
        serializer.save(user=self.request.user, blog=blog)

class SearchBlog(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    
    def get_queryset(self):
        blog_title = self.kwargs.get('title')
        if blog_title:
            search = Blog.objects.filter(title__icontains=blog_title)
            return search
        else:
            return Blog.objects.all()

class LikeBlogView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    
    def update(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        
        if request.user in blog.liked_by.all():
            blog.liked_by.remove(request.user)
        else:
            blog.liked_by.add(request.user)
            liked = False
            
        serializer = self.get_serializer(blog)
        return Response({
            'liked': liked,
            'blog': serializer.data
        }, status=status.HTTP_200_OK)
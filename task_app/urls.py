from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('notes/', Notes.as_view()),
    path('all-notes/', ShowAllNotes.as_view()),
    path('notes/<int:pk>/', NotesDetail.as_view()),
    path('blog/', BlogCreateVIew.as_view()),
    path('all-blogs/', ShowAllBlogs.as_view()),
    path('blogs/<int:pk>/',DetailBlogView.as_view()),
    path('specific-blog/<int:pk>/',SpecificBlog.as_view()),
    path('blog-comment/<int:pk>/', CommentView.as_view()),
    path('search/<str:title>/', SearchBlog.as_view()),
    path('search/', SearchBlog.as_view()),
    path('blog-like/<int:pk>/', LikeBlogView.as_view(), name='like_blog'),
]

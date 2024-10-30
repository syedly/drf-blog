from django.urls import path, include

urlpatterns = [
    path('task_app/', include('task_app.urls'))
]

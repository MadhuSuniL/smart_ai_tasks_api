from django.urls import path, include


urlpatterns = [
    path('api/auth/', include('auth_app.urls')),
    path('api/ai_tasks/', include('ai_tasks_app.urls')),
]
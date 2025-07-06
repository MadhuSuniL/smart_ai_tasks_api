from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ContextViewSet, CategoryViewSet, AISuggestedTasks, AISuggestedTasksSave, TaskExportCSVView, TaskImportView, TaskICSExportView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'contexts', ContextViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ai_suggested_tasks/', AISuggestedTasks.as_view()),
    path('save_ai_suggested_tasks/', AISuggestedTasksSave.as_view()),
    path('tasks/export/csv/', TaskExportCSVView.as_view(), name='task-export-csv'),
    path('tasks/import/csv/', TaskImportView.as_view(), name='task-import-csv'),
    path('tasks_ics/export/csv/<pk>', TaskICSExportView.as_view(), name='task_ics-export-csv'),   
]

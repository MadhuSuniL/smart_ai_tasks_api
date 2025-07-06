import io
import csv
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, views
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Task, Context, Category
from .serializers import TaskSerializer, ContextSerializer, CategorySerializer
from helper.ai.process import AutoTaskGenerator
from helper.utils import generate_ics_from_task
from .filters import TaskFilter


class ModelViewSetWithCurrentUserQuerySet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        current_user = self.request.user
        return super().get_queryset().filter(user = current_user)
    

class TaskViewSet(ModelViewSetWithCurrentUserQuerySet):
    queryset = Task.objects.all().order_by('-priority_score')
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

class ContextViewSet(ModelViewSetWithCurrentUserQuerySet):
    queryset = Context.objects.all().order_by('-created_at')
    serializer_class = ContextSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class APIViewSetWithCurrentUserQuerySet(views.APIView):
    
    def get_queryset(self):
        current_user = self.request.user
        return self.queryset.filter(user = current_user)
    

class AISuggestedTasks(APIViewSetWithCurrentUserQuerySet):
    queryset = Context.objects.all().order_by('-created_at')
        
    def get(self, request : Request):
        contexts = self.get_queryset().filter(is_task_generated = False)
        if len(contexts) == 0:
            return Response({"detail" : "No new contexts found!"})
        print(contexts)
        auto_task_generator : AutoTaskGenerator = AutoTaskGenerator(contexts=contexts)
        tasks = auto_task_generator.generate_tasks()
        return Response(tasks)


class AISuggestedTasksSave(APIViewSetWithCurrentUserQuerySet):
    queryset = Context.objects.all().order_by('-created_at')
    
    def post(self, request : Request):
        tasks = request.data.get('tasks')
        serializer = TaskSerializer(data=tasks, many=True, context = {'request' : request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        contexts = self.get_queryset().filter(is_task_generated = False)
        contexts.update(is_task_generated=True)
        return Response(serializer.data, status=201)
    

class TaskExportCSVView(APIViewSetWithCurrentUserQuerySet):
    queryset = Task.objects.all().order_by('-created_at')

    def get(self, request):
        tasks : list[Task] = self.get_queryset()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tasks_export.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'title', 'description', 'category', 'tags',
            'priority_score', 'priority', 'deadline', 'status', 'created At'
        ])

        for task in tasks:
            writer.writerow([
                task.title,
                task.description,
                task.category.name if task.category else '',
                "-".join(task.tags),
                task.priority_score,
                task.priority,
                task.deadline.isoformat() if task.deadline else '',
                task.status,
                task.created_at.isoformat()
            ])

        return response
    
    
class TaskImportView(views.APIView):

    def post(self, request):
        file = request.FILES.get('file')
        if not file or not file.name.endswith('.csv'):
            return Response({"detail": "Please upload a valid CSV file."}, status=400)

        decoded_file = file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(decoded_file))

        task_data_list = []
        for row in csv_reader:
            category_name = row.get("category", "").strip()
            category = None
            if category_name:
                category, _ = Category.objects.get_or_create(name=category_name)

            task_data = {
                "title": row["title"],
                "description": row["description"],
                "category_id": category.id if category else None,
                "tags": [tag.strip() for tag in row.get("tags", "").split(",") if tag.strip()],
                "priority_score": float(row["priority_score"]),
                "priority": row["priority"],
                "deadline": row.get("deadline") or None,
                "status": row.get("status", "pending"),
                "user": request.user.id  
            }
            task_data_list.append(task_data)

        serializer = TaskSerializer(data=task_data_list, many=True, context = {'request' : request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
    
    
class TaskICSExportView(views.APIView):

    def get(self, request, pk):
        task = Task.objects.get(pk=pk, user=request.user)
        ics_content = generate_ics_from_task(task)

        response = HttpResponse(ics_content, content_type='text/calendar')
        response['Content-Disposition'] = f'attachment; filename="{task.title}.ics"'
        return response
from django.db import models
from helper.models import TimeLine, UUIDPrimaryKey
from auth_app.models import User


class Category(TimeLine, UUIDPrimaryKey):
    name = models.CharField(max_length=100, unique=True)
    usage_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Context(TimeLine, UUIDPrimaryKey):
    SOURCE_CHOICES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('note', 'Note'),
        ('other', 'Other'),
    ]

    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    content = models.TextField()
    processed_insights = models.TextField(blank=True, null=True)  # For AI summaries
    is_task_generated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contexts')

    def __str__(self):
        return f"{self.source_type.title()} - {self.created_at.strftime('%Y-%m-%d %I:%M')}"


class Task(TimeLine, UUIDPrimaryKey):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    tags = models.JSONField(default=list)
    priority_score = models.FloatField(default=0.0)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    
    def __str__(self):
        return f"{self.title} ({self.priority})"

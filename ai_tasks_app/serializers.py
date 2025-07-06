from rest_framework import serializers
from .models import Task, Context, Category
from helper.ai.process import ProcessContext

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ContextSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    def create(self, validated_data):
        context = Context(**validated_data)
        process_context = ProcessContext(context)
        return process_context.pre_process_context()

    class Meta:
        model = Context
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )

    class Meta:
        model = Task
        fields = "__all__"

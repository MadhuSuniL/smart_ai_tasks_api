from .llm import llm
from .prompts import CONTEXT_PROCESS_SYSTEM_PROMPT, TASK_GENERATION_SYSTEM_PROMPT
from .schemas import TasksSchema
from django.utils import timezone
from ai_tasks_app.models import Context, Category
from helper.consonants import CONTEXT_PROCESS_CHAR_LIMIT
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


class ProcessContext:
    def __init__(self, context : Context):
        self.context : Context = context
        self.llm = llm
        self.current_time = timezone.now().isoformat() + "Z"
    
    def pre_process_context(self) -> Context:
        content = self.context.content
        # Limit the content to ignore context length issues..
        limited_content = content[:CONTEXT_PROCESS_CHAR_LIMIT]
        input = [
                SystemMessage(CONTEXT_PROCESS_SYSTEM_PROMPT.format(current_time = self.current_time)),
                HumanMessage(limited_content)
            ]
        response : AIMessage = self.llm.invoke(input)
        self.context.processed_insights = response.content
        self.context.save()
        return self.context
    

class AutoTaskGenerator:
    
    def __init__(self, contexts : list[Context]):
        self.contexts : list[Context] = contexts
        self.llm = llm.with_structured_output(TasksSchema, method='json_mode')
        self.current_time = timezone.now().isoformat() + "Z"
    
    def generate_tasks(self):
        chunks = [context.processed_insights for context in self.contexts]
        chunks_string = "\n\n".join(chunks)
        input = [
                SystemMessage(TASK_GENERATION_SYSTEM_PROMPT.format(current_time = self.current_time)),
                HumanMessage(chunks_string)
            ]
        
        tasks_schema: list[TasksSchema] = self.llm.invoke(input)
        task_dicts = [task for task in tasks_schema.model_dump()['tasks']]
        
        # Handle the category if already exisist..
        for task in task_dicts:
            category_name = task.pop("category", None)
            if category_name:
                category, _ = Category.objects.get_or_create(name=category_name)
                task["category_id"] = category.id
                task["category"] = category.name
        return task_dicts
        
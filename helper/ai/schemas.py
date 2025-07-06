from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime


class TaskSchema(BaseModel):
    title: str = Field(..., description="Short task title summarizing the intent")
    description: str = Field(..., description="Expanded explanation of the task")
    category: str = Field(..., description="General category name, e.g., 'Work', 'Personal', 'Finance'")
    tags: List[str] = Field(..., min_items=1, max_items=3, description="1 to 3 short relevant keywords")
    priority_score: float = Field(..., ge=0.0, le=1.0, description="Score indicating urgency/stress level")
    priority: Literal["low", "medium", "high"] = Field(..., description="Task priority level")
    deadline: datetime = Field(..., description="Deadline in ISO 8601 format")
    status: Literal["pending"] = Field("pending", description="Always set to 'pending' initially")


class TasksSchema(BaseModel):
    tasks : List[TaskSchema] = Field(..., description="List of tasks (1 or more tasks)")
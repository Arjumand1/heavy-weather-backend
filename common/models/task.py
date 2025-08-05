from dataclasses import dataclass
from rococo.models import VersionedModel
from typing import ClassVar, Optional
from datetime import datetime


@dataclass
class Task(VersionedModel):
    use_type_checking: ClassVar[bool] = True
    table_name: ClassVar[str] = "task"
    
    # Define database fields (person_id and title are NOT NULL in DB)
    person_id: str = ""
    title: str = ""
    description: str = ""
    completed: bool = False
    completed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
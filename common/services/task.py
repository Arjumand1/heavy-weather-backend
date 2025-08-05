from common.repositories.factory import RepositoryFactory, RepoType
from common.models.task import Task


class TaskService:

    def __init__(self, config):
        self.config = config
        self.repository_factory = RepositoryFactory(config)
        self.task_repo = self.repository_factory.get_repository(RepoType.TASK)

    def save_task(self, task: Task):
        task = self.task_repo.save(task)
        return task

    def get_tasks_by_person_id(self, person_id: str, completed=None):
        filters = {"person_id": person_id}
        if completed is not None:
            filters["completed"] = completed
        tasks = self.task_repo.get_many(filters)
        return tasks

    def get_task_by_id(self, entity_id: str):
        task = self.task_repo.get_one({"entity_id": entity_id})
        return task

    def update_task(self, task: Task):
        task = self.task_repo.save(task)
        return task

    def delete_task(self, entity_id: str):
        task = self.task_repo.get_one({"entity_id": entity_id})
        if task:
            self.task_repo.delete(task)
        return task

from flask_restx import Namespace, Resource
from flask import request, g, current_app
from app.helpers.response import get_success_response, get_failure_response, parse_request_body, validate_required_fields
from app.helpers.decorators import login_required
from common.app_config import config
from common.services import TaskService
from common.models import Task
from datetime import datetime

# Create the task blueprint
task_api = Namespace('tasks', description="Task related APIs")


@task_api.route('')
class TaskList(Resource):
    @login_required()
    def get(self):
        """Get all tasks for the authenticated user"""
        completed = request.args.get('completed')
        if completed is not None:
            completed = completed.lower() == 'true'
        
        task_service = TaskService(config)
        tasks = task_service.get_tasks_by_person_id(g.current_user_id, completed)
        return get_success_response(tasks=[task.as_dict() for task in tasks])

    @login_required()
    @task_api.expect(
        {'type': 'object', 'properties': {
            'title': {'type': 'string', 'required': True},
            'description': {'type': 'string', 'required': False}
        }}
    )
    def post(self):
        """Create a new task"""
        parsed_body = parse_request_body(request, ['title', 'description'])
        validate_required_fields({'title': parsed_body['title']})  # Only title is required

        task = Task()
        print(f"Creating task with person_id: {g.current_user_id}")
        print(f"Parsed request body: {parsed_body}")
        task.person_id = g.current_user_id
        task.title = parsed_body['title']
        task.description = parsed_body.get('description', '')
        task.completed = False
        print(f"Task before save - person_id: {task.person_id}, title: {task.title}, description: {task.description}")

        task_service = TaskService(config)
        saved_task = task_service.save_task(task)
        
        return get_success_response(task=saved_task.as_dict(), message="Task created successfully")


@task_api.route('/<string:task_id>')
class TaskDetail(Resource):
    @login_required()
    def get(self, task_id):
        """Get a specific task"""
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id)
        
        if not task or task.person_id != g.current_user_id:
            return get_failure_response(message="Task not found", status_code=404)
        
        return get_success_response(task=task.as_dict())

    @login_required()
    @task_api.expect(
        {'type': 'object', 'properties': {
            'title': {'type': 'string', 'required': False},
            'description': {'type': 'string', 'required': False},
            'completed': {'type': 'boolean', 'required': False}
        }}
    )
    def put(self, task_id):
        """Update a task"""
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id)
        
        if not task or task.person_id != g.current_user_id:
            return get_failure_response(message="Task not found", status_code=404)

        # Parse the raw JSON directly to handle nullable values and partial updates
        try:
            raw_body = request.get_json(force=True)
            current_app.logger.info(f"DEBUG: Raw request body: {raw_body}")
        except Exception as e:
            current_app.logger.error(f"DEBUG: Error parsing JSON: {e}")
            raw_body = {}
            
        current_app.logger.info(f"DEBUG: Before update - completed: {task.completed}, completed_at: {task.completed_at}")
        
        # Handle title updates - title can be empty/null
        if 'title' in raw_body:
            task.title = raw_body['title'] if raw_body['title'] is not None else ""
        # Handle description updates - can be null
        if 'description' in raw_body:
            task.description = raw_body['description'] if raw_body['description'] is not None else ""
            
        # Handle completed status updates
        if 'completed' in raw_body:
            current_app.logger.info(f"DEBUG: Setting completed to: {raw_body['completed']} (type: {type(raw_body['completed'])})")
            task.completed = raw_body['completed']
            current_app.logger.info(f"DEBUG: Task completed after assignment: {task.completed}")
            if task.completed and not task.completed_at:
                task.completed_at = datetime.utcnow()
                current_app.logger.info(f"DEBUG: Set completed_at to: {task.completed_at}")
            elif not task.completed:
                task.completed_at = None
                current_app.logger.info("DEBUG: Set completed_at to None")

        current_app.logger.info(f"DEBUG: Before save - completed: {task.completed}, completed_at: {task.completed_at}")
        updated_task = task_service.update_task(task)
        current_app.logger.info(f"DEBUG: After save - completed: {updated_task.completed}, completed_at: {updated_task.completed_at}")
        
        return get_success_response(task=updated_task.as_dict(), message="Task updated successfully")

    @login_required()
    def delete(self, task_id):
        """Delete a task"""
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id)
        
        if not task or task.person_id != g.current_user_id:
            return get_failure_response(message="Task not found", status_code=404)

        task_service.delete_task(task_id)
        
        return get_success_response(message="Task deleted successfully")
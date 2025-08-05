from flask_restx import Namespace, Resource
from flask import request, current_app
from app.helpers.response import get_success_response, parse_request_body
from app.helpers.decorators import login_required
from common.app_config import config
from common.services import PersonService

# Create the organization blueprint
person_api = Namespace('person', description="Person-related APIs")


@person_api.route('/me')
class Me(Resource):
    
    @login_required()
    def get(self, person):
        return get_success_response(person=person.as_dict())

    @person_api.expect(
        {'type': 'object', 'properties': {
            'first_name': {'type': 'string'},
            'last_name': {'type': 'string'}
        }}
    )
    @login_required()
    def put(self, person):
        """Update user profile"""
        # Parse the raw JSON directly to handle nullable values and partial updates
        try:
            raw_body = request.get_json(force=True)
            current_app.logger.info(f"DEBUG: Raw request body: {raw_body}")
        except Exception as e:
            current_app.logger.error(f"DEBUG: Error parsing JSON: {e}")
            raw_body = {}
        
        person_service = PersonService(config)
        current_app.logger.info(f"DEBUG: Before update: {person.first_name}, {person.last_name}")
        
        # Handle first_name updates - can be empty/null
        if 'first_name' in raw_body:
            person.first_name = raw_body['first_name'] if raw_body['first_name'] is not None else ""
            
        # Handle last_name updates - can be empty/null
        if 'last_name' in raw_body:
            person.last_name = raw_body['last_name'] if raw_body['last_name'] is not None else ""

        current_app.logger.info(f"DEBUG: After field update: {person.first_name}, {person.last_name}")
        
        updated_person = person_service.save_person(person)
        
        current_app.logger.info(f"DEBUG: After save: {updated_person.first_name}, {updated_person.last_name}")
        
        return get_success_response(person=updated_person.as_dict(), message="Profile updated successfully")

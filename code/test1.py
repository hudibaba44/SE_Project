from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from pathlib import Path 
import os

app = Flask(__name__)
api = Api(app)

START_PORT_FOR_EDITOR = 5500

def find_code_editor_user_id_project_id(user_id, project_id):
    return False

def get_free_port():
    return 5500

def create_code_editor(user_id, project_id, file_path):
    path_to_folder = Path(file_path)
    assert path_to_folder.exists() == 1
    port_no = get_free_port()    
    return (1,2)

class code_editor(Resource):
    # Parameters
    # user_id: String
    # project_id: String    
    # file_path: String
    # 
    # Response
    # server_ip: String 
    # port_no: String
    def put(self):
        request_data = request.get_json()
        print(type(request_data))
        assert 'user_id' in request_data
        assert 'project_id' in request_data
        assert 'file_path' in request_data
        user_id = request_data['user_id']
        project_id = request_data['project_id']
        file_path = request_data['file_path']
        result_of_find = find_code_editor_user_id_project_id(user_id, project_id)
        if(result_of_find == False):
            server_ip, port_no = create_code_editor(user_id, project_id, file_path)

        print(request_data['user_id'])
        print(request_data['project_id'])
        print(request_data['file_path'])
        print(request_data)
        return {'hello': 'world1'}

api.add_resource(code_editor, '/')

if __name__ == '__main__':
    app.run(debug=True)
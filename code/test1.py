from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from pathlib import Path 
import os
import docker 
import json 
# import .database_code_editor
from database_code_editor import code_editor_db_service
app = Flask(__name__)
api = Api(app)
docker_client = docker.from_env()

CODE_EDITOR_IMAGE_NAME = "codercom/code-server:v2"
PORT_OF_CONTAINER = '8080/tcp'
PATH_TO_BIND_HOST_FOLDER_TO_CONTAINER = "/home/project"
START_PORT_FOR_EDITOR = 5500
HOST_IP = "0.0.0.0"
code_editor_db = code_editor_db_service()

def make_dictionary_server_ip_port_no(server_ip, port_no):
    return {
        'server_ip':server_ip,
        'port_no':port_no
    }

def find_code_editor_user_id_project_id(user_id, project_id):
    document =  code_editor_db.get_document_for_user_id_project_id(user_id, project_id)
    if(document is None):
        return None
    else:
        return make_dictionary_server_ip_port_no(
            document['ip_address'], document['port_no'])
        # return (document['ip_address'], document['port_no'])

def get_free_port():
    return 5500

def create_code_editor(user_id, project_id, file_path):
    path_to_folder = Path(file_path)
    assert path_to_folder.exists() == 1
    port_no = get_free_port()    
    container_object = docker_client.containers.run(CODE_EDITOR_IMAGE_NAME, ports={PORT_OF_CONTAINER: f'{port_no}'}, volumes = {path_to_folder: {'bind' : PATH_TO_BIND_HOST_FOLDER_TO_CONTAINER, 'mode': 'rw'}}, detach = True)
    code_editor_db.insert_user_id_project_id_ip_address_port_no_container_id(user_id, project_id, HOST_IP, port_no, container_object.id)
    return (1,2)

def delete_code_editor(user_id, project_id):
    container_id = code_editor_db.get_container_id(user_id, project_id)
    print("Container id is ", container_id)
    if (container_id is None):
        return False
    container = docker_client.containers.get(container_id)
    container.stop()
    container.remove()
    code_editor_db.delete_user_id_project_id(user_id, project_id)
    return True

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
        assert 'user_id' in request_data
        assert 'project_id' in request_data
        assert 'file_path' in request_data
        user_id = request_data['user_id']
        project_id = request_data['project_id']
        file_path = request_data['file_path']
        result_of_find = find_code_editor_user_id_project_id(user_id, project_id)
        if(result_of_find is None):
            server_ip, port_no = create_code_editor(user_id, project_id, file_path)
            return make_response(
                json.dumps(
                    make_dictionary_server_ip_port_no(server_ip, port_no)
                    ),
                200
            )
        else:
            return make_response(
                json.dumps(
                    result_of_find
                ),
                200
            )

        # print(request_data['user_id'])
        # print(request_data['project_id'])
        # print(request_data['file_path'])
        # print(request_data)
        return {'hello': 'world1'}

    def delete(self):
        request_data = request.get_json()
        assert 'user_id' in request_data
        assert 'project_id' in request_data
        user_id = request_data['user_id']
        project_id = request_data['project_id']
        # file_path = request_data['file_path']
        if (delete_code_editor(user_id, project_id) is False):
            return make_response("No container exists", 404)
        else:
            return make_response("Container deleted succesfully", 200)

api.add_resource(code_editor, '/')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from pathlib import Path
import os
import docker
import json
# import .database_code_editor
from database_code_editor import code_editor_db_service
import time
import shutil
from time import sleep

app = Flask(__name__)
api = Api(app)
docker_client = docker.from_env()

CODE_EDITOR_IMAGE_NAME = "codercom/code-server:v2"
PORT_OF_CONTAINER = '8080/tcp'
PATH_TO_BIND_HOST_FOLDER_TO_CONTAINER = "/home/project"
START_PORT_FOR_EDITOR = 5500
START_PORT_FOR_DEPLOYED_SERVER = 6000
HOST_IP = "0.0.0.0"
PATH_TO_DOCKERFILES = "dockerfiles"
code_editor_db = code_editor_db_service()

current_micro_time = lambda: int(round(time.time() * 1000000))

def get_dockerfile_path(project_id):
    return Path(PATH_TO_DOCKERFILES, "Dockerfile_flask")

def make_dictionary_server_ip_port_no(server_ip, port_no):
    return {
        'server_ip': server_ip,
        'port_no': port_no
    }


def find_code_editor_user_id_project_id(user_id, project_id):
    document = code_editor_db.get_document_for_user_id_project_id(
        user_id, project_id)
    if(document is None):
        return None
    else:
        return make_dictionary_server_ip_port_no(
            document['ip_address'], document['port_no'])

def find_user_deployed_server_user_id_project_id(user_id, project_id):
    return None
    document = code_editor_db.get_document_for_user_id_project_id(
        user_id, project_id)
    if(document is None):
        return None
    else:
        return make_dictionary_server_ip_port_no(
            document['ip_address'], document['port_no'])



def get_free_port(START_PORT):
    ports = code_editor_db.get_all_ports()
    set_of_ports = set()
    # set_of_ports = [set_of_ports.add(i['port_no']) for i in ports]
    # print("Ports are")
    for i in ports:
        # print(i['port_no'])
        set_of_ports.add(i['port_no'])
    print(set_of_ports)
    free_port = START_PORT
    for i in range(1000):
        if(free_port+i not in set_of_ports):
            return free_port+i
    return None
    # return 5500

def build_image(user_id, project_id, folder_path):
    tmp_folder_name = "tmp"+str(current_micro_time())
    tmp_folder_path = Path(tmp_folder_name)
    if(os.path.exists(tmp_folder_path)):
        tmp_folder_name+='1'
        tmp_folder_path = Path(tmp_folder_name)
    # os.mkdir(tmp_folder_path)
    shutil.copytree(folder_path, tmp_folder_path/"app")
    dockerfile_path = get_dockerfile_path(project_id)
    shutil.copy(dockerfile_path, tmp_folder_path/"Dockerfile")
    print(f'{user_id}_{project_id}')
    # Spaces not allowed in tag name
    docker_client.images.build(path = str(tmp_folder_path), 
    tag = f'{user_id}_{project_id}')

    # shutil.copytree()
    sleep(2)
    shutil.rmtree(tmp_folder_path)

    
def create_code_editor(user_id, project_id, folder_path):
    path_to_folder = Path(folder_path)
    assert path_to_folder.exists() == 1
    port_no = get_free_port(START_PORT_FOR_EDITOR)
    if port_no is None:
        return (None, None)
    container_object = docker_client.containers.run(
        CODE_EDITOR_IMAGE_NAME,
        ports={PORT_OF_CONTAINER: f'{port_no}'},
        volumes={
            path_to_folder: {
                'bind': PATH_TO_BIND_HOST_FOLDER_TO_CONTAINER,
                'mode': 'rw'}
        },
        detach=True)
    code_editor_db.insert_user_id_project_id_ip_address_port_no_container_id(
        user_id, project_id, HOST_IP, port_no, container_object.id)
    return (HOST_IP, port_no)

def create_user_deployed_server(user_id, project_id, folder_path):
    path_to_folder = Path(folder_path)
    assert path_to_folder.exists() == 1
    port_no = get_free_port(START_PORT_FOR_DEPLOYED_SERVER)
    if port_no is None:
        return (None, None)

    build_image(user_id, project_id, folder_path)

    container_object = docker_client.containers.run(
        f'{user_id}_{project_id}',
        ports={'5000/tcp': f'{port_no}'},
        detach=True)
    # container_object = docker_client.containers.run(
    #     CODE_EDITOR_IMAGE_NAME,
    #     ports={PORT_OF_CONTAINER: f'{port_no}'},
    #     volumes={
    #         path_to_folder: {
    #             'bind': PATH_TO_BIND_HOST_FOLDER_TO_CONTAINER,
    #             'mode': 'rw'}
    #     },
    #     detach=True)
    # code_editor_db.insert_user_id_project_id_ip_address_port_no_container_id(
    #     user_id, project_id, HOST_IP, port_no, container_object.id)
    # return ("test", "test")
    return (HOST_IP, port_no)


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


def assert_and_return_user_id_project_id_folder_path(request_data):
    assert 'user_id' in request_data
    assert 'project_id' in request_data
    assert 'folder_path' in request_data
    return (request_data['user_id'],
            request_data['project_id'],
            request_data['folder_path'])


class code_editor(Resource):
    # Parameters
    # user_id: String
    # project_id: String
    # folder_path: String
    #
    # Response
    # server_ip: String
    # port_no: String
    def put(self):
        request_data = request.get_json()
        user_id, project_id, folder_path = assert_and_return_user_id_project_id_folder_path(request_data)
        result_of_find = find_code_editor_user_id_project_id(
            user_id, project_id)
        if(result_of_find is None):
            server_ip, port_no = create_code_editor(
                user_id, project_id, folder_path)
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


class user_deployed_server(Resource):
    def put(self):
        request_data = request.get_json()
        user_id, project_id, folder_path = assert_and_return_user_id_project_id_folder_path(request_data)
        result_of_find = find_user_deployed_server_user_id_project_id(
            user_id, project_id)
        if(result_of_find is None):
            server_ip, port_no = create_user_deployed_server(
                user_id, project_id, folder_path)
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


api.add_resource(code_editor, '/')
api.add_resource(user_deployed_server, '/deploy')

if __name__ == '__main__':
    app.run(debug=True)

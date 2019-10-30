from pymongo import MongoClient
mongo_client = MongoClient('localhost', 27017)
database_code_editor = mongo_client.SE 
code_editor_db = database_code_editor.code_editor

document_to_be_found = {
        "user_id": "hello world1",
        "project_id": "neelesh"
    }
document = code_editor_db.find_one(document_to_be_found)
print(document)
print(document['container_id'])
import requests

class git_service:

    def __init__(self):
        self.drone_ip = "http://127.0.0.1:6000/"

    def create_repo(self, email_id, framework_name):
        data = {
         "auto_init": true,
          "description": framework_name,
          "gitignores": "string",
          "issue_labels": "string",
          "license": "string",
          "name": "string",
          "private": true,
          "readme": "string"
        }
        req_api = "/admin/users/{}/repos".format(email_id)
        resp = requests.post(self.drone_ip+req_api, data);
        return resp

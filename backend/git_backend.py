import requests

class git_service:
    def __init__(self):
        self.git_ip = "http://127.0.0.1:3000/"
        self.access_token = "8320d18e7112269504891a0a4a72ce987278a4ef"
        self.params = (
            ('access_token', self.access_token),
        )

    def create_repo(self, email_id, framework_name):
        data = {
            "auto_init": True,
            "description": framework_name,
            "issue_labels": "string",
            "name": framework_name,
            "private": True
        }
        name = email_id.split('@')[0] + "_" + framework_name
        req_api = "api/v1/admin/users/{}/repos".format(name)
        requests.post(self.git_ip+req_api, json = data, params=self.params)

    def create_user(self, email_id, framework_name):
        name = email_id.split('@')[0] + "_" + framework_name
        data = {
            "email": email_id,
            "full_name": name,
            "login_name": name,
            "must_change_password": True,
            "password": "test123",
            "send_notify": True,
            "source_id": 0,
            "username": name
        }
        requests.post(self.git_ip+"api/v1/admin/users", json = data, params=self.params)

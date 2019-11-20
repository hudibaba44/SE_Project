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

data = {
  "email": "user@example.com",
  "full_name": "string",
  "login_name": "string",
  "must_change_password": True,
  "password": "string",
  "send_notify": True,
  "source_id": 0,
  "username": "string"
}

data = {
  "auto_init": True,
  "description": "string",
  "issue_labels": "string",
  "name": "string",
  "private": True
}

params = (
    ('access_token', '95a957a9ca86b0ee4edcdf3e4f21b101e289e30a'),
)

# headers = {"Authorization": "token " + "95a957a9ca86b0ee4edcdf3e4f21b101e289e30a"}
# requests.post("http://192.168.43.109:3000/api/v1/admin/users", json = data, params=params)
requests.post("http://192.168.43.109:3000/api/v1/admin/users/string/repos", json = data, params=params)
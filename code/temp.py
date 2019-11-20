import docker
import time
docker_client = docker.from_env()
a = docker_client.containers.run(
        'neelesh/code122',
        ports={'8080/tcp': f'{5401}'},
        volumes={
            "/home/neelesh/SE/hello@test.com_django": {
                'bind':"/home/project" ,
                'mode': 'rw'}
        },
        # environment = ["PASSWORD=helloworld"],
        detach = True)

print(a)
print(a.logs())
time.sleep(3)
b = docker_client.containers.get(a.id)
print(b.logs())
print(a.logs())

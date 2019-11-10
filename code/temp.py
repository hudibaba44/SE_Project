import shutil

shutil.copytree("dockerfiles/flask", "docker/app")
shutil.copy("dockerfiles/Dockerfile_flask", "docker/Dockerfile")

a = input()

shutil.rmtree("docker/")
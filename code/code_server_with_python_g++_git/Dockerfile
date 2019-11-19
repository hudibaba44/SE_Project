FROM codercom/code-server
RUN sudo apt-get update
RUN sudo apt-get -y install python3
RUN sudo apt-get -y install build-essential
RUN sudo apt-get -y install git
# ENV PASSWORD=se_project
EXPOSE 8080

ENTRYPOINT ["dumb-init", "code-server", "--host", "0.0.0.0"]
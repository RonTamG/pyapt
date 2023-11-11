# This Dockerfile is used for testing the application.
FROM python:3.11.4-bullseye

COPY . /pyapt/
WORKDIR /pyapt/

CMD ["./tests/acceptance_tests/install_git.sh"]

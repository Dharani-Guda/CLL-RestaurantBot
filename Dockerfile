FROM rasa/rasa-sdk:latest

USER root

RUN apt-get update -qq && \
    apt-get install -y sudo && \
    apt-get install -y vim && \
    apt-get install -y python3-dev && \
    apt-get install -y gcc

COPY ./actions /app/actions

USER 1001

FROM rasa/rasa:latest

COPY app /app
COPY server.sh /app/server.sh

USER root
RUN chmod -R 777 /app
USER 1001

RUN rasa train

ENTRYPOINT ["/app/server.sh"]
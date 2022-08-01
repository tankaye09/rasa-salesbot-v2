FROM rasa/rasa:3.2.4

COPY app /app
# COPY server.sh /app/server.sh

USER root
RUN chmod -R 777 /app
USER 1001
WORKDIR /app

VOLUME /app/models

CMD ["run","-m","/app/models","--endpoints", "/app/app/endpoints.yml","--enable-api","--cors","*","--log-file", "out.log", "--debug"]

EXPOSE 5005
# RUN rasa train --domain domain

# ENTRYPOINT ["/app/server.sh"]
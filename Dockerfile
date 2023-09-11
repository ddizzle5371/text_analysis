FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

ARG FILENAME
ARG HOST
ARG PORT
COPY src/api/${FILENAME} /app/${FILENAME}
RUN echo "HOST='$HOST' PORT='$PORT' python3 /app/$FILENAME \$@" > /app/entrypoint.sh
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
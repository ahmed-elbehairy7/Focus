FROM python:3.11-slim as build
WORKDIR /app
COPY . .
RUN set -ex \
    && apt-get update \
    && apt-get upgrade -y
RUN apt install python3 -y
RUN apt install -y espeak
RUN apt-get install -y alsa-utils
RUN apt-get install -y software-properties-common
RUN apt-get install -y ffmpeg
RUN apt install python3-pip -y
RUN apt install espeak -y
RUN pip install -r requirements.txt
RUN apt remove python3-pip -y
RUN chmod +x main.py 
# Clean up
RUN set -ex apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
RUN set -ex \
    # Create a non-root user
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser
RUN ls
ENTRYPOINT [ "./main.py" ]
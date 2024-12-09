FROM python:3.11.11-alpine3.20

COPY ./credentials.json /app/credentials.json
COPY ./main.py /app
COPY ./requirements.txt /requirements.txt
COPY ./zotify-main /zotify-main

# Install pipx
RUN python3 -m pip install --user pipx
ENV PATH="/root/.local/bin:${PATH}"

# Install git
RUN apk add --no-cache ffmpeg git

# Install dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Install zotify
# RUN pipx install git+https://github.com/zotify-dev/zotify.git
RUN pipx install zotify-main/

WORKDIR /app

CMD ["python3", "main.py"]

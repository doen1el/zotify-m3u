FROM python:3.9-alpine as base

# Installieren von FFmpeg
RUN apk --update add ffmpeg

# Installieren von Git
RUN apk --update add git

# Installieren von pipx
RUN python3 -m pip install --user pipx

# Fügen Sie das Verzeichnis für benutzerdefinierte Skripte dem PATH hinzu
ENV PATH="/root/.local/bin:${PATH}"

# Installieren von erforderlichen Build-Abhängigkeiten
FROM base as builder

WORKDIR /install
COPY requirements.txt /requirements.txt

RUN apk add gcc libc-dev zlib zlib-dev jpeg-dev
RUN pip install --prefix="/install" -r /requirements.txt

# Kopieren der installierten Pakete ins Basisimage
FROM base

COPY --from=builder /install /usr/local/lib/python3.9/site-packages
RUN mv /usr/local/lib/python3.9/site-packages/lib/python3.9/site-packages/* /usr/local/lib/python3.9/site-packages/

# Kopieren von zotify und dem Hauptskript
COPY zotify /app/zotify
COPY main.py /app

# Kopieren der credentials.json Datei
COPY credentials.json /app/credentials.json

# Festlegen des Arbeitsverzeichnisses
WORKDIR /app

# Installieren von zotify mit pipx und Ausführen des Hauptskripts
CMD ["sh", "-c", "pipx install https://get.zotify.xyz && python3 main.py"]

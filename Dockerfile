FROM python:3.11-slim

WORKDIR /app

# Install ffmpeg, nano and git
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg nano git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pipx
RUN python3 -m pip install --user pipx
ENV PATH="/root/.local/bin:${PATH}"

# Copy the files
COPY ./main.py ./
COPY ./zotify ./zotify
COPY ./requirements.txt ./

# Install the requirements and the zotify package
RUN pip install --no-cache-dir -r requirements.txt
RUN pipx install ./zotify

# Create the credentials.json file and the downloads folder
RUN touch ./credentials.json
RUN mkdir ./downloads

CMD ["tail", "-f", "/dev/null"]
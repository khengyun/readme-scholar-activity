FROM python:3.12-slim


WORKDIR /action/workspace
COPY requirements.txt script/*.py main.sh /action/workspace/


RUN python3 -m pip install --no-cache-dir -r requirements.txt \
    && apt-get -y update \
    && apt-get -y install --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*


CMD ["/action/workspace/scholar_activity.py"]
ENTRYPOINT ["python3", "-u"]


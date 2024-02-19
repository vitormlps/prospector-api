FROM python:3.11.7-slim-bookworm as build

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# ENV PYTHONPATH="/python-deps"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils \
    libpq-dev \
    python3-dev \
    build-essential cargo 

COPY ../requirements/* /requirements/
RUN python3 -m pip install --upgrade pip setuptools wheel --no-cache-dir \
    && python3 -m pip install -r requirements/dev.txt --no-cache-dir

### create appliaction user
ARG DOCK_USER=api

RUN groupadd -g 999 $DOCK_USER \
    && useradd -r -m -u 999 -g $DOCK_USER $DOCK_USER \
    && usermod -a -G sudo $DOCK_USER
USER $DOCK_USER
ENV USER_HOME /home/$DOCK_USER
WORKDIR /home/$DOCK_USER


############################## Devel stage ##############################
FROM base as development
USER $DOCK_USER

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["python3 src/main.py"]


############################## Prod stage ##############################
FROM base as production
USER $DOCK_USER

COPY --chown=999:999 .. ./

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["python3 src/main.py"]


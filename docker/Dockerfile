FROM --platform=linux/amd64 python:3.11.7-slim-bookworm as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils \
    sudo \
    gcc \
    python3-dev \
    libpq-dev 

RUN export PATH=/usr/lib/postgresql/15/bin/:$PATH

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


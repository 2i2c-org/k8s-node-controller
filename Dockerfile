FROM python:3.14-bookworm

RUN apt-get update > /dev/null && \
    apt-get install --yes tini > /dev/null && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir /opt/jupyterhub_node_warmer
COPY pyproject.toml /opt/jupyterhub_node_warmer
COPY LICENSE.md /opt/jupyterhub_node_warmer
COPY README.md /opt/jupyterhub_node_warmer
COPY src/jupyterhub_node_warmer /opt/jupyterhub_node_warmer

WORKDIR /opt/jupyterhub_node_warmer

RUN pip install -e .

ENTRYPOINT ["tini", "--"]

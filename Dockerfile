FROM python:3.14-bookworm

RUN apt-get update > /dev/null && \
    apt-get install --yes tini > /dev/null && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV VCS_VERSIONING_PRETEND_VERSION="0.0.0"

RUN mkdir /opt/k8s_node_controller
COPY pyproject.toml /opt/k8s_node_controller
COPY LICENSE.md /opt/k8s_node_controller
COPY README.md /opt/k8s_node_controller
COPY src/k8s_node_controller /opt/k8s_node_controller/src/k8s_node_controller

WORKDIR /opt/k8s_node_controller

RUN pip install -e .

ENTRYPOINT ["tini", "--"]
CMD ["python" "src/k8s_node_controller/app.py"]
import kopf
import os
import yaml
from google.cloud import container_v1
from google.oauth2 import service_account
from typing import Any
from dotenv import load_dotenv # type: ignore

load_dotenv()

GCP_CLUSTER = os.environ.get("GCP_CLUSTER")
GCP_MACHINE_TYPE = os.environ.get("GCP_MACHINE_TYPE")
GCP_NODEPOOL = os.environ.get("GCP_NODEPOOL")
GCP_SA_FILE = os.environ.get("GCP_SA_FILE")
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
GCP_ZONE = os.environ.get("GCP_ZONE")

def get_gcp_config(machine):
    nodepool_name = (
        f"projects/{GCP_PROJECT_ID}/locations/{GCP_ZONE}/clusters/"
        f"{GCP_CLUSTER}/nodePools/{GCP_NODEPOOL}"
    )
    credentials = service_account.Credentials.from_service_account_file(GCP_SA_FILE)
    return nodepool_name, credentials

async def change_min_node_count(credentials, nodepool_name, num):
    client = container_v1.ClusterManagerAsyncClient(
        credentials=credentials
    )
    request = container_v1.GetNodePoolRequest(
        name=nodepool_name
    )  # Get current autoscaling config
    response = await client.get_node_pool(request=request)

    config = container_v1.NodePoolAutoscaling(
        enabled=response.autoscaling.enabled,
        min_node_count=num,
        max_node_count=response.autoscaling.max_node_count,
        location_policy=response.autoscaling.location_policy,
    )
    request = container_v1.SetNodePoolAutoscalingRequest(name=nodepool_name, autoscaling=config)
    await client.set_node_pool_autoscaling(request=request)
    return response.autoscaling.min_node_count

@kopf.on.create('nodepoolallocationtarget')
async def create_fn(spec: kopf.Spec, name: str, namespace: str | None, logger: kopf.Logger, **_: Any) -> None:

    min_node_count = spec.get('minimumNodeCount')
    if not min_node_count:
        min_node_count = 0

    path = os.path.join(os.path.dirname(__file__), 'npat_template.yaml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(name=name, minimumNodeCount=min_node_count)
    data = yaml.safe_load(text)

    # Scale cluster
    nodepool_name, credentials = get_gcp_config(GCP_MACHINE_TYPE)
    await change_min_node_count(credentials, nodepool_name, int(data["spec"]["minimumNodeCount"]))
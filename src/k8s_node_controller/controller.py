import kopf
import logging
from typing import Any

@kopf.on.create('nodepoolallocationtargets')
def create_fn(body: kopf.Body, **_: Any) -> None:
    logging.info(f"A handler is called with body: {body}")
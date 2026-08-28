import asyncio
import logging
import os

from traitlets.config import Application
from traitlets import default, Integer

class NodeWarmer(Application):
  """
  Traitlets Application for running the node warmer service.
  """

  name = "jupyterhub-node-warmer"
  description = "Scale nodes for your JupyterHub ahead of time."

  aliases = {
      "log_level": "NodeWarmer.log_level",
  }

  @default("log_level")
  def _log_level_default(self):
    return os.environ.get("JUPYTERHUB_NODE_WARMER_LOG_LEVEL") or logging.INFO

  @default('log_datefmt')
  def _log_datefmt_default(self):
      """Default date format"""
      return "%Y-%m-%d %H:%M:%S"

  @default('log_format')
  def _log_format_default(self):
      """Override default log format to include time"""
      return "[%(levelname)1.1s %(asctime)s.%(msecs).03d %(name)s %(module)s:%(lineno)d] %(message)s"

  loop_interval = Integer(
    help="Interval between each asyncio loop. Default is 60 seconds."
  )

  @default('loop_interval')
  def _loop_interval_default(self):
    return int(os.environ.get("JUPYTERHUB_NODE_WARMER_LOOP_INTERVAL")) or 60

  async def run(self):
    while True:
      self.log.info('hello')
      await asyncio.sleep(self.loop_interval)
      self.log.info('world')

  def start(self):
    asyncio.run(self.run())

def main():
    NodeWarmer.launch_instance()

if __name__ == "__main__":
    main()

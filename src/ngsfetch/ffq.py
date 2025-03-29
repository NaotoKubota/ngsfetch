import sys
import logging
import time
from . import general
# Configure logger
logger = logging.getLogger(__name__)

def fetch_metadata(id, json_file, attempts = 3):
	"""
	Fetch metadata for a given ID using the ffq command line tool."
	"""
	command = ["ffq", "--verbose", "--ftp", id, "-o", f"{json_file}"]
	logger.debug(f"Executing command: {command}")
	for attempt in range(attempts):
		returncode = general.execute_command(command)
		if returncode == 0:
			logger.info(f"Metadata fetched for {id} on attempt {attempt + 1}")
			return 0
		else:
			logger.warning(f"Attempt {attempt + 1} failed to fetch metadata for {id}. Retrying...")
			time.sleep(5)  # Optional: Add a delay between retries
	logger.error(f"Failed to fetch metadata for {id} after {attempts} attempts")
	sys.exit(1)

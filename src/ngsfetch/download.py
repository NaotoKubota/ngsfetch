import json
import logging
import os
import subprocess
import time
from pathlib import Path
logger = logging.getLogger(__name__)

def extract_from_flat_fastq_json(json_file, md5_fastq_table):
	"""
	Extract md5 and ftp url from a flat fastq json file.
	"""
	logger.debug(f"Reading JSON file: {json_file}")
	with open(json_file, "r") as f:
		records = json.load(f)
	logger.debug(f"Loaded {len(records)} records from JSON file.")
	output_lines = []
	for record in records:
		md5 = record.get("md5")
		url = record.get("url")
		if md5 and url:
			output_lines.append(f"{md5}\t{url}")
		else:
			logger.warning(f"Record missing 'md5' or 'url': {record}")
	logger.debug(f"Writing output to file: {md5_fastq_table}")
	with open(md5_fastq_table, "w") as f:
		f.write("\n".join(output_lines))
	logger.debug("File writing complete.")
	return 0

def fetch_fastq(md5_fastq_table, fastq_dir, processes = 1, attempts = 3):
	"""
	Fetch fastq files using aria2c.
	"""
	with open(md5_fastq_table, "r") as f:
		lines = f.readlines()
		logger.debug(f"Loaded {len(lines)} lines from fastq table.")
		# Extract file names from url
		for line in lines:
			md5, url = line.strip().split("\t")
			file_name = url.split("/")[-1]
			file_path = f"{fastq_dir}/{file_name}"
			logger.debug(f"Downloading {file_name} to {file_path}")
			# Check if file already exists
			if os.path.exists(file_path):
				logger.info(f"File {file_path} already exists. Skipping download.")
			else:
				continue
			# Download file using aria2c
			command = ["aria2c", "-x", str(processes), "-d", fastq_dir, url]
			log_file = f"{fastq_dir}/log/{file_name}.aria2c.log"
			for attempt in range(attempts):
				returncode = general.execute_command(command, log_file=log_file)
				if returncode == 0:
					logger.info(f"Downloaded {file_name} on attempt {attempt + 1}")
					# Verify md5 checksum
					md5sum_command = ["md5sum", "-c"]
					try:
						with open(f"{fastq_dir}/log/md5sum.log", "a") as md5_log:
							md5_log.write(f"{md5}  {file_path}\n")
							md5_log.flush()
							process = subprocess.Popen(md5sum_command, stdin=subprocess.PIPE, stdout=md5_log, stderr=md5_log)
							process.communicate(input=f"{md5}  {file_path}\n".encode())
						if process.returncode == 0:
							logger.info(f"MD5 checksum verified for {file_name}")
						else:
							logger.error(f"MD5 checksum failed for {file_name}")
					except Exception as e:
						logger.error(f"An error occurred during MD5 verification: {e}")
				else:
					# Retry download
					if attempt < attempts - 1:
						logger.info(f"Retrying download for {file_name}...")
						time.sleep(5)
					else:
						logger.error(f"Failed to download {file_name} after {attempts} attempts.")
						break
	# Check if all files were downloaded
	downloaded_files = os.listdir(fastq_dir)
	downloaded_files = [file for file in downloaded_files if file.endswith(".fastq.gz")]
	if len(downloaded_files) == len(lines):
		logger.info("All files downloaded successfully.")
	else:
		logger.warning(f"Some files were not downloaded. Expected {len(lines)} but got {len(downloaded_files)}.")
	return 0

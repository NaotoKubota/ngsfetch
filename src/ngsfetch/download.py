import json
import logging
import os
import subprocess
import time
from . import general
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
		file_name = url.split("/")[-1] if url else None
		if md5 and url and file_name.endswith(".fastq.gz"): # Only include fastq.gz files
			output_lines.append(f"{md5}\t{url}")
		else:
			logger.warning(f"Skipping record with missing md5 or url, or non-fastq.gz file: {record}")
	logger.debug(f"Writing output to file: {md5_fastq_table}")
	with open(md5_fastq_table, "w") as f:
		f.write("\n".join(output_lines) + "\n")
	logger.debug("File writing complete.")
	return 0

def fetch_fastq(md5_fastq_table, fastq_dir, processes = 1, attempts = 3):
	"""
	Fetch fastq files using aria2c.
	"""
	with open(md5_fastq_table, "r") as f:
		lines = [line.strip() for line in f if line.strip()]
	total = len(lines)
	logger.debug(f"Loaded {total} lines from fastq table.")
	failed_files = []
	# Extract file names from url
	for line in lines:
		md5, url = line.split("\t")
		file_name = url.split("/")[-1]
		file_path = f"{fastq_dir}/{file_name}"
		logger.debug(f"Downloading {file_name} to {file_path}")
		# Check if file already exists
		if os.path.exists(file_path):
			logger.info(f"File {file_path} already exists. Skipping download.")
			continue
		# Download file using aria2c
		command = ["aria2c", "-x", str(processes), "-d", fastq_dir, url]
		log_file = f"{fastq_dir}/log/{file_name}.aria2c.log"
		success = False
		for attempt in range(attempts):
			logger.info(f"Attempt {attempt + 1} to download {file_name}")
			returncode = general.execute_command(command, log_file=log_file)
			if returncode == 0:
				logger.info(f"Downloaded {file_name}")
				# Verify md5 checksum
				md5sum_command = ["md5sum", "-c"]
				try:
					with open(f"{fastq_dir}/log/md5sum.log", "a") as md5_log:
						process = subprocess.Popen(md5sum_command, stdin=subprocess.PIPE, stdout=md5_log, stderr=md5_log)
						process.communicate(input=f"{md5}  {file_path}\n".encode())
					if process.returncode == 0:
						logger.info(f"MD5 checksum verified for {file_name}")
						success = True
						break
					else:
						logger.error(f"MD5 checksum failed for {file_name}")
						# Remove the file if checksum fails
						os.remove(file_path)
						logger.info(f"Removed {file_path} due to checksum failure.")
				except Exception as e:
					logger.error(f"An error occurred during MD5 verification: {e}")
			# Retry unless this was the last attempt
			if attempt < attempts - 1:
				logger.info(f"Retrying download for {file_name}...")
				time.sleep(5)
		if not success:
			logger.error(f"Failed to download {file_name} after {attempts} attempts.")
			# Remove any partial output so it is not mistaken for a complete file
			for leftover in (file_path, f"{file_path}.aria2"):
				if os.path.exists(leftover):
					os.remove(leftover)
					logger.info(f"Removed incomplete file {leftover}")
			failed_files.append(file_name)
	# Report based on tracked results, not files left on disk
	if failed_files:
		logger.error(f"Completed with {len(failed_files)}/{total} files failed: {failed_files}")
		return 1
	logger.info(f"All {total} files downloaded successfully.")
	return 0

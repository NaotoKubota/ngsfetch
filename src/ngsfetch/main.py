import argparse
import sys
import os
import logging
import time
from . import ffq, download
# Configure logger
logger = logging.getLogger(__name__)
# Set version
VERSION = "v0.1.0"

def parse_args():
	parser = argparse.ArgumentParser(
		description=f"ngsfetch {VERSION} - fast retrieval of metadata and fastq files with ffq and aria2c",
	)

	parser.add_argument("-i", "--id", type = str, help = "ID of the data to fetch")
	parser.add_argument("-o", "--output", type = str, help = "Output directory")
	parser.add_argument("-p", "--processes", type=int, default=1, help="Number of processes to use (up to 16)")
	parser.add_argument("--attempts", type = int, default = 3, help = "Number of attempts to fetch metadata and fastq files")
	parser.add_argument("-v", "--verbose", action = "store_true", help = "Increase verbosity")
	args = parser.parse_args()
	return args

def main():

	# Get arguments
	args = parse_args()

	# Set up logging
	logging.basicConfig(
		format = "[%(asctime)s] %(levelname)7s %(message)s",
		level = logging.DEBUG if args.verbose else logging.INFO
	)

	# Validate input and config
	logger.info(f"Running ngsfetch ({VERSION})")
	time.sleep(1)
	logger.debug(f"Arguments: {args}")

	# Make output directory
	output_dir = args.output
	fastq_dir = os.path.join(output_dir, 'fastq')
	logger.debug("Making output directory...")
	os.makedirs(os.path.join(fastq_dir, 'log'), exist_ok=True)

	# Fetch metadata with ffq
	time.sleep(1)
	json_file = os.path.join(output_dir, f"{args.id}_metadata.json")
	if os.path.exists(json_file):
		logger.info(f"Metadata file {json_file} already exists")
	else:
		logger.info(f"Fetching metadata for {args.id}")
		_returncode = ffq.fetch_metadata(args.id, json_file, attempts=args.attempts)

	# Make a fastq url table
	logger.info(f"Making fastq url table from {json_file}")
	md5_fastq_table = os.path.join(output_dir, f"{args.id}_fastq_ftp.txt")
	if os.path.exists(md5_fastq_table):
		logger.info(f"Fastq url table {md5_fastq_table} already exists")
	else:
		_returncode = download.extract_from_flat_fastq_json(json_file, md5_fastq_table)

	# Download fastq files with aria2c
	logger.info(f"Downloading fastq files from {md5_fastq_table}")
	_returncode = download.fetch_fastq(md5_fastq_table, fastq_dir, processes = args.processes, attempts=args.attempts)

	logger.info("Done!")
	logger.info(f"Fastq files downloaded to {fastq_dir}")
	logger.info(f"Metadata file saved to {json_file}")
	logger.info(f"Fastq url table saved to {md5_fastq_table}")
	logger.info("Exiting...")
	return 0

if __name__ == "__main__":
	main()

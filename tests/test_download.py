import os

from ngsfetch import download


class FakePopen:
	"""Minimal stand-in for subprocess.Popen used by the md5 check."""

	def __init__(self, *args, **kwargs):
		self.returncode = 0

	def communicate(self, input=None):
		return (b"", b"")


def _make_layout(tmp_path):
	fastq_dir = tmp_path / "fastq"
	(fastq_dir / "log").mkdir(parents=True)
	url = "ftp://ftp.example.invalid/vol1/fastq/SRR000/SRR000_1.fastq.gz"
	table = tmp_path / "table.txt"
	table.write_text(f"fakemd5\t{url}\n")
	return fastq_dir, table


def test_fetch_fastq_reports_failure_and_cleans_up(tmp_path, monkeypatch):
	fastq_dir, table = _make_layout(tmp_path)

	def fake_execute_command(command, log_file=None):
		# Simulate aria2c leaving a truncated file behind, then failing.
		dest_dir = command[command.index("-d") + 1]
		file_name = command[-1].split("/")[-1]
		with open(os.path.join(dest_dir, file_name), "wb") as fh:
			fh.write(b"partial")
		return 1

	monkeypatch.setattr(download.general, "execute_command", fake_execute_command)

	rc = download.fetch_fastq(str(table), str(fastq_dir), processes=1, attempts=1)

	assert rc == 1
	assert not (fastq_dir / "SRR000_1.fastq.gz").exists()
	assert not (fastq_dir / "SRR000_1.fastq.gz.aria2").exists()


def test_fetch_fastq_reports_success(tmp_path, monkeypatch):
	fastq_dir, table = _make_layout(tmp_path)

	def fake_execute_command(command, log_file=None):
		dest_dir = command[command.index("-d") + 1]
		file_name = command[-1].split("/")[-1]
		with open(os.path.join(dest_dir, file_name), "wb") as fh:
			fh.write(b"complete")
		return 0

	monkeypatch.setattr(download.general, "execute_command", fake_execute_command)
	monkeypatch.setattr(download.subprocess, "Popen", FakePopen)

	rc = download.fetch_fastq(str(table), str(fastq_dir), processes=1, attempts=1)

	assert rc == 0
	assert (fastq_dir / "SRR000_1.fastq.gz").exists()

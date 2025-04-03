# ngsfetch (v0.1.1)

[![GitHub License](https://img.shields.io/github/license/NaotoKubota/ngsfetch)](https://github.com/NaotoKubota/ngsfetch/blob/main/LICENSE)
[![DOI](https://zenodo.org/badge/956254675.svg)](https://doi.org/10.5281/zenodo.15107010)
[![GitHub Release](https://img.shields.io/github/v/release/NaotoKubota/ngsfetch?style=flat)](https://github.com/NaotoKubota/ngsfetch/releases)
[![GitHub Release Date](https://img.shields.io/github/release-date/NaotoKubota/ngsfetch)](https://github.com/NaotoKubota/ngsfetch/releases)
[![Create Release](https://github.com/NaotoKubota/ngsfetch/actions/workflows/release.yaml/badge.svg)](https://github.com/NaotoKubota/ngsfetch/actions/workflows/release.yaml)
[![Publish PyPI](https://github.com/NaotoKubota/ngsfetch/actions/workflows/publish.yaml/badge.svg)](https://github.com/NaotoKubota/ngsfetch/actions/workflows/publish.yaml)
[![Python](https://img.shields.io/pypi/pyversions/ngsfetch.svg?label=Python&color=blue)](https://pypi.org/project/ngsfetch/)
[![PyPI](https://img.shields.io/pypi/v/ngsfetch.svg?label=PyPI&color=orange)](https://pypi.org/project/ngsfetch/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ngsfetch.svg?label=PyPI%20-%20Downloads&color=orange)](https://pypi.org/project/ngsfetch/)
[![Conda](https://img.shields.io/conda/v/bioconda/ngsfetch?color=3EB049)](https://anaconda.org/bioconda/ngsfetch)
[![Conda - Downloads](https://img.shields.io/conda/dn/bioconda/ngsfetch?label=Conda%20-%20Downloads&color=3EB049)](https://anaconda.org/bioconda/ngsfetch)
[![Docker](https://img.shields.io/docker/v/naotokubota/ngsfetch?color=blue&label=Docker)](https://hub.docker.com/r/naotokubota/ngsfetch)
[![Docker Pulls](https://img.shields.io/docker/pulls/naotokubota/ngsfetch)](https://hub.docker.com/r/naotokubota/ngsfetch)
[![Docker Image Size](https://img.shields.io/docker/image-size/naotokubota/ngsfetch)](https://hub.docker.com/r/naotokubota/ngsfetch)

A utility to retrieve fastq files with [ffq](https://github.com/pachterlab/ffq) and [aria2](https://aria2.github.io/). It is designed to be fast and efficient, allowing you to download large datasets quickly and easily. This tool can be used to fetch fastq files from various public repositories, including:

- [GEO](https://www.ncbi.nlm.nih.gov/geo/): Gene Expression Omnibus,
- [SRA](https://www.ncbi.nlm.nih.gov/sra): Sequence Read Archive,
- [EMBL-EBI](https://www.ebi.ac.uk/): European Molecular BIology Laboratory’s European BIoinformatics Institute,
- [DDBJ](https://www.ddbj.nig.ac.jp/index-e.html): DNA Data Bank of Japan.

> [!IMPORTANT]
> - **Fast**: Uses `aria2` to download files in parallel, which can significantly speed up the download process.
> - **Integrity**: Verifies the integrity of downloaded files using `md5sum` to ensure that the files are not corrupted during the download process.
> - **Retry Mechanism**: Automatically attempts to re-download files if the initial download fails, ensuring successful retrieval of data.

## Quick start

```bash
# Fetch fastq files of GSE52856
ngsfetch -i GSE52856 -o /path/to/output/GSE52856 -p 16

# Fetch fastq files of SRP175008
ngsfetch -i SRP175008 -o /path/to/output/SRP175008 -p 16

# Fetch fastq files of ERP126666
ngsfetch -i ERP126666 -o /path/to/output/ERP126666 -p 16
```

## How to install

### pip

```bash
pip install ngsfetch
```

or

```bash
git clone https://github.com/NaotoKubota/ngsfetch.git
cd ngsfetch
pip install .
```

### conda

```bash
conda create -n ngsfetch python=3.9
conda activate ngsfetch
conda install -c bioconda ngsfetch
```

### Docker

```bash
docker pull naotokubota/ngsfetch
```

## Dependencies

### Operating system

- Linux (i.e. where the `md5sum` command is available)

> [!TIP]
> Are you using MacOS or Windows? Don't worry! You can use [Docker](https://www.docker.com/) to run `ngsfetch` on your local machine. Just install Docker and run the following command:
> ```bash
> docker run -it --rm -v /path/to/output:/data naotokubota/ngsfetch ngsfetch -i GSE52856 -o /data/GSE52856 -p 16
> ```
> This command will mount the `/path/to/output` directory on your local machine to the `/data` directory in the Docker container, allowing you to access the downloaded files on your local machine.
> Make sure to replace `/path/to/output` with the actual path where you want to save the downloaded files.

### python packages

- python (>=3.9)
- ffq (>=0.3.1)
- aria2 (>=0.0.1b0)

## Usage

```bash
usage: ngsfetch [-h] [-i ID] [-o OUTPUT] [-p PROCESSES] [--attempts ATTEMPTS] [-v]

ngsfetch v0.1.1 - fast retrieval of metadata and fastq files with ffq and aria2c

optional arguments:
  -h, --help            show this help message and exit
  -i ID, --id ID        ID of the data to fetch
  -o OUTPUT, --output OUTPUT
                        Output directory
  -p PROCESSES, --processes PROCESSES
                        Number of processes to use (up to 16)
  --attempts ATTEMPTS   Number of attempts to fetch metadata and fastq files
  -v, --verbose         Increase verbosity
```

## Contributing

Thank you for wanting to improve ngsfetch! If you have any bugs or questions, feel free to [open an issue](https://github.com/NaotoKubota/ngsfetch/issues) or pull request.

## Authors

- Naoto Kubota ([0000-0003-0612-2300](https://orcid.org/0000-0003-0612-2300))

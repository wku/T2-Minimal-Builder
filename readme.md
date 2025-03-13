# T2 SDE Minimal Linux Build in Docker

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Docker](https://img.shields.io/badge/docker-20.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

This project provides a Python script to build a minimal Linux system using T2 System Development Environment (T2 SDE), packaged in a Docker container for easy deployment and dependency management. The script includes options to control CPU usage during the build process.

## Key Features

- Automated T2 SDE build process in an isolated Docker environment.
- Configurable number of CPU cores used for building (via `--jobs` or `JOBS` environment variable).
- Logging to the `logs` folder on the host machine.
- Restart capability via a Bash script.

## Requirements

- **Docker**: Version 20.x or higher.
- **Docker Compose**: Version 1.29 or higher.

### Installing Docker (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/t2-sde-build.git
   cd t2-sde-build
   ```

2. Verify Docker is installed:
   ```bash
   docker --version
   docker-compose --version
   ```

## Usage

1. Run the build process with Docker Compose (default: half of CPU cores):
   ```bash
   docker-compose up
   ```

2. To specify the number of CPU cores, set the `JOBS` environment variable in `docker-compose.yml`:
   ```yaml
   environment:
     - PYTHONUNBUFFERED=1
     - JOBS=2  # Use 2 CPU cores
   ```
   Then run:
   ```bash
   docker-compose up
   ```

3. Alternatively, pass the `--jobs` argument:
   ```bash
   docker-compose run t2-builder python3 build_t2_iso.py --jobs 2
   ```

4. To restart the process, use the script:
   ```bash
   chmod +x restart.sh
   ./restart.sh
   ```

5. Logs are saved to the `logs` folder on the host.

### What Does the Script Do?

- Downloads T2 SDE version 24.6.
- Extracts the archive and configures a minimal system.
- Builds an ISO image within the container, using a configurable number of CPU cores.

## Project Structure

```
t2-sde-build/
│
├── build_t2_iso.py    # Python build script
├── Dockerfile         # Docker image build file
├── docker-compose.yml # Docker Compose configuration
├── restart.sh         # Restart script
├── logs/             # Directory for logs (created automatically)
└── README.md         # This file
```

## Configuration

- **`--jobs`**: Command-line argument to set the number of parallel build jobs (e.g., `--jobs 2`). Defaults to half of available CPU cores.
- **`JOBS`**: Environment variable to override the number of jobs (e.g., `export JOBS=2`).

Example:
```bash
export JOBS=2
docker-compose up
```

## Possible Issues

- **Docker not running**: Ensure the Docker service is active (`sudo systemctl status docker`).
- **Insufficient disk space**: Check available disk space for downloading and building.
- **Build errors**: Review logs in the `logs` folder for troubleshooting.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests with suggestions or fixes.

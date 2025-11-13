# PHP LFI (Local File Inclusion) Lab

This lab demonstrates a Local File Inclusion vulnerability in PHP applications.

## Setup

1. Ensure Docker and Docker Compose are installed on your system.

2. Navigate to the `SSRF-PHP-LFI` directory:
   ```bash
   cd SSRF-PHP-LFI
   ```

3. Start the lab environment:
   ```bash
   docker-compose up -d --build
   ```

4. Access the application at `http://localhost:8080`

## Lab Description

The application has a vulnerable `include()` statement that allows attackers to include arbitrary local files by manipulating the `page` GET parameter.

## Cleanup

To stop and remove the containers:
```bash
docker-compose down
```

## Security Note
This is a deliberately vulnerable application for educational purposes only. Never deploy code like this in production.
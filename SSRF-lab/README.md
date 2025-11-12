# SSRF Lab

This lab demonstrates Server-Side Request Forgery (SSRF) vulnerability with a single server.

## Setup

Run the following command to start the lab:

```bash
docker-compose up --build
```

## Server

- **Victim** (http://localhost:8080): Server with SSRF vulnerability and a private endpoint.

## Endpoints

- `/`: Web page with form to enter URL to fetch
- `/fetch?url=...`: Fetches the provided URL and returns the content
- `/secret`: Private endpoint that returns sensitive data, only accessible from localhost (within the container)

## Attack

To exploit the SSRF:

1. Visit http://localhost:8080
2. Use the form to fetch `http://localhost:8080/secret`
3. The server will fetch the secret data internally, revealing the flag

The `/secret` endpoint is protected by IP check (only allows 127.0.0.1), but since the `/fetch` endpoint can access internal URLs, it can bypass this restriction.

## Cleanup

```bash
docker-compose down
```
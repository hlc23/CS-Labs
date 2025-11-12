# SSRF Bypass Lab

This lab demonstrates Server-Side Request Forgery (SSRF) vulnerability with hostname validation bypass techniques.

## Setup

Run the following command to start the lab:

```bash
docker-compose up --build
```

## Server

- **Victim** (http://localhost:8080): Server with SSRF vulnerability that attempts to restrict requests to httpbin.dev domains.

## Endpoints

- `/`: Web page with form to enter URL to request
- `/mkreq?url=...`: Makes a request to the provided URL, but only allows hostnames starting with "httpbin.dev"
- `/internal-only`: Private endpoint that returns a flag, only accessible from 127.0.0.1
- `/?debug=1`: Debug mode that reveals the source code

## Vulnerability

The `/mkreq` endpoint checks if the hostname starts with "httpbin.dev", but this can be bypassed using various SSRF techniques:

1. **DNS Rebinding**: Use a domain that resolves to internal IPs
2. **URL Parsing Tricks**: Manipulate the URL to bypass the check
3. **Redirects**: Use services that redirect to internal URLs
4. **IPv6**: Use IPv6 addresses to bypass hostname checks

## Goal

The goal is to access the `/internal-only` endpoint to retrieve the flag, despite the hostname restriction.

## Cleanup

```bash
docker-compose down
```
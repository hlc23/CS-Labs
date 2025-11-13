# SSRF Bypass Lab

This lab demonstrates Server-Side Request Forgery (SSRF) vulnerability with hostname validation bypass techniques.

## Setup

Run the following command to start the lab:

```bash
docker-compose up --build
```

## Goal

The goal is to access the `/internal-only` endpoint to retrieve the flag, despite the hostname restriction.

## Cleanup

```bash
docker-compose down
```

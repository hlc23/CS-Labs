# SSRF + DNS Rebind Lab

This lab demonstrates a common SSRF mitigation (DNS check) that can be bypassed via DNS rebinding.

Overview
- `victim` (Flask) performs a DNS resolution check before fetching a URL, blocking requests to private IPs.
- `attacker` runs a DNS server that first resolves `rebind.local` to the attacker web server, then on subsequent queries returns a private IP (the `admin` service) — performing a DNS rebound.
- `admin` is an internal service (private IP) that hosts a sensitive endpoint.

Goal
- Show that the victim checks DNS once but performs the HTTP request later — allowing a DNS rebind attack to make the request go to the internal `admin` service.

Files
- `docker-compose.yml` - sets up a small Docker network and three services.
- `victim/` - Flask app that does the DNS check then fetch.
- `attacker/` - DNS+HTTP server that alternates DNS responses per client.
- `admin/` - internal service returning a mock secret.

Run the lab
1. From this folder run:

```bash
docker compose up --build -d
```

2. Access the victim web interface at http://localhost:5000 to test the SSRF protection and exploit.

3. Alternatively, access the attacker web UI at http://localhost:8080/ui for a different interface.

4. To test the SSRF attack, enter `http://rebind.local:8081/secret` in the URL field. This should bypass the DNS check and retrieve the secret from the admin service.

What to expect
- The victim will perform a DNS check and see `rebind.local` resolves to an attacker IP (public), so it allows the fetch.
- The attacker DNS will then rebind `rebind.local` to the private `admin` IP, and the subsequent HTTP request from the victim will go to `admin`, returning the secret.

Notes
- This lab is intended for learning in a safe, isolated environment.
- The demo places all services in a custom Docker network so the rebind target is reachable inside the network.

If you want I can run the environment now and demonstrate the exploit automatically.
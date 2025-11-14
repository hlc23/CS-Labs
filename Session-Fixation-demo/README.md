# Session Fixation Demo

This demo illustrates a Session Fixation vulnerability.

## Setup

1. Run `docker-compose up --build`
2. Visit the attacker site at http://localhost:5001
3. Click the link to go to the victim login with a fixed session ID.
4. Log in with any username/password.
5. Now, the session ID is fixed to 'abc123'.
6. To simulate the attacker accessing the session, open browser dev tools, set a cookie named 'sessionid' with value 'abc123' for localhost:5000, and visit http://localhost:5000/profile.

## How it works

The victim application accepts a `session_id` parameter in the login URL and uses it for the session instead of generating a new one. In a real vulnerability, this might happen through other means, but this demonstrates the concept.

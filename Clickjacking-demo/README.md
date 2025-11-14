# Clickjacking Demo

This demo illustrates a clickjacking attack.

## Components

- **Victim**: A simple web page with a "Delete Account" button that shows an "Account deleted!" message when clicked.
- **Attacker**: A page that embeds the victim page in a hidden iframe and overlays a fake "Claim Free Nitro!" button. The overlay allows clicks to pass through to the iframe. There's also a "Toggle Iframe Visibility" button to reveal the embedded iframe.

## Running the Demo

1. Build and start the services:
   ```
   docker-compose up --build
   ```

2. Access the victim site at `http://localhost:5000`

3. Access the attacker site at `http://localhost:5001`

On the attacker site, the victim page is embedded in a hidden iframe with a transparent overlay. The fake "Claim Free Nitro!" button on the overlay has `pointer-events: none`, so clicks on it actually interact with the "Delete Account" button in the iframe below. Use the "Toggle Iframe Visibility" button to see the embedded victim page.

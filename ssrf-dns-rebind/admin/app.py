from flask import Flask
app = Flask(__name__)

@app.route('/secret')
def secret():
    # Mock internal secret (example of sensitive metadata)
    return 'METADATA: AWS_ACCESS_KEY_ID=EXAMPLEKEY\nAWS_SECRET_ACCESS_KEY=EXAMPLESECRET'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

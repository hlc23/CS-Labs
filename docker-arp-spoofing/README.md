Origin Repository: https://github.com/themithy/docker-arp-spoofing


# Docker ARP spoofing problem

Although the default network bridge created between containers should not allow
for easy sniffing even with the NET_ADMIN capability, it is still susceptible
to ARP spoofing.

The following setup will include two parties (*sender* and *receiver*) sending
plain unencrypted data using `netcat` on port 80, and a *attacker* running
simple sniffer:
```
docker-compose up
```

Now start spoofing ARP packets:
```
docker exec attacker /usr/sbin/arpspoof -r -t sender receiver
```

You can see the traffic being captured in the stdout of `docker-compose`
command.

Beside securing the communication between parties there are at least two simple
fixes to this situation.

**Fix #1**: Drop NET_RAW capability from offending container:
```
  attacker:
    ...
    cap_drop:
      - NET_RAW
```

**Fix #2**: Create a network bridge for communicating parties:
```
services:
  receiver:
    ...
    networks:
      - tunnel
  sender:
    ...
    networks:
      - tunnel
  ...
networks:
  tunnel:
```

Remember: A root inside the container is still a potent figure, even with
limitations applied by docker. It is therefore possible to run different
attacks or even escape docker to the host by exploiting syscalls in an
unforeseen way.

Conclusion: Docker does a fairly good job at securing containers, but as usual
the restrictions implemented are balancing the needs of different software on
that will run inside of it. In production setup consider dropping unneeded
capabilities or run software as a non-root user.

#!/bin/sh

iptables -N SSH
iptables -N SSH_ABL
iptables -A SSH -m recent --name SSH_ABL --update --seconds 3600 -j REJECT
iptables -A SSH -m recent --name SSH --rcheck --seconds 60 --hitcount 3 -j SSH_ABL
iptables -A SSH_ABL -m recent --name SSH_ABL --set -j LOG --log-level warn --log-prefix "ABL: +SSH:"
iptables -A SSH_ABL -j REJECT
iptables -A SSH -m recent --name SSH --rcheck --seconds 2 -j LOG --log-level warn --log-prefix "RATE:"
iptables -A SSH -m recent --name SSH --update --seconds 2 -j REJECT
iptables -A SSH -m recent --name SSH_ABL --remove -j LOG --log-level warn --log-prefix "ABL: -SSH:"
iptables -A SSH -m recent --name SSH --set -j ACCEPT
iptables -A INPUT -m state --state NEW -p tcp -m tcp --dport 22 -j SSH

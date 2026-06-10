import os
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from base_nodes import SwitchL3, Router

# Saltillo site
#
# 1 Router     (saltillo)
# 1 Core       (sSALc1)
# 3 Dist       (sSALd1-3)
# 11 Access    (sSALl, sSALf11-13, sSALf21-24, sSALf31-33)
# 1 Server     (hSALsrv1) — VLAN 130, runs DNS/DHCP (dnsmasq) + web (python3 http.server)
#
# VLANs
#   20  Engineering  10.30.20.0/25   gw 10.30.20.1
#   50  Reception    10.30.50.0/27   gw 10.30.50.1
#   99  Uplink       10.30.99.0/30   p2p gateway ↔ core
#  130  Servers      10.30.130.0/24  gw 10.30.130.254
#
# Link/port map for sSALc1 (derived from addLink order):
#   eth1 → saltillo   (tag=99)
#   eth2 → sSALd1     (trunk 20,50)
#   eth3 → sSALd2     (trunk 20,50)
#   eth4 → sSALd3     (trunk 20,50)
#   eth5 → hSALsrv1   (tag=130)


class Saltillo:

    def __init__(self):
        self.gateway = None

    def build(self, net):
        self.gateway = net.addHost('saltillo', cls=Router)
        sSALc1 = net.addSwitch('sSALc1', cls=SwitchL3, failMode='standalone')

        # Distribution switches
        sSALd1 = net.addSwitch('sSALd1', failMode='standalone')  # Floor 1 & Lobby
        sSALd2 = net.addSwitch('sSALd2', failMode='standalone')  # Floor 2
        sSALd3 = net.addSwitch('sSALd3', failMode='standalone')  # Floor 3

        # Floor 1 access switches
        sSALl1   = net.addSwitch('sSALl1',   failMode='standalone')  # Lobby PoE
        sSALf11 = net.addSwitch('sSALf11', failMode='standalone')  # Non-PoE 48P (1)
        sSALf12 = net.addSwitch('sSALf12', failMode='standalone')  # Non-PoE 48P (2)
        sSALf13 = net.addSwitch('sSALf13', failMode='standalone')  # PoE 48P

        # Floor 2 access switches
        sSALf21 = net.addSwitch('sSALf21', failMode='standalone')  # Non-PoE 24P
        sSALf22 = net.addSwitch('sSALf22', failMode='standalone')  # Non-PoE 48P (1)
        sSALf23 = net.addSwitch('sSALf23', failMode='standalone')  # Non-PoE 48P (2)
        sSALf24 = net.addSwitch('sSALf24', failMode='standalone')  # PoE 12P

        # Floor 3 access switches
        sSALf31 = net.addSwitch('sSALf31', failMode='standalone')  # Non-PoE 24P
        sSALf32 = net.addSwitch('sSALf32', failMode='standalone')  # PoE 24P
        sSALf33 = net.addSwitch('sSALf33', failMode='standalone')  # Non-PoE 48P

        # ── Switch links ──────────────────────────────────────────────
        net.addLink(self.gateway, sSALc1)  # saltillo-eth0 ↔ sSALc1-eth1

        net.addLink(sSALc1, sSALd1)        # sSALc1-eth2  ↔ sSALd1-eth1
        net.addLink(sSALc1, sSALd2)        # sSALc1-eth3  ↔ sSALd2-eth1
        net.addLink(sSALc1, sSALd3)        # sSALc1-eth4  ↔ sSALd3-eth1

        net.addLink(sSALd1, sSALl1)         # sSALd1-eth2  ↔ sSALl1-eth1
        net.addLink(sSALd1, sSALf11)       # sSALd1-eth3  ↔ sSALf11-eth1
        net.addLink(sSALd1, sSALf12)       # sSALd1-eth4  ↔ sSALf12-eth1
        net.addLink(sSALd1, sSALf13)       # sSALd1-eth5  ↔ sSALf13-eth1

        net.addLink(sSALd2, sSALf21)       # sSALd2-eth2  ↔ sSALf21-eth1
        net.addLink(sSALd2, sSALf22)       # sSALd2-eth3  ↔ sSALf22-eth1
        net.addLink(sSALd2, sSALf23)       # sSALd2-eth4  ↔ sSALf23-eth1
        net.addLink(sSALd2, sSALf24)       # sSALd2-eth5  ↔ sSALf24-eth1

        net.addLink(sSALd3, sSALf31)       # sSALd3-eth2  ↔ sSALf31-eth1
        net.addLink(sSALd3, sSALf32)       # sSALd3-eth3  ↔ sSALf32-eth1
        net.addLink(sSALd3, sSALf33)       # sSALd3-eth4  ↔ sSALf33-eth1

        # ── Representative hosts ──────────────────────────────────────

        # Engineering - VLAN 20
        hSALf1eng1 = net.addHost('hSALf1eng1', ip='10.30.20.10/25')
        hSALf2eng1 = net.addHost('hSALf2eng1', ip='10.30.20.20/25')
        hSALf3eng1 = net.addHost('hSALf3eng1', ip='10.30.20.30/25')

        net.addLink(hSALf1eng1, sSALf11)   # hSALf1eng1-eth0 ↔ sSALf11-eth2
        net.addLink(hSALf2eng1, sSALf21)   # hSALf2eng1-eth0 ↔ sSALf21-eth2
        net.addLink(hSALf3eng1, sSALf31)   # hSALf3eng1-eth0 ↔ sSALf31-eth2

        # Reception - VLAN 50 (lobby & floor 1 use DHCP; floors 2-3 static)
        hSALlrec1  = net.addHost('hSALlrec1',  ip=None)
        hSALf1rec1 = net.addHost('hSALf1rec1', ip=None)
        hSALf2rec1 = net.addHost('hSALf2rec1', ip='10.30.50.20/27')
        hSALf3rec1 = net.addHost('hSALf3rec1', ip='10.30.50.30/27')

        net.addLink(hSALlrec1,  sSALl1)     # hSALlrec1-eth0  ↔ sSALl1-eth2
        net.addLink(hSALf1rec1, sSALf11)   # hSALf1rec1-eth0 ↔ sSALf11-eth3
        net.addLink(hSALf2rec1, sSALf21)   # hSALf2rec1-eth0 ↔ sSALf21-eth3
        net.addLink(hSALf3rec1, sSALf31)   # hSALf3rec1-eth0 ↔ sSALf31-eth3

        # Server - VLAN 130 (DNS/DHCP + web)
        hSALsrv1 = net.addHost('hSALsrv1', ip=None)
        net.addLink(sSALc1, hSALsrv1)      # sSALc1-eth5 ↔ hSALsrv1-eth0

        print("Saltillo site built successfully!")

    def config(self, net):
        sSALc1  = net.get('sSALc1')
        sSALd1  = net.get('sSALd1')
        sSALd2  = net.get('sSALd2')
        sSALd3  = net.get('sSALd3')
        sSALl1   = net.get('sSALl1')
        sSALf11 = net.get('sSALf11')
        sSALf12 = net.get('sSALf12')
        sSALf13 = net.get('sSALf13')
        sSALf21 = net.get('sSALf21')
        sSALf22 = net.get('sSALf22')
        sSALf23 = net.get('sSALf23')
        sSALf24 = net.get('sSALf24')
        sSALf31 = net.get('sSALf31')
        sSALf32 = net.get('sSALf32')
        sSALf33 = net.get('sSALf33')
        hSALsrv1 = net.get('hSALsrv1')

        # ── Gateway (WAN router) ──────────────────────────────────────
        self.gateway.setIP('10.30.99.1/30', intf='saltillo-eth0')
        self.gateway.cmd('ip route add 10.30.0.0/16 via 10.30.99.2')

        # ── Core switch: SVIs ─────────────────────────────────────────
        # VLAN 99 – p2p uplink to gateway
        sSALc1.cmd('ovs-vsctl add-port sSALc1 salc1.v99  tag=99  -- set interface salc1.v99  type=internal')
        sSALc1.cmd('ip addr add 10.30.99.2/30   dev salc1.v99  && ip link set salc1.v99  up')

        # VLAN 130 – servers
        sSALc1.cmd('ovs-vsctl add-port sSALc1 salc1.v130 tag=130 -- set interface salc1.v130 type=internal')
        sSALc1.cmd('ip addr add 10.30.130.254/24 dev salc1.v130 && ip link set salc1.v130 up')

        # VLAN 20 – engineering
        sSALc1.cmd('ovs-vsctl add-port sSALc1 salc1.v20  tag=20  -- set interface salc1.v20  type=internal')
        sSALc1.cmd('ip addr add 10.30.20.1/25   dev salc1.v20  && ip link set salc1.v20  up')

        # VLAN 50 – reception
        sSALc1.cmd('ovs-vsctl add-port sSALc1 salc1.v50  tag=50  -- set interface salc1.v50  type=internal')
        sSALc1.cmd('ip addr add 10.30.50.1/27   dev salc1.v50  && ip link set salc1.v50  up')

        sSALc1.cmd('ip route add default via 10.30.99.1')

        # ── Core switch: port assignments ─────────────────────────────
        sSALc1.cmd('ovs-vsctl set port sSALc1-eth1 tag=99')         # uplink to gateway
        sSALc1.cmd('ovs-vsctl set port sSALc1-eth2 trunks=20,50')   # to sSALd1
        sSALc1.cmd('ovs-vsctl set port sSALc1-eth3 trunks=20,50')   # to sSALd2
        sSALc1.cmd('ovs-vsctl set port sSALc1-eth4 trunks=20,50')   # to sSALd3
        sSALc1.cmd('ovs-vsctl set port sSALc1-eth5 tag=130')        # to server

        # ── Distribution 1 – Floor 1 & Lobby ─────────────────────────
        sSALd1.cmd('ovs-vsctl set port sSALd1-eth1 trunks=20,50')   # uplink
        sSALd1.cmd('ovs-vsctl set port sSALd1-eth2 trunks=50')      # to sSALl1  (lobby-only)
        sSALd1.cmd('ovs-vsctl set port sSALd1-eth3 trunks=20,50')   # to sSALf11
        sSALd1.cmd('ovs-vsctl set port sSALd1-eth4 trunks=20,50')   # to sSALf12
        sSALd1.cmd('ovs-vsctl set port sSALd1-eth5 trunks=20,50')   # to sSALf13

        # ── Distribution 2 – Floor 2 ──────────────────────────────────
        sSALd2.cmd('ovs-vsctl set port sSALd2-eth1 trunks=20,50')   # uplink
        sSALd2.cmd('ovs-vsctl set port sSALd2-eth2 trunks=20,50')   # to sSALf21
        sSALd2.cmd('ovs-vsctl set port sSALd2-eth3 trunks=20,50')   # to sSALf22
        sSALd2.cmd('ovs-vsctl set port sSALd2-eth4 trunks=20,50')   # to sSALf23
        sSALd2.cmd('ovs-vsctl set port sSALd2-eth5 trunks=20,50')   # to sSALf24

        # ── Distribution 3 – Floor 3 ──────────────────────────────────
        sSALd3.cmd('ovs-vsctl set port sSALd3-eth1 trunks=20,50')   # uplink
        sSALd3.cmd('ovs-vsctl set port sSALd3-eth2 trunks=20,50')   # to sSALf31
        sSALd3.cmd('ovs-vsctl set port sSALd3-eth3 trunks=20,50')   # to sSALf32
        sSALd3.cmd('ovs-vsctl set port sSALd3-eth4 trunks=20,50')   # to sSALf33

        # ── Lobby switch ──────────────────────────────────────────────
        sSALl1.cmd('ovs-vsctl set port sSALl1-eth1 trunks=50')        # uplink
        sSALl1.cmd('ovs-vsctl set port sSALl1-eth2 tag=50')           # to hSALlrec1

        # ── Floor 1 access switches ───────────────────────────────────
        sSALf11.cmd('ovs-vsctl set port sSALf11-eth1 trunks=20,50') # uplink
        sSALf11.cmd('ovs-vsctl set port sSALf11-eth2 tag=20')       # to hSALf1eng1
        sSALf11.cmd('ovs-vsctl set port sSALf11-eth3 tag=50')       # to hSALf1rec1
        sSALf12.cmd('ovs-vsctl set port sSALf12-eth1 trunks=20,50') # uplink
        sSALf13.cmd('ovs-vsctl set port sSALf13-eth1 trunks=20,50') # uplink

        # ── Floor 2 access switches ───────────────────────────────────
        sSALf21.cmd('ovs-vsctl set port sSALf21-eth1 trunks=20,50') # uplink
        sSALf21.cmd('ovs-vsctl set port sSALf21-eth2 tag=20')       # to hSALf2eng1
        sSALf21.cmd('ovs-vsctl set port sSALf21-eth3 tag=50')       # to hSALf2rec1
        sSALf22.cmd('ovs-vsctl set port sSALf22-eth1 trunks=20,50') # uplink
        sSALf23.cmd('ovs-vsctl set port sSALf23-eth1 trunks=20,50') # uplink
        sSALf24.cmd('ovs-vsctl set port sSALf24-eth1 trunks=20,50') # uplink

        # ── Floor 3 access switches ───────────────────────────────────
        sSALf31.cmd('ovs-vsctl set port sSALf31-eth1 trunks=20,50') # uplink
        sSALf31.cmd('ovs-vsctl set port sSALf31-eth2 tag=20')       # to hSALf3eng1
        sSALf31.cmd('ovs-vsctl set port sSALf31-eth3 tag=50')       # to hSALf3rec1
        sSALf32.cmd('ovs-vsctl set port sSALf32-eth1 trunks=20,50') # uplink
        sSALf33.cmd('ovs-vsctl set port sSALf33-eth1 trunks=20,50') # uplink

        # ── Static host default routes ────────────────────────────────
        net.get('hSALf1eng1').setDefaultRoute('via 10.30.20.1')
        net.get('hSALf2eng1').setDefaultRoute('via 10.30.20.1')
        net.get('hSALf3eng1').setDefaultRoute('via 10.30.20.1')
        net.get('hSALf2rec1').setDefaultRoute('via 10.30.50.1')
        net.get('hSALf3rec1').setDefaultRoute('via 10.30.50.1')

        # ── Server host ───────────────────────────────────────────────
        hSALsrv1.setIP('10.30.130.1/24', intf='hSALsrv1-eth0')
        hSALsrv1.setDefaultRoute('via 10.30.130.254')

        # Point server's resolver at itself
        src_resolv = os.path.abspath('./saltillo/resolv.conf')
        hSALsrv1.cmd('umount /etc/resolv.conf 2>/dev/null; true')
        hSALsrv1.cmd('touch /etc/resolv.conf')
        hSALsrv1.cmd(f'mount --bind {src_resolv} /etc/resolv.conf')

        # DNS + DHCP (dnsmasq)
        hSALsrv1.cmd('dnsmasq -d --conf-file=./saltillo/site.conf --pid-file=/tmp/dnsmasq-sal.pid &')

        # Web server – serves saltillo/web/index.html on port 80
        web_root = os.path.abspath('./saltillo/web')
        hSALsrv1.cmd(f'python3 -m http.server 80 --directory {web_root} &')

        # ── DHCP relay on core switch ─────────────────────────────────
        # Listens on VLAN 20 and 50 SVIs, forwards requests to the server
        sSALc1.cmd('dhcrelay -4 -i salc1.v20 -i salc1.v50 10.30.130.1 &')

        CLI(net)

        # Cleanup
        hSALsrv1.cmd('kill $(cat /tmp/dnsmasq-sal.pid) 2>/dev/null')
        hSALsrv1.cmd('pkill -f "http.server" 2>/dev/null')
        sSALc1.cmd('pkill dhcrelay 2>/dev/null')
        net.stop()


def run():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink, autoSetMacs=True)
    site = Saltillo()
    site.build(net)
    net.start()
    site.config(net)

if __name__ == '__main__':
    setLogLevel('info')
    run()

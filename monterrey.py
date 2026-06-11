import os
SITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'monterrey')

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from base_nodes import SwitchL3, Router

# Monterrey site
#
# VLANs
#   10  Executives    10.20.10.0/27    gw 10.20.10.1
#   20  Engineering   10.20.20.0/23    gw 10.20.20.1
#   30  IoT Labs      10.20.30.0/26    gw 10.20.30.1
#   40  HR            10.20.40.0/27    gw 10.20.40.1
#   50  Reception     10.20.50.0/28    gw 10.20.50.1
#   60  Print Servers 10.20.60.0/28    gw 10.20.60.1
#   70  Meeting Rooms 10.20.70.0/26    gw 10.20.70.1
#   99  Uplink        10.20.99.0/30    p2p gateway ↔ core
#  100  Cameras       10.20.100.0/27   gw 10.20.100.1
#  110  Guests        10.20.110.0/26   gw 10.20.110.1
#  120  VoIP          10.20.120.0/24   gw 10.20.120.1
#  130  Servers       10.20.130.0/27   gw 10.20.130.1
#
# Inter-VLAN policy (enforced via iptables on sMTYc1):
#   Executives (10)  → all VLANs
#   Engineering (20) ↔ Engineering + IoT (30) + Servers (130)
#   IoT (30)         ↔ IoT + Engineering (20) + Servers (130)
#   HR (40)          ↔ HR + Executives (10) + Servers (130)
#   Reception (50)   ↔ Reception + VoIP (120) + Cameras (100) + Servers (130)
#   VoIP (120)       ↔ VoIP + Reception (50) + Servers (130)
#   Cameras (100)    ↔ Cameras + Reception (50) + Servers (130)
#   Guests (110)     → TCP/80 to Servers only (no ping, no other VLANs)
#   Print (60), Meeting (70): unrestricted (default ACCEPT)


class Monterrey:

    def __init__(self):
        self.gateway = None

    def build(self, net):
        self.gateway = net.addHost('monterrey', cls=Router)

        # Core switch (L3)
        sMTYc1 = net.addSwitch('sMTYc1', cls=SwitchL3, failMode='standalone')

        # Server switch and service hosts – VLAN 130 (10.20.130.0/27)
        sMTYs1    = net.addSwitch('sMTYs1', failMode='standalone')
        hMTYdns1  = net.addHost('hMTYdns1',  ip='10.20.130.2/27', defaultRoute='via 10.20.130.1')
        hMTYweb1  = net.addHost('hMTYweb1',  ip='10.20.130.3/27', defaultRoute='via 10.20.130.1')
        hMTYftp1  = net.addHost('hMTYftp1',  ip='10.20.130.4/27', defaultRoute='via 10.20.130.1')
        hMTYdhcp1 = net.addHost('hMTYdhcp1', ip='10.20.130.5/27', defaultRoute='via 10.20.130.1')

        net.addLink(hMTYdns1,  sMTYs1)   # sMTYs1-eth1
        net.addLink(hMTYweb1,  sMTYs1)   # sMTYs1-eth2
        net.addLink(hMTYftp1,  sMTYs1)   # sMTYs1-eth3
        net.addLink(hMTYdhcp1, sMTYs1)   # sMTYs1-eth4

        # Distribution switches (one per floor)
        sMTYd1 = net.addSwitch('sMTYd1', failMode='standalone')  # Lobby + Floor 1
        sMTYd2 = net.addSwitch('sMTYd2', failMode='standalone')  # Floor 2
        sMTYd3 = net.addSwitch('sMTYd3', failMode='standalone')  # Floor 3
        sMTYd4 = net.addSwitch('sMTYd4', failMode='standalone')  # Floor 4

        # Lobby access switch
        sMTYl1  = net.addSwitch('sMTYl1',  failMode='standalone')  # Reception + Guests

        # Floor 1 access switches
        sMTYf11 = net.addSwitch('sMTYf11', failMode='standalone')  # IoT + Print
        sMTYf12 = net.addSwitch('sMTYf12', failMode='standalone')  # Cameras + VoIP

        # Floor 2 access switches
        sMTYf21 = net.addSwitch('sMTYf21', failMode='standalone')  # Engineering
        sMTYf22 = net.addSwitch('sMTYf22', failMode='standalone')  # Meeting Rooms
        sMTYf23 = net.addSwitch('sMTYf23', failMode='standalone')  # Cameras + VoIP

        # Floor 3 access switches
        sMTYf31 = net.addSwitch('sMTYf31', failMode='standalone')  # Engineering + HR + Reception
        sMTYf32 = net.addSwitch('sMTYf32', failMode='standalone')  # Cameras + VoIP

        # Floor 4 access switches
        sMTYf41 = net.addSwitch('sMTYf41', failMode='standalone')  # Engineering + Executives
        sMTYf42 = net.addSwitch('sMTYf42', failMode='standalone')  # Cameras + VoIP

        # ── Switch links (order determines OVS port numbering) ────────
        net.addLink(self.gateway, sMTYc1)  # monterrey-eth0 ↔ sMTYc1-eth1
        net.addLink(sMTYc1, sMTYd1)       # sMTYc1-eth2    ↔ sMTYd1-eth1
        net.addLink(sMTYc1, sMTYd2)       # sMTYc1-eth3    ↔ sMTYd2-eth1
        net.addLink(sMTYc1, sMTYd3)       # sMTYc1-eth4    ↔ sMTYd3-eth1
        net.addLink(sMTYc1, sMTYd4)       # sMTYc1-eth5    ↔ sMTYd4-eth1
        net.addLink(sMTYc1, sMTYs1)       # sMTYc1-eth6    ↔ sMTYs1-eth5

        net.addLink(sMTYd1, sMTYl1)       # sMTYd1-eth2    ↔ sMTYl1-eth1
        net.addLink(sMTYd1, sMTYf11)      # sMTYd1-eth3    ↔ sMTYf11-eth1
        net.addLink(sMTYd1, sMTYf12)      # sMTYd1-eth4    ↔ sMTYf12-eth1

        net.addLink(sMTYd2, sMTYf21)      # sMTYd2-eth2    ↔ sMTYf21-eth1
        net.addLink(sMTYd2, sMTYf22)      # sMTYd2-eth3    ↔ sMTYf22-eth1
        net.addLink(sMTYd2, sMTYf23)      # sMTYd2-eth4    ↔ sMTYf23-eth1

        net.addLink(sMTYd3, sMTYf31)      # sMTYd3-eth2    ↔ sMTYf31-eth1
        net.addLink(sMTYd3, sMTYf32)      # sMTYd3-eth3    ↔ sMTYf32-eth1

        net.addLink(sMTYd4, sMTYf41)      # sMTYd4-eth2    ↔ sMTYf41-eth1
        net.addLink(sMTYd4, sMTYf42)      # sMTYd4-eth3    ↔ sMTYf42-eth1

        # ── Representative hosts ──────────────────────────────────────

        # Lobby – sMTYl1 (Reception + Guests)
        hMTYlrec1 = net.addHost('hMTYlrec1', ip='10.20.50.2/28')
        hMTYlgs1  = net.addHost('hMTYlgs1',  ip=None, privateDirs=['/etc'])  # DHCP client
        net.addLink(hMTYlrec1, sMTYl1)    # sMTYl1-eth2
        net.addLink(hMTYlgs1,  sMTYl1)    # sMTYl1-eth3

        # Floor 1 – sMTYf11 (IoT + Print)
        hMTYf1iot1 = net.addHost('hMTYf1iot1', ip='10.20.30.2/26')
        hMTYf1prt1 = net.addHost('hMTYf1prt1', ip='10.20.60.2/28')
        net.addLink(hMTYf1iot1, sMTYf11)  # sMTYf11-eth2
        net.addLink(hMTYf1prt1, sMTYf11)  # sMTYf11-eth3

        # Floor 1 – sMTYf12 (Cameras + VoIP)
        hMTYf1cam1  = net.addHost('hMTYf1cam1',  ip='10.20.100.2/27')
        hMTYf1voi1 = net.addHost('hMTYf1voi1', ip='10.20.120.2/24')
        net.addLink(hMTYf1cam1,  sMTYf12)  # sMTYf12-eth2
        net.addLink(hMTYf1voi1, sMTYf12)  # sMTYf12-eth3

        # Floor 2 – sMTYf21 (Engineering)
        hMTYf2eng1 = net.addHost('hMTYf2eng1', ip='10.20.20.10/23')
        net.addLink(hMTYf2eng1, sMTYf21)  # sMTYf21-eth2

        # Floor 2 – sMTYf22 (Meeting Rooms)
        hMTYf2mr1 = net.addHost('hMTYf2mr1', ip='10.20.70.2/26')
        net.addLink(hMTYf2mr1, sMTYf22)  # sMTYf22-eth2

        # Floor 2 – sMTYf23 (Cameras + VoIP)
        hMTYf2cam1  = net.addHost('hMTYf2cam1',  ip='10.20.100.3/27')
        hMTYf2voi1 = net.addHost('hMTYf2voi1', ip='10.20.120.3/24')
        net.addLink(hMTYf2cam1,  sMTYf23)  # sMTYf23-eth2
        net.addLink(hMTYf2voi1, sMTYf23)  # sMTYf23-eth3

        # Floor 3 – sMTYf31 (Engineering + HR + Reception)
        hMTYf3eng1 = net.addHost('hMTYf3eng1', ip='10.20.20.20/23')
        hMTYf3hr1  = net.addHost('hMTYf3hr1',  ip='10.20.40.2/27')
        hMTYf3rec1 = net.addHost('hMTYf3rec1', ip='10.20.50.3/28')
        net.addLink(hMTYf3eng1, sMTYf31)  # sMTYf31-eth2
        net.addLink(hMTYf3hr1,  sMTYf31)  # sMTYf31-eth3
        net.addLink(hMTYf3rec1, sMTYf31)  # sMTYf31-eth4

        # Floor 3 – sMTYf32 (Cameras + VoIP)
        hMTYf3cam1  = net.addHost('hMTYf3cam1',  ip='10.20.100.4/27')
        hMTYf3voi1 = net.addHost('hMTYf3voi1', ip='10.20.120.4/24')
        net.addLink(hMTYf3cam1,  sMTYf32)  # sMTYf32-eth2
        net.addLink(hMTYf3voi1, sMTYf32)  # sMTYf32-eth3

        # Floor 4 – sMTYf41 (Engineering + Executives)
        hMTYf4eng1 = net.addHost('hMTYf4eng1', ip='10.20.20.30/23')
        hMTYf4exe1 = net.addHost('hMTYf4exe1', ip='10.20.10.2/27')
        net.addLink(hMTYf4eng1, sMTYf41)  # sMTYf41-eth2
        net.addLink(hMTYf4exe1, sMTYf41)  # sMTYf41-eth3

        # Floor 4 – sMTYf42 (Cameras + VoIP)
        hMTYf4cam1  = net.addHost('hMTYf4cam1',  ip='10.20.100.5/27')
        hMTYf4voi1 = net.addHost('hMTYf4voi1', ip='10.20.120.5/24')
        net.addLink(hMTYf4cam1,  sMTYf42)  # sMTYf42-eth2
        net.addLink(hMTYf4voi1, sMTYf42)  # sMTYf42-eth3

        print("Monterrey site built successfully!")

    def config(self, net):
        sMTYc1  = net.get('sMTYc1')
        sMTYd1  = net.get('sMTYd1')
        sMTYd2  = net.get('sMTYd2')
        sMTYd3  = net.get('sMTYd3')
        sMTYd4  = net.get('sMTYd4')
        sMTYl1  = net.get('sMTYl1')
        sMTYf11 = net.get('sMTYf11')
        sMTYf12 = net.get('sMTYf12')
        sMTYf21 = net.get('sMTYf21')
        sMTYf22 = net.get('sMTYf22')
        sMTYf23 = net.get('sMTYf23')
        sMTYf31 = net.get('sMTYf31')
        sMTYf32 = net.get('sMTYf32')
        sMTYf41 = net.get('sMTYf41')
        sMTYf42 = net.get('sMTYf42')
        hMTYdhcp1 = net.get('hMTYdhcp1')
        hMTYweb1  = net.get('hMTYweb1')
        hMTYftp1  = net.get('hMTYftp1')
        hMTYlgs1  = net.get('hMTYlgs1')

        # Fix: privateDirs=['/etc'] creates isolated /etc without fstab
        hMTYlgs1.cmd('touch /etc/fstab')

        # ── Gateway ───────────────────────────────────────────────────
        self.gateway.setIP('10.20.99.1/30', intf='monterrey-eth0')
        self.gateway.cmd('ip route add 10.20.0.0/16 via 10.20.99.2')

        # ── Core switch: SVIs ─────────────────────────────────────────
        def add_svi(vlan, ip_cidr):
            name = f'mtyc1.v{vlan}'
            sMTYc1.cmd(f'ovs-vsctl add-port sMTYc1 {name} tag={vlan} -- set interface {name} type=internal')
            sMTYc1.cmd(f'ip addr add {ip_cidr} dev {name} && ip link set {name} up')

        add_svi(10,  '10.20.10.1/27')
        add_svi(20,  '10.20.20.1/23')
        add_svi(30,  '10.20.30.1/26')
        add_svi(40,  '10.20.40.1/27')
        add_svi(50,  '10.20.50.1/28')
        add_svi(60,  '10.20.60.1/28')
        add_svi(70,  '10.20.70.1/26')
        add_svi(99,  '10.20.99.2/30')
        add_svi(100, '10.20.100.1/27')
        add_svi(110, '10.20.110.1/26')
        add_svi(120, '10.20.120.1/24')
        add_svi(130, '10.20.130.1/27')

        sMTYc1.cmd('ip route add default via 10.20.99.1')

        # ── Core switch: port assignments ─────────────────────────────
        sMTYc1.cmd('ovs-vsctl set port sMTYc1-eth1 tag=99')                          # gateway
        sMTYc1.cmd('ovs-vsctl set port sMTYc1-eth2 trunks=30,50,60,100,110,120')     # to sMTYd1
        sMTYc1.cmd('ovs-vsctl set port sMTYc1-eth3 trunks=20,70,100,120')            # to sMTYd2
        sMTYc1.cmd('ovs-vsctl set port sMTYc1-eth4 trunks=20,40,50,100,120')         # to sMTYd3
        sMTYc1.cmd('ovs-vsctl set port sMTYc1-eth5 trunks=10,20,100,120')            # to sMTYd4
        sMTYc1.cmd('ovs-vsctl set port sMTYc1-eth6 tag=130')                          # to sMTYs1

        # ── Distribution 1 – Lobby + Floor 1 ─────────────────────────
        sMTYd1.cmd('ovs-vsctl set port sMTYd1-eth1 trunks=30,50,60,100,110,120')  # uplink
        sMTYd1.cmd('ovs-vsctl set port sMTYd1-eth2 trunks=50,110')                # to sMTYl1
        sMTYd1.cmd('ovs-vsctl set port sMTYd1-eth3 trunks=30,60')                 # to sMTYf11
        sMTYd1.cmd('ovs-vsctl set port sMTYd1-eth4 trunks=100,120')               # to sMTYf12

        # ── Distribution 2 – Floor 2 ──────────────────────────────────
        sMTYd2.cmd('ovs-vsctl set port sMTYd2-eth1 trunks=20,70,100,120')  # uplink
        sMTYd2.cmd('ovs-vsctl set port sMTYd2-eth2 trunks=20')             # to sMTYf21
        sMTYd2.cmd('ovs-vsctl set port sMTYd2-eth3 trunks=70')             # to sMTYf22
        sMTYd2.cmd('ovs-vsctl set port sMTYd2-eth4 trunks=100,120')        # to sMTYf23

        # ── Distribution 3 – Floor 3 ──────────────────────────────────
        sMTYd3.cmd('ovs-vsctl set port sMTYd3-eth1 trunks=20,40,50,100,120')  # uplink
        sMTYd3.cmd('ovs-vsctl set port sMTYd3-eth2 trunks=20,40,50')          # to sMTYf31
        sMTYd3.cmd('ovs-vsctl set port sMTYd3-eth3 trunks=100,120')            # to sMTYf32

        # ── Distribution 4 – Floor 4 ──────────────────────────────────
        sMTYd4.cmd('ovs-vsctl set port sMTYd4-eth1 trunks=10,20,100,120')  # uplink
        sMTYd4.cmd('ovs-vsctl set port sMTYd4-eth2 trunks=10,20')          # to sMTYf41
        sMTYd4.cmd('ovs-vsctl set port sMTYd4-eth3 trunks=100,120')        # to sMTYf42

        # ── Lobby ─────────────────────────────────────────────────────
        sMTYl1.cmd('ovs-vsctl set port sMTYl1-eth1 trunks=50,110')
        sMTYl1.cmd('ovs-vsctl set port sMTYl1-eth2 tag=50')    # hMTYlrec1
        sMTYl1.cmd('ovs-vsctl set port sMTYl1-eth3 tag=110')   # hMTYlgs1

        # ── Floor 1 ───────────────────────────────────────────────────
        sMTYf11.cmd('ovs-vsctl set port sMTYf11-eth1 trunks=30,60')
        sMTYf11.cmd('ovs-vsctl set port sMTYf11-eth2 tag=30')  # hMTYf1iot1
        sMTYf11.cmd('ovs-vsctl set port sMTYf11-eth3 tag=60')  # hMTYf1prt1

        sMTYf12.cmd('ovs-vsctl set port sMTYf12-eth1 trunks=100,120')
        sMTYf12.cmd('ovs-vsctl set port sMTYf12-eth2 tag=100') # hMTYf1cam1
        sMTYf12.cmd('ovs-vsctl set port sMTYf12-eth3 tag=120') # hMTYf1voi1

        # ── Floor 2 ───────────────────────────────────────────────────
        sMTYf21.cmd('ovs-vsctl set port sMTYf21-eth1 trunks=20')
        sMTYf21.cmd('ovs-vsctl set port sMTYf21-eth2 tag=20')  # hMTYf2eng1

        sMTYf22.cmd('ovs-vsctl set port sMTYf22-eth1 trunks=70')
        sMTYf22.cmd('ovs-vsctl set port sMTYf22-eth2 tag=70')  # hMTYf2mr1

        sMTYf23.cmd('ovs-vsctl set port sMTYf23-eth1 trunks=100,120')
        sMTYf23.cmd('ovs-vsctl set port sMTYf23-eth2 tag=100') # hMTYf2cam1
        sMTYf23.cmd('ovs-vsctl set port sMTYf23-eth3 tag=120') # hMTYf2voi1

        # ── Floor 3 ───────────────────────────────────────────────────
        sMTYf31.cmd('ovs-vsctl set port sMTYf31-eth1 trunks=20,40,50')
        sMTYf31.cmd('ovs-vsctl set port sMTYf31-eth2 tag=20')  # hMTYf3eng1
        sMTYf31.cmd('ovs-vsctl set port sMTYf31-eth3 tag=40')  # hMTYf3hr1
        sMTYf31.cmd('ovs-vsctl set port sMTYf31-eth4 tag=50')  # hMTYf3rec1

        sMTYf32.cmd('ovs-vsctl set port sMTYf32-eth1 trunks=100,120')
        sMTYf32.cmd('ovs-vsctl set port sMTYf32-eth2 tag=100') # hMTYf3cam1
        sMTYf32.cmd('ovs-vsctl set port sMTYf32-eth3 tag=120') # hMTYf3voi1

        # ── Floor 4 ───────────────────────────────────────────────────
        sMTYf41.cmd('ovs-vsctl set port sMTYf41-eth1 trunks=10,20')
        sMTYf41.cmd('ovs-vsctl set port sMTYf41-eth2 tag=20')  # hMTYf4eng1
        sMTYf41.cmd('ovs-vsctl set port sMTYf41-eth3 tag=10')  # hMTYf4exe1

        sMTYf42.cmd('ovs-vsctl set port sMTYf42-eth1 trunks=100,120')
        sMTYf42.cmd('ovs-vsctl set port sMTYf42-eth2 tag=100') # hMTYf4cam1
        sMTYf42.cmd('ovs-vsctl set port sMTYf42-eth3 tag=120') # hMTYf4voi1

        # ── Static host default routes ────────────────────────────────
        net.get('hMTYlrec1').setDefaultRoute('via 10.20.50.1')
        net.get('hMTYf1iot1').setDefaultRoute('via 10.20.30.1')
        net.get('hMTYf1prt1').setDefaultRoute('via 10.20.60.1')
        net.get('hMTYf1cam1').setDefaultRoute('via 10.20.100.1')
        net.get('hMTYf1voi1').setDefaultRoute('via 10.20.120.1')
        net.get('hMTYf2eng1').setDefaultRoute('via 10.20.20.1')
        net.get('hMTYf2mr1').setDefaultRoute('via 10.20.70.1')
        net.get('hMTYf2cam1').setDefaultRoute('via 10.20.100.1')
        net.get('hMTYf2voi1').setDefaultRoute('via 10.20.120.1')
        net.get('hMTYf3eng1').setDefaultRoute('via 10.20.20.1')
        net.get('hMTYf3hr1').setDefaultRoute('via 10.20.40.1')
        net.get('hMTYf3rec1').setDefaultRoute('via 10.20.50.1')
        net.get('hMTYf3cam1').setDefaultRoute('via 10.20.100.1')
        net.get('hMTYf3voi1').setDefaultRoute('via 10.20.120.1')
        net.get('hMTYf4eng1').setDefaultRoute('via 10.20.20.1')
        net.get('hMTYf4exe1').setDefaultRoute('via 10.20.10.1')
        net.get('hMTYf4cam1').setDefaultRoute('via 10.20.100.1')
        net.get('hMTYf4voi1').setDefaultRoute('via 10.20.120.1')

        # ── Services ──────────────────────────────────────────────────
        hMTYdhcp1.cmd(f'rm -f {SITE_DIR}/MTY_dhcp.pid {SITE_DIR}/MTY_dhcp.leases {SITE_DIR}/MTY_dhcp.log')
        hMTYdhcp1.cmd(f'dnsmasq --conf-file={SITE_DIR}/MTY_dhcp.conf --addn-hosts={SITE_DIR}/records.txt --pid-file={SITE_DIR}/MTY_dhcp.pid --dhcp-leasefile={SITE_DIR}/MTY_dhcp.leases --log-dhcp --log-facility={SITE_DIR}/MTY_dhcp.log &')
        sMTYc1.cmd('pkill dhcrelay 2>/dev/null')
        sMTYc1.cmd('dhcrelay -4 -i mtyc1.v50 -i mtyc1.v110 10.20.130.5 &')

        hMTYweb1.cmd(f'python3 -m http.server 80 --directory {SITE_DIR}/web &')
        hMTYftp1.cmd(f'cd {SITE_DIR}/ftp && python3 -m pyftpdlib -p 21 -w -u admin -P secret123 &')

        sMTYc1.cmd(f'sed -i "/agco.monterrey/d" /etc/hosts && cat {SITE_DIR}/records.txt >> /etc/hosts')

        # ── Inter-VLAN access policy (iptables on sMTYc1) ─────────────
        c = sMTYc1.cmd
        c('iptables -N MTY_FWD 2>/dev/null; iptables -F MTY_FWD')
        c('iptables -C FORWARD -j MTY_FWD 2>/dev/null || iptables -A FORWARD -j MTY_FWD')

        c('iptables -A MTY_FWD -m state --state ESTABLISHED,RELATED -j ACCEPT')

        # Executives (10): no restriction — default ACCEPT covers them

        # Engineering (20): ↔ Engineering + IoT + Servers only
        c('iptables -A MTY_FWD -s 10.20.20.0/23 -d 10.20.20.0/23  -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.20.0/23 -d 10.20.30.0/26  -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.20.0/23 -d 10.20.130.0/27 -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.20.0/23 -d 10.10.20.0/23  -j ACCEPT')  # → Illinois Eng
        c('iptables -A MTY_FWD -s 10.20.20.0/23 -d 10.30.20.0/25  -j ACCEPT')  # → Saltillo Eng
        c('iptables -A MTY_FWD -s 10.20.20.0/23 -j REJECT --reject-with icmp-net-prohibited')

        # IoT (30): ↔ IoT + Engineering + Servers only
        c('iptables -A MTY_FWD -s 10.20.30.0/26 -d 10.20.30.0/26  -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.30.0/26 -d 10.20.20.0/23  -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.30.0/26 -d 10.20.130.0/27 -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.30.0/26 -d 10.10.20.0/23  -j ACCEPT')  # → Illinois Eng (remote lab access)
        c('iptables -A MTY_FWD -s 10.20.30.0/26 -j REJECT --reject-with icmp-net-prohibited')

        # HR (40): ↔ HR + Executives + Servers only
        c('iptables -A MTY_FWD -s 10.20.40.0/27 -d 10.20.40.0/27  -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.40.0/27 -d 10.20.10.0/27  -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.40.0/27 -d 10.20.130.0/27 -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.40.0/27 -j REJECT --reject-with icmp-net-prohibited')

        # Reception (50): ↔ Reception + VoIP + Cameras + Servers only
        c('iptables -A MTY_FWD -s 10.20.50.0/28 -d 10.20.50.0/28  -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.50.0/28 -d 10.20.120.0/24 -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.50.0/28 -d 10.20.100.0/27 -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.50.0/28 -d 10.20.130.0/27 -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.50.0/28 -j REJECT --reject-with icmp-net-prohibited')

        # Cameras (100): symmetric with Reception
        c('iptables -A MTY_FWD -s 10.20.100.0/27 -d 10.20.100.0/27 -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.100.0/27 -d 10.20.50.0/28  -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.100.0/27 -d 10.20.130.0/27 -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.100.0/27 -j REJECT --reject-with icmp-net-prohibited')

        # VoIP (120): symmetric with Reception
        c('iptables -A MTY_FWD -s 10.20.120.0/24 -d 10.20.120.0/24 -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.120.0/24 -d 10.20.50.0/28  -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.120.0/24 -d 10.20.130.0/27 -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.120.0/24 -j REJECT --reject-with icmp-net-prohibited')

        # Guests (110): TCP/80 to servers only — DROP (no ICMP response, fully dark)
        c('iptables -A MTY_FWD -s 10.20.110.0/26 -d 10.20.130.0/27 -p tcp --dport 80 -j ACCEPT')
        c('iptables -A MTY_FWD -s 10.20.110.0/26 -j DROP')


def run():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink, autoSetMacs=True)
    site = Monterrey()
    site.build(net)
    net.start()
    site.config(net)
    CLI(net)
    net.get('sMTYc1').cmd('pkill dhcrelay 2>/dev/null')
    net.get('sMTYc1').cmd('sed -i "/agco.monterrey/d" /etc/hosts')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()

import os
SITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'texas')

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from base_nodes import SwitchL3, Router

# Texas site
#
# VLANs
#   10  Executives    10.40.10.0/27    gw 10.40.10.1
#   20  Engineering   10.40.20.0/25    gw 10.40.20.1
#   30  Labs          10.40.30.0/25    gw 10.40.30.1
#   40  HR            10.40.40.0/27    gw 10.40.40.1
#   50  Reception     10.40.50.0/28    gw 10.40.50.1
#   60  Print Servers 10.40.60.0/28    gw 10.40.60.1
#   70  Meeting Rooms 10.40.70.0/27    gw 10.40.70.1
#   99  Uplink        10.40.99.0/30    p2p gateway ↔ core
#  100  Cameras       10.40.100.0/26   gw 10.40.100.1
#  110  Guests        10.40.110.0/28   gw 10.40.110.1
#  120  VoIP          10.40.120.0/26   gw 10.40.120.1
#  130  Servers       10.40.130.0/26   gw 10.40.130.1
#
# Inter-VLAN policy (enforced via iptables on sTEXc1):
#   Executives (10)  → all VLANs
#   Engineering (20) ↔ Engineering + Labs (30) + Servers (130)
#   Labs (30)        ↔ Labs + Engineering (20) + Servers (130)
#   HR (40)          ↔ HR + Executives (10) + Servers (130)
#   Reception (50)   ↔ Reception + VoIP (120) + Cameras (100) + Servers (130)
#   VoIP (120)       ↔ VoIP + Reception (50) + Servers (130)
#   Cameras (100)    ↔ Cameras + Reception (50) + Servers (130)
#   Guests (110)     → TCP/80 to Servers only (no ping, no other VLANs)
#   Print (60), Meeting (70): unrestricted (default ACCEPT)


class Texas:

    def __init__(self):
        self.gateway = None

    def build(self, net):
        self.gateway = net.addHost('texas', cls=Router)

        # Core switch (L3)
        sTEXc1 = net.addSwitch('sTEXc1', cls=SwitchL3, failMode='standalone')

        # Server switch and service hosts – VLAN 130 (10.40.130.0/26)
        sTEXs1    = net.addSwitch('sTEXs1', failMode='standalone')
        hTEXdns1  = net.addHost('hTEXdns1',  ip='10.40.130.10/26', defaultRoute='via 10.40.130.1')
        hTEXweb1  = net.addHost('hTEXweb1',  ip='10.40.130.20/26', defaultRoute='via 10.40.130.1')
        hTEXftp1  = net.addHost('hTEXftp1',  ip='10.40.130.30/26', defaultRoute='via 10.40.130.1')
        hTEXdhcp1 = net.addHost('hTEXdhcp1', ip='10.40.130.40/26', defaultRoute='via 10.40.130.1')

        net.addLink(hTEXdns1,  sTEXs1)   # sTEXs1-eth1
        net.addLink(hTEXweb1,  sTEXs1)   # sTEXs1-eth2
        net.addLink(hTEXftp1,  sTEXs1)   # sTEXs1-eth3
        net.addLink(hTEXdhcp1, sTEXs1)   # sTEXs1-eth4

        # Distribution switches (one per floor)
        sTEXd1 = net.addSwitch('sTEXd1', failMode='standalone')  # Floor 1
        sTEXd2 = net.addSwitch('sTEXd2', failMode='standalone')  # Floor 2
        sTEXd3 = net.addSwitch('sTEXd3', failMode='standalone')  # Floor 3
        sTEXd4 = net.addSwitch('sTEXd4', failMode='standalone')  # Floor 4
        sTEXd5 = net.addSwitch('sTEXd5', failMode='standalone')  # Floor 5

        # Floor 1 access switches
        sTEXf11 = net.addSwitch('sTEXf11', failMode='standalone')  # Reception + Guests
        sTEXf12 = net.addSwitch('sTEXf12', failMode='standalone')  # Cameras

        # Floor 2 access switches
        sTEXf21 = net.addSwitch('sTEXf21', failMode='standalone')  # Labs
        sTEXf22 = net.addSwitch('sTEXf22', failMode='standalone')  # Cameras + VoIP

        # Floor 3 access switches
        sTEXf31 = net.addSwitch('sTEXf31', failMode='standalone')  # Engineering
        sTEXf32 = net.addSwitch('sTEXf32', failMode='standalone')  # Cameras + VoIP

        # Floor 4 access switches
        sTEXf41 = net.addSwitch('sTEXf41', failMode='standalone')  # Meeting + Engineering
        sTEXf42 = net.addSwitch('sTEXf42', failMode='standalone')  # Cameras + VoIP

        # Floor 5 access switches
        sTEXf51 = net.addSwitch('sTEXf51', failMode='standalone')  # Exec + HR + Meeting + Print
        sTEXf52 = net.addSwitch('sTEXf52', failMode='standalone')  # Cameras + VoIP

        # ── Switch links (order determines OVS port numbering) ────────
        net.addLink(self.gateway, sTEXc1)  # texas-eth0     ↔ sTEXc1-eth1
        net.addLink(sTEXc1, sTEXd1)       # sTEXc1-eth2    ↔ sTEXd1-eth1
        net.addLink(sTEXc1, sTEXd2)       # sTEXc1-eth3    ↔ sTEXd2-eth1
        net.addLink(sTEXc1, sTEXd3)       # sTEXc1-eth4    ↔ sTEXd3-eth1
        net.addLink(sTEXc1, sTEXd4)       # sTEXc1-eth5    ↔ sTEXd4-eth1
        net.addLink(sTEXc1, sTEXd5)       # sTEXc1-eth6    ↔ sTEXd5-eth1
        net.addLink(sTEXc1, sTEXs1)       # sTEXc1-eth7    ↔ sTEXs1-eth5

        net.addLink(sTEXd1, sTEXf11)      # sTEXd1-eth2    ↔ sTEXf11-eth1
        net.addLink(sTEXd1, sTEXf12)      # sTEXd1-eth3    ↔ sTEXf12-eth1

        net.addLink(sTEXd2, sTEXf21)      # sTEXd2-eth2    ↔ sTEXf21-eth1
        net.addLink(sTEXd2, sTEXf22)      # sTEXd2-eth3    ↔ sTEXf22-eth1

        net.addLink(sTEXd3, sTEXf31)      # sTEXd3-eth2    ↔ sTEXf31-eth1
        net.addLink(sTEXd3, sTEXf32)      # sTEXd3-eth3    ↔ sTEXf32-eth1

        net.addLink(sTEXd4, sTEXf41)      # sTEXd4-eth2    ↔ sTEXf41-eth1
        net.addLink(sTEXd4, sTEXf42)      # sTEXd4-eth3    ↔ sTEXf42-eth1

        net.addLink(sTEXd5, sTEXf51)      # sTEXd5-eth2    ↔ sTEXf51-eth1
        net.addLink(sTEXd5, sTEXf52)      # sTEXd5-eth3    ↔ sTEXf52-eth1

        # ── Representative hosts ──────────────────────────────────────

        # Floor 1 – sTEXf11 (Reception + Guests)
        hTEXf1rec1 = net.addHost('hTEXf1rec1', ip='10.40.50.2/28')
        hTEXf1gs1  = net.addHost('hTEXf1gs1',  ip=None, privateDirs=['/etc'])  # DHCP client
        net.addLink(hTEXf1rec1, sTEXf11)  # sTEXf11-eth2
        net.addLink(hTEXf1gs1,  sTEXf11)  # sTEXf11-eth3

        # Floor 1 – sTEXf12 (Cameras)
        hTEXf1cam1 = net.addHost('hTEXf1cam1', ip='10.40.100.2/26')
        net.addLink(hTEXf1cam1, sTEXf12)  # sTEXf12-eth2

        # Floor 2 – sTEXf21 (Labs)
        hTEXf2lab1 = net.addHost('hTEXf2lab1', ip='10.40.30.2/25')
        net.addLink(hTEXf2lab1, sTEXf21)  # sTEXf21-eth2

        # Floor 2 – sTEXf22 (Cameras + VoIP)
        hTEXf2cam1  = net.addHost('hTEXf2cam1',  ip='10.40.100.3/26')
        hTEXf2voi1 = net.addHost('hTEXf2voi1', ip='10.40.120.2/26')
        net.addLink(hTEXf2cam1,  sTEXf22)  # sTEXf22-eth2
        net.addLink(hTEXf2voi1, sTEXf22)  # sTEXf22-eth3

        # Floor 3 – sTEXf31 (Engineering)
        hTEXf3eng1 = net.addHost('hTEXf3eng1', ip='10.40.20.2/25')
        net.addLink(hTEXf3eng1, sTEXf31)  # sTEXf31-eth2

        # Floor 3 – sTEXf32 (Cameras + VoIP)
        hTEXf3cam1  = net.addHost('hTEXf3cam1',  ip='10.40.100.4/26')
        hTEXf3voi1 = net.addHost('hTEXf3voi1', ip='10.40.120.3/26')
        net.addLink(hTEXf3cam1,  sTEXf32)  # sTEXf32-eth2
        net.addLink(hTEXf3voi1, sTEXf32)  # sTEXf32-eth3

        # Floor 4 – sTEXf41 (Meeting + Engineering)
        hTEXf4mr1 = net.addHost('hTEXf4mr1', ip='10.40.70.2/27')
        hTEXf4eng1  = net.addHost('hTEXf4eng1',  ip='10.40.20.3/25')
        net.addLink(hTEXf4mr1, sTEXf41)  # sTEXf41-eth2
        net.addLink(hTEXf4eng1,  sTEXf41)  # sTEXf41-eth3

        # Floor 4 – sTEXf42 (Cameras + VoIP)
        hTEXf4cam1  = net.addHost('hTEXf4cam1',  ip='10.40.100.5/26')
        hTEXf4voi1 = net.addHost('hTEXf4voi1', ip='10.40.120.4/26')
        net.addLink(hTEXf4cam1,  sTEXf42)  # sTEXf42-eth2
        net.addLink(hTEXf4voi1, sTEXf42)  # sTEXf42-eth3

        # Floor 5 – sTEXf51 (Exec + HR + Meeting + Print)
        hTEXf5exe1  = net.addHost('hTEXf5exe1',  ip='10.40.10.2/27')
        hTEXf5hr1   = net.addHost('hTEXf5hr1',   ip='10.40.40.2/27')
        hTEXf5mr1 = net.addHost('hTEXf5mr1', ip='10.40.70.3/27')
        hTEXf5prt1  = net.addHost('hTEXf5prt1',  ip='10.40.60.2/28')
        net.addLink(hTEXf5exe1,  sTEXf51)  # sTEXf51-eth2
        net.addLink(hTEXf5hr1,   sTEXf51)  # sTEXf51-eth3
        net.addLink(hTEXf5mr1, sTEXf51)  # sTEXf51-eth4
        net.addLink(hTEXf5prt1,  sTEXf51)  # sTEXf51-eth5

        # Floor 5 – sTEXf52 (Cameras + VoIP)
        hTEXf5cam1  = net.addHost('hTEXf5cam1',  ip='10.40.100.6/26')
        hTEXf5voi1 = net.addHost('hTEXf5voi1', ip='10.40.120.5/26')
        net.addLink(hTEXf5cam1,  sTEXf52)  # sTEXf52-eth2
        net.addLink(hTEXf5voi1, sTEXf52)  # sTEXf52-eth3

        print("Texas site built successfully!")

    def config(self, net):
        sTEXc1  = net.get('sTEXc1')
        sTEXd1  = net.get('sTEXd1')
        sTEXd2  = net.get('sTEXd2')
        sTEXd3  = net.get('sTEXd3')
        sTEXd4  = net.get('sTEXd4')
        sTEXd5  = net.get('sTEXd5')
        sTEXf11 = net.get('sTEXf11')
        sTEXf12 = net.get('sTEXf12')
        sTEXf21 = net.get('sTEXf21')
        sTEXf22 = net.get('sTEXf22')
        sTEXf31 = net.get('sTEXf31')
        sTEXf32 = net.get('sTEXf32')
        sTEXf41 = net.get('sTEXf41')
        sTEXf42 = net.get('sTEXf42')
        sTEXf51 = net.get('sTEXf51')
        sTEXf52 = net.get('sTEXf52')
        hTEXdhcp1 = net.get('hTEXdhcp1')
        hTEXweb1  = net.get('hTEXweb1')
        hTEXftp1  = net.get('hTEXftp1')
        hTEXf1gs1 = net.get('hTEXf1gs1')

        # Fix: privateDirs=['/etc'] creates isolated /etc without fstab
        hTEXf1gs1.cmd('touch /etc/fstab')

        # ── Gateway ───────────────────────────────────────────────────
        self.gateway.setIP('10.40.99.1/30', intf='texas-eth0')
        self.gateway.cmd('ip route add 10.40.0.0/16 via 10.40.99.2')

        # ── Core switch: SVIs ─────────────────────────────────────────
        def add_svi(vlan, ip_cidr):
            name = f'texc1.v{vlan}'
            sTEXc1.cmd(f'ovs-vsctl add-port sTEXc1 {name} tag={vlan} -- set interface {name} type=internal')
            sTEXc1.cmd(f'ip addr add {ip_cidr} dev {name} && ip link set {name} up')

        add_svi(10,  '10.40.10.1/27')
        add_svi(20,  '10.40.20.1/25')
        add_svi(30,  '10.40.30.1/25')
        add_svi(40,  '10.40.40.1/27')
        add_svi(50,  '10.40.50.1/28')
        add_svi(60,  '10.40.60.1/28')
        add_svi(70,  '10.40.70.1/27')
        add_svi(99,  '10.40.99.2/30')
        add_svi(100, '10.40.100.1/26')
        add_svi(110, '10.40.110.1/28')
        add_svi(120, '10.40.120.1/26')
        add_svi(130, '10.40.130.1/26')

        sTEXc1.cmd('ip route add default via 10.40.99.1')

        # ── Core switch: port assignments ─────────────────────────────
        sTEXc1.cmd('ovs-vsctl set port sTEXc1-eth1 tag=99')                          # gateway
        sTEXc1.cmd('ovs-vsctl set port sTEXc1-eth2 trunks=50,100,110')               # to sTEXd1
        sTEXc1.cmd('ovs-vsctl set port sTEXc1-eth3 trunks=30,100,120')               # to sTEXd2
        sTEXc1.cmd('ovs-vsctl set port sTEXc1-eth4 trunks=20,100,120')               # to sTEXd3
        sTEXc1.cmd('ovs-vsctl set port sTEXc1-eth5 trunks=20,70,100,120')            # to sTEXd4
        sTEXc1.cmd('ovs-vsctl set port sTEXc1-eth6 trunks=10,40,60,70,100,120')      # to sTEXd5
        sTEXc1.cmd('ovs-vsctl set port sTEXc1-eth7 tag=130')                          # to sTEXs1

        # ── Distribution 1 – Floor 1 ──────────────────────────────────
        sTEXd1.cmd('ovs-vsctl set port sTEXd1-eth1 trunks=50,100,110')  # uplink
        sTEXd1.cmd('ovs-vsctl set port sTEXd1-eth2 trunks=50,110')      # to sTEXf11
        sTEXd1.cmd('ovs-vsctl set port sTEXd1-eth3 trunks=100')         # to sTEXf12

        # ── Distribution 2 – Floor 2 ──────────────────────────────────
        sTEXd2.cmd('ovs-vsctl set port sTEXd2-eth1 trunks=30,100,120')  # uplink
        sTEXd2.cmd('ovs-vsctl set port sTEXd2-eth2 trunks=30')          # to sTEXf21
        sTEXd2.cmd('ovs-vsctl set port sTEXd2-eth3 trunks=100,120')     # to sTEXf22

        # ── Distribution 3 – Floor 3 ──────────────────────────────────
        sTEXd3.cmd('ovs-vsctl set port sTEXd3-eth1 trunks=20,100,120')  # uplink
        sTEXd3.cmd('ovs-vsctl set port sTEXd3-eth2 trunks=20')          # to sTEXf31
        sTEXd3.cmd('ovs-vsctl set port sTEXd3-eth3 trunks=100,120')     # to sTEXf32

        # ── Distribution 4 – Floor 4 ──────────────────────────────────
        sTEXd4.cmd('ovs-vsctl set port sTEXd4-eth1 trunks=20,70,100,120')  # uplink
        sTEXd4.cmd('ovs-vsctl set port sTEXd4-eth2 trunks=20,70')          # to sTEXf41
        sTEXd4.cmd('ovs-vsctl set port sTEXd4-eth3 trunks=100,120')        # to sTEXf42

        # ── Distribution 5 – Floor 5 ──────────────────────────────────
        sTEXd5.cmd('ovs-vsctl set port sTEXd5-eth1 trunks=10,40,60,70,100,120')  # uplink
        sTEXd5.cmd('ovs-vsctl set port sTEXd5-eth2 trunks=10,40,60,70')           # to sTEXf51
        sTEXd5.cmd('ovs-vsctl set port sTEXd5-eth3 trunks=100,120')               # to sTEXf52

        # ── Floor 1 ───────────────────────────────────────────────────
        sTEXf11.cmd('ovs-vsctl set port sTEXf11-eth1 trunks=50,110')
        sTEXf11.cmd('ovs-vsctl set port sTEXf11-eth2 tag=50')   # hTEXf1rec1
        sTEXf11.cmd('ovs-vsctl set port sTEXf11-eth3 tag=110')  # hTEXf1gs1

        sTEXf12.cmd('ovs-vsctl set port sTEXf12-eth1 trunks=100')
        sTEXf12.cmd('ovs-vsctl set port sTEXf12-eth2 tag=100')  # hTEXf1cam1

        # ── Floor 2 ───────────────────────────────────────────────────
        sTEXf21.cmd('ovs-vsctl set port sTEXf21-eth1 trunks=30')
        sTEXf21.cmd('ovs-vsctl set port sTEXf21-eth2 tag=30')   # hTEXf2lab1

        sTEXf22.cmd('ovs-vsctl set port sTEXf22-eth1 trunks=100,120')
        sTEXf22.cmd('ovs-vsctl set port sTEXf22-eth2 tag=100')  # hTEXf2cam1
        sTEXf22.cmd('ovs-vsctl set port sTEXf22-eth3 tag=120')  # hTEXf2voi1

        # ── Floor 3 ───────────────────────────────────────────────────
        sTEXf31.cmd('ovs-vsctl set port sTEXf31-eth1 trunks=20')
        sTEXf31.cmd('ovs-vsctl set port sTEXf31-eth2 tag=20')   # hTEXf3eng1

        sTEXf32.cmd('ovs-vsctl set port sTEXf32-eth1 trunks=100,120')
        sTEXf32.cmd('ovs-vsctl set port sTEXf32-eth2 tag=100')  # hTEXf3cam1
        sTEXf32.cmd('ovs-vsctl set port sTEXf32-eth3 tag=120')  # hTEXf3voi1

        # ── Floor 4 ───────────────────────────────────────────────────
        sTEXf41.cmd('ovs-vsctl set port sTEXf41-eth1 trunks=20,70')
        sTEXf41.cmd('ovs-vsctl set port sTEXf41-eth2 tag=70')   # hTEXf4mr1
        sTEXf41.cmd('ovs-vsctl set port sTEXf41-eth3 tag=20')   # hTEXf4eng1

        sTEXf42.cmd('ovs-vsctl set port sTEXf42-eth1 trunks=100,120')
        sTEXf42.cmd('ovs-vsctl set port sTEXf42-eth2 tag=100')  # hTEXf4cam1
        sTEXf42.cmd('ovs-vsctl set port sTEXf42-eth3 tag=120')  # hTEXf4voi1

        # ── Floor 5 ───────────────────────────────────────────────────
        sTEXf51.cmd('ovs-vsctl set port sTEXf51-eth1 trunks=10,40,60,70')
        sTEXf51.cmd('ovs-vsctl set port sTEXf51-eth2 tag=10')   # hTEXf5exe1
        sTEXf51.cmd('ovs-vsctl set port sTEXf51-eth3 tag=40')   # hTEXf5hr1
        sTEXf51.cmd('ovs-vsctl set port sTEXf51-eth4 tag=70')   # hTEXf5mr1
        sTEXf51.cmd('ovs-vsctl set port sTEXf51-eth5 tag=60')   # hTEXf5prt1

        sTEXf52.cmd('ovs-vsctl set port sTEXf52-eth1 trunks=100,120')
        sTEXf52.cmd('ovs-vsctl set port sTEXf52-eth2 tag=100')  # hTEXf5cam1
        sTEXf52.cmd('ovs-vsctl set port sTEXf52-eth3 tag=120')  # hTEXf5voi1

        # ── Static host default routes ────────────────────────────────
        net.get('hTEXf1rec1').setDefaultRoute('via 10.40.50.1')
        net.get('hTEXf1cam1').setDefaultRoute('via 10.40.100.1')
        net.get('hTEXf2lab1').setDefaultRoute('via 10.40.30.1')
        net.get('hTEXf2cam1').setDefaultRoute('via 10.40.100.1')
        net.get('hTEXf2voi1').setDefaultRoute('via 10.40.120.1')
        net.get('hTEXf3eng1').setDefaultRoute('via 10.40.20.1')
        net.get('hTEXf3cam1').setDefaultRoute('via 10.40.100.1')
        net.get('hTEXf3voi1').setDefaultRoute('via 10.40.120.1')
        net.get('hTEXf4mr1').setDefaultRoute('via 10.40.70.1')
        net.get('hTEXf4eng1').setDefaultRoute('via 10.40.20.1')
        net.get('hTEXf4cam1').setDefaultRoute('via 10.40.100.1')
        net.get('hTEXf4voi1').setDefaultRoute('via 10.40.120.1')
        net.get('hTEXf5exe1').setDefaultRoute('via 10.40.10.1')
        net.get('hTEXf5hr1').setDefaultRoute('via 10.40.40.1')
        net.get('hTEXf5mr1').setDefaultRoute('via 10.40.70.1')
        net.get('hTEXf5prt1').setDefaultRoute('via 10.40.60.1')
        net.get('hTEXf5cam1').setDefaultRoute('via 10.40.100.1')
        net.get('hTEXf5voi1').setDefaultRoute('via 10.40.120.1')

        # ── Services ──────────────────────────────────────────────────
        hTEXdhcp1.cmd(f'rm -f {SITE_DIR}/TEX_dhcp.pid {SITE_DIR}/TEX_dhcp.leases {SITE_DIR}/TEX_dhcp.log')
        hTEXdhcp1.cmd(f'dnsmasq --conf-file={SITE_DIR}/TEX_dhcp.conf --addn-hosts={SITE_DIR}/records.txt --pid-file={SITE_DIR}/TEX_dhcp.pid --dhcp-leasefile={SITE_DIR}/TEX_dhcp.leases --log-dhcp --log-facility={SITE_DIR}/TEX_dhcp.log &')
        sTEXc1.cmd('pkill dhcrelay 2>/dev/null')
        sTEXc1.cmd('dhcrelay -4 -i texc1.v50 -i texc1.v110 10.40.130.40 &')

        hTEXweb1.cmd(f'python3 -m http.server 80 --directory {SITE_DIR}/web &')
        hTEXftp1.cmd(f'cd {SITE_DIR}/ftp && python3 -m pyftpdlib -p 21 -w -u admin -P secret123 &')

        sTEXc1.cmd(f'sed -i "/agco.texas/d" /etc/hosts && cat {SITE_DIR}/records.txt >> /etc/hosts')

        # ── Inter-VLAN access policy (iptables on sTEXc1) ─────────────
        c = sTEXc1.cmd
        c('iptables -N TEX_FWD 2>/dev/null; iptables -F TEX_FWD')
        c('iptables -C FORWARD -j TEX_FWD 2>/dev/null || iptables -A FORWARD -j TEX_FWD')

        c('iptables -A TEX_FWD -m state --state ESTABLISHED,RELATED -j ACCEPT')

        # Executives (10): no restriction — default ACCEPT covers them

        # Engineering (20): ↔ Engineering + Labs + Servers only
        c('iptables -A TEX_FWD -s 10.40.20.0/25 -d 10.40.20.0/25  -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.20.0/25 -d 10.40.30.0/25  -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.20.0/25 -d 10.40.130.0/26 -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.20.0/25 -d 10.10.20.0/23  -j ACCEPT')  # → Illinois Eng
        c('iptables -A TEX_FWD -s 10.40.20.0/25 -d 10.20.20.0/23  -j ACCEPT')  # → Monterrey Eng
        c('iptables -A TEX_FWD -s 10.40.20.0/25 -j REJECT --reject-with icmp-net-prohibited')

        # Labs (30): ↔ Labs + Engineering + Servers only
        c('iptables -A TEX_FWD -s 10.40.30.0/25 -d 10.40.30.0/25  -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.30.0/25 -d 10.40.20.0/25  -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.30.0/25 -d 10.40.130.0/26 -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.30.0/25 -j REJECT --reject-with icmp-net-prohibited')

        # HR (40): ↔ HR + Executives + Servers only
        c('iptables -A TEX_FWD -s 10.40.40.0/27 -d 10.40.40.0/27  -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.40.0/27 -d 10.40.10.0/27  -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.40.0/27 -d 10.40.130.0/26 -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.40.0/27 -j REJECT --reject-with icmp-net-prohibited')

        # Reception (50): ↔ Reception + VoIP + Cameras + Servers only
        c('iptables -A TEX_FWD -s 10.40.50.0/28 -d 10.40.50.0/28  -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.50.0/28 -d 10.40.120.0/26 -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.50.0/28 -d 10.40.100.0/26 -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.50.0/28 -d 10.40.130.0/26 -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.50.0/28 -j REJECT --reject-with icmp-net-prohibited')

        # Cameras (100): symmetric with Reception
        c('iptables -A TEX_FWD -s 10.40.100.0/26 -d 10.40.100.0/26 -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.100.0/26 -d 10.40.50.0/28  -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.100.0/26 -d 10.40.130.0/26 -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.100.0/26 -d 10.10.130.0/24 -j ACCEPT')  # → Illinois Servers (nightly replication)
        c('iptables -A TEX_FWD -s 10.40.100.0/26 -j REJECT --reject-with icmp-net-prohibited')

        # VoIP (120): symmetric with Reception
        c('iptables -A TEX_FWD -s 10.40.120.0/26 -d 10.40.120.0/26 -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.120.0/26 -d 10.40.50.0/28  -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.120.0/26 -d 10.40.130.0/26 -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.120.0/26 -j REJECT --reject-with icmp-net-prohibited')

        # Guests (110): TCP/80 to servers only — DROP (no ICMP response, fully dark)
        c('iptables -A TEX_FWD -s 10.40.110.0/28 -d 10.40.130.0/26 -p tcp --dport 80 -j ACCEPT')
        c('iptables -A TEX_FWD -s 10.40.110.0/28 -j DROP')


def run():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink, autoSetMacs=True)
    site = Texas()
    site.build(net)
    net.start()
    site.config(net)
    CLI(net)
    net.get('sTEXc1').cmd('pkill dhcrelay 2>/dev/null')
    net.get('sTEXc1').cmd('sed -i "/agco.texas/d" /etc/hosts')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()

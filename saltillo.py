import os
SITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saltillo')

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from base_nodes import SwitchL3, Router

# Saltillo site
#
# VLANs
#   10  Executives    10.30.10.0/28    gw 10.30.10.1
#   20  Engineering   10.30.20.0/25    gw 10.30.20.1
#   30  IoT Labs      10.30.30.0/24    gw 10.30.30.1
#   40  HR            10.30.40.0/27    gw 10.30.40.1
#   50  Reception     10.30.50.0/27    gw 10.30.50.1
#   60  Print Servers 10.30.60.0/28    gw 10.30.60.1
#   70  Meeting Rooms 10.30.70.0/27    gw 10.30.70.1
#   99  Uplink        10.30.99.0/30    p2p gateway ↔ core
#  100  Cameras       10.30.100.0/26   gw 10.30.100.1
#  110  Guests        10.30.110.0/28   gw 10.30.110.1
#  120  VoIP          10.30.120.0/26   gw 10.30.120.1
#  130  Servers       10.30.130.0/27   gw 10.30.130.1
#
# Inter-VLAN policy (enforced via iptables on sSALc1):
#   Executives (10)  → all VLANs
#   Engineering (20) ↔ Engineering + IoT (30) + Servers (130)
#   IoT (30)         ↔ IoT + Engineering (20) + Servers (130)
#   HR (40)          ↔ HR + Executives (10) + Servers (130)
#   Reception (50)   ↔ Reception + VoIP (120) + Cameras (100) + Servers (130)
#   VoIP (120)       ↔ VoIP + Reception (50) + Servers (130)
#   Cameras (100)    ↔ Cameras + Reception (50) + Servers (130)
#   Guests (110)     → TCP/80 to Servers only (no ping, no other VLANs)
#   Print (60), Meeting (70): unrestricted (default ACCEPT)


class Saltillo:

    def __init__(self):
        self.gateway = None

    def build(self, net):
        self.gateway = net.addHost('saltillo', cls=Router)

        # Core switch (L3)
        sSALc1 = net.addSwitch('sSALc1', cls=SwitchL3, failMode='standalone')

        # Server switch and service hosts – VLAN 130 (10.30.130.0/27)
        sSALs1    = net.addSwitch('sSALs1', failMode='standalone')
        hSALdns1  = net.addHost('hSALdns1',  ip='10.30.130.2/27', defaultRoute='via 10.30.130.1')
        hSALweb1  = net.addHost('hSALweb1',  ip='10.30.130.3/27', defaultRoute='via 10.30.130.1')
        hSALftp1  = net.addHost('hSALftp1',  ip='10.30.130.4/27', defaultRoute='via 10.30.130.1')
        hSALdhcp1 = net.addHost('hSALdhcp1', ip='10.30.130.5/27', defaultRoute='via 10.30.130.1')

        net.addLink(hSALdns1,  sSALs1)   # sSALs1-eth1
        net.addLink(hSALweb1,  sSALs1)   # sSALs1-eth2
        net.addLink(hSALftp1,  sSALs1)   # sSALs1-eth3
        net.addLink(hSALdhcp1, sSALs1)   # sSALs1-eth4

        # Distribution switches
        sSALd1 = net.addSwitch('sSALd1', failMode='standalone')  # Floor 1 & Lobby
        sSALd2 = net.addSwitch('sSALd2', failMode='standalone')  # Floor 2
        sSALd3 = net.addSwitch('sSALd3', failMode='standalone')  # Floor 3

        # Floor 1 & Lobby access switches
        sSALl1  = net.addSwitch('sSALl1',  failMode='standalone')  # Lobby
        sSALf11 = net.addSwitch('sSALf11', failMode='standalone')  # Eng + IoT + Print
        sSALf12 = net.addSwitch('sSALf12', failMode='standalone')  # Cameras + VoIP
        sSALf13 = net.addSwitch('sSALf13', failMode='standalone')  # Reception

        # Floor 2 access switches
        sSALf21 = net.addSwitch('sSALf21', failMode='standalone')  # Eng + HR
        sSALf22 = net.addSwitch('sSALf22', failMode='standalone')  # Cameras + VoIP
        sSALf23 = net.addSwitch('sSALf23', failMode='standalone')  # Meeting Rooms
        sSALf24 = net.addSwitch('sSALf24', failMode='standalone')  # spare

        # Floor 3 access switches
        sSALf31 = net.addSwitch('sSALf31', failMode='standalone')  # Exec + Eng
        sSALf32 = net.addSwitch('sSALf32', failMode='standalone')  # Cameras
        sSALf33 = net.addSwitch('sSALf33', failMode='standalone')  # VoIP

        # ── Switch links (order determines OVS port numbering) ────────
        net.addLink(self.gateway, sSALc1)  # saltillo-eth0  ↔ sSALc1-eth1
        net.addLink(sSALc1, sSALd1)       # sSALc1-eth2    ↔ sSALd1-eth1
        net.addLink(sSALc1, sSALd2)       # sSALc1-eth3    ↔ sSALd2-eth1
        net.addLink(sSALc1, sSALd3)       # sSALc1-eth4    ↔ sSALd3-eth1
        net.addLink(sSALc1, sSALs1)       # sSALc1-eth5    ↔ sSALs1-eth5

        net.addLink(sSALd1, sSALl1)       # sSALd1-eth2    ↔ sSALl1-eth1
        net.addLink(sSALd1, sSALf11)      # sSALd1-eth3    ↔ sSALf11-eth1
        net.addLink(sSALd1, sSALf12)      # sSALd1-eth4    ↔ sSALf12-eth1
        net.addLink(sSALd1, sSALf13)      # sSALd1-eth5    ↔ sSALf13-eth1

        net.addLink(sSALd2, sSALf21)      # sSALd2-eth2    ↔ sSALf21-eth1
        net.addLink(sSALd2, sSALf22)      # sSALd2-eth3    ↔ sSALf22-eth1
        net.addLink(sSALd2, sSALf23)      # sSALd2-eth4    ↔ sSALf23-eth1
        net.addLink(sSALd2, sSALf24)      # sSALd2-eth5    ↔ sSALf24-eth1

        net.addLink(sSALd3, sSALf31)      # sSALd3-eth2    ↔ sSALf31-eth1
        net.addLink(sSALd3, sSALf32)      # sSALd3-eth3    ↔ sSALf32-eth1
        net.addLink(sSALd3, sSALf33)      # sSALd3-eth4    ↔ sSALf33-eth1

        # ── Representative hosts ──────────────────────────────────────

        # Lobby
        hSALlrec1 = net.addHost('hSALlrec1', ip='10.30.50.10/27')
        hSALlgs1  = net.addHost('hSALlgs1',  ip=None, privateDirs=['/etc'])  # DHCP client
        net.addLink(hSALlrec1, sSALl1)    # sSALl1-eth2
        net.addLink(hSALlgs1,  sSALl1)    # sSALl1-eth3

        # Floor 1 – sSALf11 (Engineering + IoT + Print)
        hSALf1eng1 = net.addHost('hSALf1eng1', ip='10.30.20.10/25')
        hSALf1iot1 = net.addHost('hSALf1iot1', ip='10.30.30.10/24')
        hSALf1prt1 = net.addHost('hSALf1prt1', ip='10.30.60.2/28')
        net.addLink(hSALf1eng1, sSALf11)  # sSALf11-eth2
        net.addLink(hSALf1iot1, sSALf11)  # sSALf11-eth3
        net.addLink(hSALf1prt1, sSALf11)  # sSALf11-eth4

        # Floor 1 – sSALf12 (Cameras + VoIP)
        hSALf1cam1  = net.addHost('hSALf1cam1',  ip='10.30.100.10/26')
        hSALf1voi1 = net.addHost('hSALf1voi1', ip='10.30.120.10/26')
        net.addLink(hSALf1cam1,  sSALf12)  # sSALf12-eth2
        net.addLink(hSALf1voi1, sSALf12)  # sSALf12-eth3

        # Floor 1 – sSALf13 (Reception)
        hSALf1rec1 = net.addHost('hSALf1rec1', ip='10.30.50.11/27')
        net.addLink(hSALf1rec1, sSALf13)   # sSALf13-eth2

        # Floor 2 – sSALf21 (Engineering + HR)
        hSALf2eng1 = net.addHost('hSALf2eng1', ip='10.30.20.20/25')
        hSALf2hr1  = net.addHost('hSALf2hr1',  ip='10.30.40.10/27')
        net.addLink(hSALf2eng1, sSALf21)   # sSALf21-eth2
        net.addLink(hSALf2hr1,  sSALf21)   # sSALf21-eth3

        # Floor 2 – sSALf22 (Cameras + VoIP)
        hSALf2cam1  = net.addHost('hSALf2cam1',  ip='10.30.100.20/26')
        hSALf2voi1 = net.addHost('hSALf2voi1', ip='10.30.120.20/26')
        net.addLink(hSALf2cam1,  sSALf22)  # sSALf22-eth2
        net.addLink(hSALf2voi1, sSALf22)  # sSALf22-eth3

        # Floor 2 – sSALf23 (Meeting Rooms)
        hSALf2mr1 = net.addHost('hSALf2mr1', ip='10.30.70.10/27')
        net.addLink(hSALf2mr1, sSALf23)  # sSALf23-eth2

        # Floor 3 – sSALf31 (Executives + Engineering)
        hSALf3exe1 = net.addHost('hSALf3exe1', ip='10.30.10.2/28')
        hSALf3eng1 = net.addHost('hSALf3eng1', ip='10.30.20.30/25')
        net.addLink(hSALf3exe1, sSALf31)   # sSALf31-eth2
        net.addLink(hSALf3eng1, sSALf31)   # sSALf31-eth3

        # Floor 3 – sSALf32 (Cameras)
        hSALf3cam1 = net.addHost('hSALf3cam1', ip='10.30.100.30/26')
        net.addLink(hSALf3cam1, sSALf32)   # sSALf32-eth2

        # Floor 3 – sSALf33 (VoIP)
        hSALf3voi1 = net.addHost('hSALf3voi1', ip='10.30.120.30/26')
        net.addLink(hSALf3voi1, sSALf33)  # sSALf33-eth2

        print("Saltillo site built successfully!")

    def config(self, net):
        sSALc1  = net.get('sSALc1')
        sSALd1  = net.get('sSALd1')
        sSALd2  = net.get('sSALd2')
        sSALd3  = net.get('sSALd3')
        sSALl1  = net.get('sSALl1')
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
        hSALdhcp1 = net.get('hSALdhcp1')
        hSALweb1  = net.get('hSALweb1')
        hSALftp1  = net.get('hSALftp1')
        hSALlgs1  = net.get('hSALlgs1')

        # Fix: privateDirs=['/etc'] creates isolated /etc without fstab
        hSALlgs1.cmd('touch /etc/fstab')

        # ── Gateway ───────────────────────────────────────────────────
        self.gateway.setIP('10.30.99.1/30', intf='saltillo-eth0')
        self.gateway.cmd('ip route add 10.30.0.0/16 via 10.30.99.2')

        # ── Core switch: SVIs ─────────────────────────────────────────
        def add_svi(vlan, ip_cidr):
            name = f'salc1.v{vlan}'
            sSALc1.cmd(f'ovs-vsctl add-port sSALc1 {name} tag={vlan} -- set interface {name} type=internal')
            sSALc1.cmd(f'ip addr add {ip_cidr} dev {name} && ip link set {name} up')

        add_svi(10,  '10.30.10.1/28')
        add_svi(20,  '10.30.20.1/25')
        add_svi(30,  '10.30.30.1/24')
        add_svi(40,  '10.30.40.1/27')
        add_svi(50,  '10.30.50.1/27')
        add_svi(60,  '10.30.60.1/28')
        add_svi(70,  '10.30.70.1/27')
        add_svi(99,  '10.30.99.2/30')
        add_svi(100, '10.30.100.1/26')
        add_svi(110, '10.30.110.1/28')
        add_svi(120, '10.30.120.1/26')
        add_svi(130, '10.30.130.1/27')

        sSALc1.cmd('ip route add default via 10.30.99.1')

        # ── Core switch: port assignments ─────────────────────────────
        sSALc1.cmd('ovs-vsctl set port sSALc1-eth1 tag=99')
        sSALc1.cmd('ovs-vsctl set port sSALc1-eth2 trunks=10,20,30,40,50,60,70,100,110,120')  # to sSALd1
        sSALc1.cmd('ovs-vsctl set port sSALc1-eth3 trunks=10,20,40,50,60,70,100,120')          # to sSALd2
        sSALc1.cmd('ovs-vsctl set port sSALc1-eth4 trunks=10,20,50,60,70,100,120')             # to sSALd3
        sSALc1.cmd('ovs-vsctl set port sSALc1-eth5 tag=130')                                   # to sSALs1

        # ── Distribution 1 – Floor 1 & Lobby ─────────────────────────
        sSALd1.cmd('ovs-vsctl set port sSALd1-eth1 trunks=10,20,30,40,50,60,70,100,110,120')  # uplink
        sSALd1.cmd('ovs-vsctl set port sSALd1-eth2 trunks=50,110')       # to sSALl1  (Rec + Guest)
        sSALd1.cmd('ovs-vsctl set port sSALd1-eth3 trunks=20,30,60,100,120') # to sSALf11
        sSALd1.cmd('ovs-vsctl set port sSALd1-eth4 trunks=100,120')      # to sSALf12
        sSALd1.cmd('ovs-vsctl set port sSALd1-eth5 trunks=50')           # to sSALf13

        # ── Distribution 2 – Floor 2 ──────────────────────────────────
        sSALd2.cmd('ovs-vsctl set port sSALd2-eth1 trunks=10,20,40,50,60,70,100,120')  # uplink
        sSALd2.cmd('ovs-vsctl set port sSALd2-eth2 trunks=20,40')        # to sSALf21
        sSALd2.cmd('ovs-vsctl set port sSALd2-eth3 trunks=100,120')      # to sSALf22
        sSALd2.cmd('ovs-vsctl set port sSALd2-eth4 trunks=70')           # to sSALf23
        sSALd2.cmd('ovs-vsctl set port sSALd2-eth5 trunks=70')           # to sSALf24 (spare)

        # ── Distribution 3 – Floor 3 ──────────────────────────────────
        sSALd3.cmd('ovs-vsctl set port sSALd3-eth1 trunks=10,20,50,60,70,100,120')  # uplink
        sSALd3.cmd('ovs-vsctl set port sSALd3-eth2 trunks=10,20')        # to sSALf31
        sSALd3.cmd('ovs-vsctl set port sSALd3-eth3 trunks=100')          # to sSALf32
        sSALd3.cmd('ovs-vsctl set port sSALd3-eth4 trunks=120')          # to sSALf33

        # ── Lobby ─────────────────────────────────────────────────────
        sSALl1.cmd('ovs-vsctl set port sSALl1-eth1 trunks=50,110')
        sSALl1.cmd('ovs-vsctl set port sSALl1-eth2 tag=50')    # hSALlrec1
        sSALl1.cmd('ovs-vsctl set port sSALl1-eth3 tag=110')   # hSALlgs1

        # ── Floor 1 ───────────────────────────────────────────────────
        sSALf11.cmd('ovs-vsctl set port sSALf11-eth1 trunks=20,30,60,100,120')
        sSALf11.cmd('ovs-vsctl set port sSALf11-eth2 tag=20')  # hSALf1eng1
        sSALf11.cmd('ovs-vsctl set port sSALf11-eth3 tag=30')  # hSALf1iot1
        sSALf11.cmd('ovs-vsctl set port sSALf11-eth4 tag=60')  # hSALf1prt1

        sSALf12.cmd('ovs-vsctl set port sSALf12-eth1 trunks=100,120')
        sSALf12.cmd('ovs-vsctl set port sSALf12-eth2 tag=100') # hSALf1cam1
        sSALf12.cmd('ovs-vsctl set port sSALf12-eth3 tag=120') # hSALf1voi1

        sSALf13.cmd('ovs-vsctl set port sSALf13-eth1 trunks=50')
        sSALf13.cmd('ovs-vsctl set port sSALf13-eth2 tag=50')  # hSALf1rec1

        # ── Floor 2 ───────────────────────────────────────────────────
        sSALf21.cmd('ovs-vsctl set port sSALf21-eth1 trunks=20,40')
        sSALf21.cmd('ovs-vsctl set port sSALf21-eth2 tag=20')  # hSALf2eng1
        sSALf21.cmd('ovs-vsctl set port sSALf21-eth3 tag=40')  # hSALf2hr1

        sSALf22.cmd('ovs-vsctl set port sSALf22-eth1 trunks=100,120')
        sSALf22.cmd('ovs-vsctl set port sSALf22-eth2 tag=100') # hSALf2cam1
        sSALf22.cmd('ovs-vsctl set port sSALf22-eth3 tag=120') # hSALf2voi1

        sSALf23.cmd('ovs-vsctl set port sSALf23-eth1 trunks=70')
        sSALf23.cmd('ovs-vsctl set port sSALf23-eth2 tag=70')  # hSALf2mr1

        sSALf24.cmd('ovs-vsctl set port sSALf24-eth1 trunks=70')  # spare

        # ── Floor 3 ───────────────────────────────────────────────────
        sSALf31.cmd('ovs-vsctl set port sSALf31-eth1 trunks=10,20')
        sSALf31.cmd('ovs-vsctl set port sSALf31-eth2 tag=10')  # hSALf3exe1
        sSALf31.cmd('ovs-vsctl set port sSALf31-eth3 tag=20')  # hSALf3eng1

        sSALf32.cmd('ovs-vsctl set port sSALf32-eth1 trunks=100')
        sSALf32.cmd('ovs-vsctl set port sSALf32-eth2 tag=100') # hSALf3cam1

        sSALf33.cmd('ovs-vsctl set port sSALf33-eth1 trunks=120')
        sSALf33.cmd('ovs-vsctl set port sSALf33-eth2 tag=120') # hSALf3voi1

        # ── Static host default routes ────────────────────────────────
        net.get('hSALlrec1').setDefaultRoute('via 10.30.50.1')
        net.get('hSALf1eng1').setDefaultRoute('via 10.30.20.1')
        net.get('hSALf1iot1').setDefaultRoute('via 10.30.30.1')
        net.get('hSALf1prt1').setDefaultRoute('via 10.30.60.1')
        net.get('hSALf1cam1').setDefaultRoute('via 10.30.100.1')
        net.get('hSALf1voi1').setDefaultRoute('via 10.30.120.1')
        net.get('hSALf1rec1').setDefaultRoute('via 10.30.50.1')
        net.get('hSALf2eng1').setDefaultRoute('via 10.30.20.1')
        net.get('hSALf2hr1').setDefaultRoute('via 10.30.40.1')
        net.get('hSALf2cam1').setDefaultRoute('via 10.30.100.1')
        net.get('hSALf2voi1').setDefaultRoute('via 10.30.120.1')
        net.get('hSALf2mr1').setDefaultRoute('via 10.30.70.1')
        net.get('hSALf3exe1').setDefaultRoute('via 10.30.10.1')
        net.get('hSALf3eng1').setDefaultRoute('via 10.30.20.1')
        net.get('hSALf3cam1').setDefaultRoute('via 10.30.100.1')
        net.get('hSALf3voi1').setDefaultRoute('via 10.30.120.1')

        # ── Services ──────────────────────────────────────────────────
        hSALdhcp1.cmd(f'rm -f {SITE_DIR}/SAL_dhcp.pid {SITE_DIR}/SAL_dhcp.leases {SITE_DIR}/SAL_dhcp.log')
        hSALdhcp1.cmd(f'dnsmasq --conf-file={SITE_DIR}/SAL_dhcp.conf --addn-hosts={SITE_DIR}/records.txt --pid-file={SITE_DIR}/SAL_dhcp.pid --dhcp-leasefile={SITE_DIR}/SAL_dhcp.leases --log-dhcp --log-facility={SITE_DIR}/SAL_dhcp.log &')
        sSALc1.cmd('pkill dhcrelay 2>/dev/null')
        sSALc1.cmd('dhcrelay -4 -i salc1.v50 -i salc1.v110 10.30.130.5 &')

        hSALweb1.cmd(f'python3 -m http.server 80 --directory {SITE_DIR}/web &')
        hSALftp1.cmd(f'cd {SITE_DIR}/ftp && python3 -m pyftpdlib -p 21 -w -u admin -P secret123 &')

        sSALc1.cmd(f'sed -i "/agco.saltillo/d" /etc/hosts && cat {SITE_DIR}/records.txt >> /etc/hosts')

        # ── Inter-VLAN access policy (iptables on sSALc1) ─────────────
        # All OVSSwitch nodes share the root namespace, so each site uses
        # its own chain to avoid flushing rules set by other sites.
        c = sSALc1.cmd
        c('iptables -N SAL_FWD 2>/dev/null; iptables -F SAL_FWD')
        c('iptables -C FORWARD -j SAL_FWD 2>/dev/null || iptables -A FORWARD -j SAL_FWD')

        c('iptables -A SAL_FWD -m state --state ESTABLISHED,RELATED -j ACCEPT')

        # Executives (10): no restriction — default ACCEPT covers them

        # Engineering (20): ↔ Engineering + IoT + Servers only
        c('iptables -A SAL_FWD -s 10.30.20.0/25 -d 10.30.20.0/25  -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.20.0/25 -d 10.30.30.0/24  -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.20.0/25 -d 10.30.130.0/27 -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.20.0/25 -d 10.10.20.0/23  -j ACCEPT')  # → Illinois Eng
        c('iptables -A SAL_FWD -s 10.30.20.0/25 -d 10.20.20.0/23  -j ACCEPT')  # → Monterrey Eng
        c('iptables -A SAL_FWD -s 10.30.20.0/25 -j REJECT --reject-with icmp-net-prohibited')

        # IoT (30): ↔ IoT + Engineering + Servers only
        c('iptables -A SAL_FWD -s 10.30.30.0/24 -d 10.30.30.0/24  -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.30.0/24 -d 10.30.20.0/25  -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.30.0/24 -d 10.30.130.0/27 -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.30.0/24 -j REJECT --reject-with icmp-net-prohibited')

        # HR (40): ↔ HR + Executives + Servers only
        c('iptables -A SAL_FWD -s 10.30.40.0/27 -d 10.30.40.0/27  -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.40.0/27 -d 10.30.10.0/28  -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.40.0/27 -d 10.30.130.0/27 -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.40.0/27 -j REJECT --reject-with icmp-net-prohibited')

        # Reception (50): ↔ Reception + VoIP + Cameras + Servers only
        c('iptables -A SAL_FWD -s 10.30.50.0/27 -d 10.30.50.0/27  -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.50.0/27 -d 10.30.120.0/26 -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.50.0/27 -d 10.30.100.0/26 -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.50.0/27 -d 10.30.130.0/27 -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.50.0/27 -j REJECT --reject-with icmp-net-prohibited')

        # Cameras (100): symmetric with Reception
        c('iptables -A SAL_FWD -s 10.30.100.0/26 -d 10.30.100.0/26 -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.100.0/26 -d 10.30.50.0/27  -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.100.0/26 -d 10.30.130.0/27 -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.100.0/26 -j REJECT --reject-with icmp-net-prohibited')

        # VoIP (120): symmetric with Reception
        c('iptables -A SAL_FWD -s 10.30.120.0/26 -d 10.30.120.0/26 -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.120.0/26 -d 10.30.50.0/27  -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.120.0/26 -d 10.30.130.0/27 -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.120.0/26 -j REJECT --reject-with icmp-net-prohibited')

        # Guests (110): TCP/80 to servers only — DROP (no ICMP response, fully dark)
        c('iptables -A SAL_FWD -s 10.30.110.0/28 -d 10.30.130.0/27 -p tcp --dport 80 -j ACCEPT')
        c('iptables -A SAL_FWD -s 10.30.110.0/28 -j DROP')


def run():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink, autoSetMacs=True)
    site = Saltillo()
    site.build(net)
    net.start()
    site.config(net)
    CLI(net)
    net.get('sSALc1').cmd('pkill dhcrelay 2>/dev/null')
    net.get('sSALc1').cmd('sed -i "/agco.saltillo/d" /etc/hosts')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()

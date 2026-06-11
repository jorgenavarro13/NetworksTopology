#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import OVSSwitch, Node
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class SwitchL3(OVSSwitch):
    def config(self, **params):
        super(SwitchL3, self).config(**params)
        # Ensure root namespace routes cleanly between SVIs and transit segments
        self.cmd('sysctl -w net.ipv4.ip_forward=1')
        self.cmd('sysctl -w net.ipv4.conf.all.rp_filter=0')
        self.cmd('sysctl -w net.ipv4.conf.default.rp_filter=0')
        self.cmd('iptables -P FORWARD ACCEPT')
        self.cmd('iptables -F FORWARD')

class Router(Node):
    def config(self, **params):
        super(Router, self).config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')
        self.cmd('sysctl -w net.ipv4.conf.all.rp_filter=0')
        self.cmd('sysctl -w net.ipv4.conf.default.rp_filter=0')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super(Router, self).terminate()

class Texas(Node):
    def __init__(self):
        self.gateway = None
    
    # Rango principal: 10.40.0.0/16 
    def build(self, net: Mininet):
        # WAN link to Illinois
        self.gateway = net.addHost('texas1', cls=Router, ip='10.40.255.254/16')

        # Layer 3 Switch / Core
        sp = net.addSwitch('sp', dpid='00000000000000A1', cls=SwitchL3, failMode='standalone')

        # Distribution Switches
        s1 = net.addSwitch('s1', failMode='standalone')
        s2 = net.addSwitch('s2', failMode='standalone')
        s3 = net.addSwitch('s3', failMode='standalone')
        s4 = net.addSwitch('s4', failMode='standalone')
        s5 = net.addSwitch('s5', failMode='standalone')

        # --- Switch Connection ---
        net.addLink(self.gateway, sp) # texas-eth1 <-> sp-eth1
        net.addLink(sp, s1) # sp-eth2 <-> s1-eth1
        net.addLink(sp, s2) # sp-eth3 <-> s2-eth1
        net.addLink(sp, s3) # sp-eth4 <-> s3-eth1
        net.addLink(sp, s4) # sp-eth5 <-> s4-eth1
        net.addLink(sp, s5) # sp-eth6 <-> s5-eth1

        # ============= REPRESENTATIVE HOSTS ================

        # ----======= PISO NO° 1 =======-----
        # El piso cuenta con: Servidor DHCP, Cámaras, Recepción, Invitados
        s1f1 = net.addSwitch('s1f1', failMode='standalone') 
        s2f1 = net.addSwitch('s2f1', failMode='standalone')
        s3f1 = net.addSwitch('s3f1', failMode='standalone')

        net.addLink(s1, s1f1) # s1-eth2 <-> s1f1-eth1
        net.addLink(s1, s2f1) # s1-eth3 <-> s2f1-eth1
        net.addLink(s1, s3f1) # s1-eth4 <-> s3f1-eth1 (PoE)

        dhcp1srv= net.addHost('dhcp1srv', ip='10.40.130.2/26', defaultRoute='via 10.40.130.1')
        ihf1gst = net.addHost('ihf1gst', ip=None) # Awaits DHCP IP in the 10.40.110.0/28 range
        ihf1rec = net.addHost('ihf1rec', ip='10.40.50.2/28', defaultRoute='via 10.40.50.1')
        ihf1cam = net.addHost('ihf1cam', ip='10.40.100.2/26', defaultRoute='via 10.40.100.1')

        net.addLink(dhcp1srv, s1f1) # dhcp1srv-eth1 <-> s1f1-eth2
        net.addLink(ihf1rec, s2f1)  # ihf1rec-eth1 <-> s2f1-eth2
        net.addLink(ihf1gst, s2f1) # ihf1gst-eth1 <-> s2f1-eth3
        net.addLink(ihf1cam, s3f1) # ihf1cam-eth1 <-> s3f1-eth4

        # ----======= PISO NO° 2 =======-----
        # El piso cuenta con: VoIP, Cámaras, Laboratorios. 
        s1f2 = net.addSwitch('s1f2', failMode='standalone')
        s2f2 = net.addSwitch('s2f2', failMode='standalone')
        s3f2 = net.addSwitch('s3f2', failMode='standalone')

        net.addLink(s2, s1f2) # s2-eth2 <-> s1f2-eth1
        net.addLink(s2, s2f2) # s2-eth3 <-> s2f2-eth1
        net.addLink(s2, s3f2) # s2-eth4 <-> s3f2-eth1 (PoE)

        # Updated masks based on VLSM Table
        ihf2vip = net.addHost('ihf2vip', ip='10.40.120.2/26', defaultRoute='via 10.40.120.1')
        ihf2cam = net.addHost('ihf2cam', ip='10.40.100.3/26', defaultRoute='via 10.40.100.1')
        ihf2lab = net.addHost('ihf2lab', ip='10.40.30.2/25', defaultRoute='via 10.40.30.1')

        net.addLink(ihf2lab, s1f2) # ihf2lab-eth1 <-> s1f2-eth2
        net.addLink(ihf2cam, s3f2) # ihf2vip-eth1 <-> s3f2-eth2
        net.addLink(ihf2vip, s3f2) # ihf2cam-eth1 <-> s3f2-eth3

        # ----======= PISO NO° 3 =======-----
        # El piso cuenta con: VoIP, Cámaras, Ingeniería.
        s1f3 = net.addSwitch('s1f3', failMode='standalone')
        s2f3 = net.addSwitch('s2f3', failMode='standalone')

        net.addLink(s3, s1f3) # s3-eth2 <-> s1f3-eth1
        net.addLink(s3, s2f3) # s3-eth3 <-> s2f3-eth1 (Poe)

        ihf3vip = net.addHost('ihf3vip', ip='10.40.120.3/26', defaultRoute='via 10.40.120.1')
        ihf3cam = net.addHost('ihf3cam', ip='10.40.100.4/26', defaultRoute='via 10.40.100.1')
        ihf3eng = net.addHost('ihf3eng', ip='10.40.20.2/25', defaultRoute='via 10.40.20.1')

        net.addLink(ihf3eng, s1f3) # ihg3eng-eth1 <-> s1f3-eth2
        net.addLink(ihf3cam, s2f3) # ihf3cam-eth1 <-> s2f3-eth2
        net.addLink(ihf3vip, s2f3) # ihf3vip-eth1 <-> s2f3-eth3

        # ----======= PISO NO° 4 =======-----
        # El piso cuenta con: VoIP, Cámaras, Ingeniería, Salas de Conferencia. 
        s1f4 = net.addSwitch('s1f4', failMode='standalone')
        s2f4 = net.addSwitch('s2f4', failMode='standalone')
        s3f4 = net.addSwitch('s3f4', failMode='standalone')

        net.addLink(s4, s1f4) # s3-eth2 <-> s1f4-eth1
        net.addLink(s4, s2f4) # s3-eth3 <-> s2f4-eth1
        net.addLink(s4, s3f4) # s3-eth4 <-> s3f4-eth1

        ihf4vip = net.addHost('ihf4vip', ip='10.40.120.4/26', defaultRoute='via 10.40.120.1')
        ihf4cam = net.addHost('ihf4cam', ip='10.40.100.5/26', defaultRoute='via 10.40.100.1')
        ihf4mrs = net.addHost('ihf4mrs', ip='10.40.70.2/27', defaultRoute='via 10.40.70.1')
        ihf4eng = net.addHost('ihf4eng', ip='10.40.20.3/25', defaultRoute='via 10.40.20.1')
        
        net.addLink(ihf4mrs, s1f4) # ihf4cam-eth1 <-> s1f4-eth2
        net.addLink(ihf4eng, s2f4) # ihf4vip-eth1 <-> s2f4-eth2
        net.addLink(ihf4cam, s3f4) # ihf4eng-eth1 <-> s3f4-eth2
        net.addLink(ihf4vip, s3f4) # ihf4mrs-eth1 <-> s3f4-eth3

        # ----======= PISO NO° 5 =======-----
        # El piso cuenta con: VoIP, Cámaras, Salas de Conferencia, RH, Ejecutivos, Impresoras.
        s1f5 = net.addSwitch('s1f5', failMode='standalone')
        s2f5 = net.addSwitch('s2f5', failMode='standalone')
        s3f5 = net.addSwitch('s3f5', failMode='standalone')
        # s4f5 = net.addSwitch('s4f5', failMode='standalone') 

        net.addLink(s5, s1f5) # s5-eth2 <-> s1f5-eth1
        net.addLink(s5, s2f5) # s5-eth3 <-> s2f5-eth1
        net.addLink(s5, s3f5) # s5-eth4 <-> s3f5-eth1

        ihf5vip = net.addHost('ihf5vip', ip='10.40.120.5/26', defaultRoute='via 10.40.120.1')
        ihf5cam = net.addHost('ihf5cam', ip='10.40.100.6/26', defaultRoute='via 10.40.100.1')
        ihf5mrs = net.addHost('ihf5mrs', ip='10.40.70.3/27', defaultRoute='via 10.40.70.1')
        ihf5prn = net.addHost('ihf5prn', ip='10.40.60.2/28', defaultRoute='via 10.40.60.1')
        ihf5hrs = net.addHost('ihf5hrs', ip='10.40.40.2/27', defaultRoute='via 10.40.40.1')
        ihf5exe = net.addHost('ihf5exe', ip='10.40.10.2/27', defaultRoute='via 10.40.10.1')

        net.addLink(ihf5mrs, s1f5) # ihf5cam-eth1 <-> s1f5-eth2
        net.addLink(ihf5exe, s2f5) # ihf5vip-eth1 <-> s2f5-eth2
        net.addLink(ihf5hrs, s2f5) # ihf5mrs-eth1 <-> s2f5-eth3
        net.addLink(ihf5prn, s2f5) # ihf5hrs-eth1 <-> s2f5-eth4
        net.addLink(ihf5cam, s3f5) # ihf5exe-eth1 <-> s3f5-eth2
        net.addLink(ihf5vip, s3f5) # ihf5prn-eth1 <-> s3f5-eth3

        # ================ RUNTIME ================
        net.start()

        # ---------------- VLANs PISO 1 ----------------
        s1f1.cmd('ovs-vsctl set port s1f1-eth2 tag=130') # Servidor DHCP
        s2f1.cmd('ovs-vsctl set port s2f1-eth2 tag=50')  # Recepcion
        s2f1.cmd('ovs-vsctl set port s2f1-eth3 tag=110') # Invitados
        s3f1.cmd('ovs-vsctl set port s3f1-eth2 tag=100') # Camaras

        # ---------------- VLANs PISO 2 ----------------
        s1f2.cmd('ovs-vsctl set port s1f2-eth2 tag=30')  # IoT Labs
        s3f2.cmd('ovs-vsctl set port s3f2-eth2 tag=100') # Camaras
        s3f2.cmd('ovs-vsctl set port s3f2-eth3 tag=120') # VoIP

        # ---------------- VLANs PISO 3 ----------------
        s1f3.cmd('ovs-vsctl set port s1f3-eth2 tag=20') # Ingenieria
        s2f3.cmd('ovs-vsctl set port s2f3-eth2 tag=100') # Camaras
        s2f3.cmd('ovs-vsctl set port s2f3-eth3 tag=120') # VoIP

        # ---------------- VLANs PISO 4 ----------------
        s1f4.cmd('ovs-vsctl set port s1f4-eth2 tag=70') # Sala de Reuniones
        s2f4.cmd('ovs-vsctl set port s2f4-eth2 tag=20') # Ingenieria
        s3f4.cmd('ovs-vsctl set port s3f4-eth2 tag=100') # Camaras
        s3f4.cmd('ovs-vsctl set port s3f4-eth3 tag=120') # VoIP

        # ---------------- VLANs PISO 5 ----------------
        s1f5.cmd('ovs-vsctl set port s1f5-eth2 tag=70') # Sala de Reuniones
        s2f5.cmd('ovs-vsctl set port s2f5-eth2 tag=10') # Ejecutivos
        s2f5.cmd('ovs-vsctl set port s2f5-eth3 tag=40') # RH
        s2f5.cmd('ovs-vsctl set port s2f5-eth4 tag=60') # Servidores de Impresion
        s3f5.cmd('ovs-vsctl set port s3f5-eth2 tag=100') # Camaras
        s3f5.cmd('ovs-vsctl set port s3f5-eth3 tag=120') # VoIP

        # -->
        # ----=======---- Aislacion de Capa 3 ----=======----
        # -->

        vlan_str = "10,20,30,40,50,60,70,100,110,120,130"
        sp.cmd(f'ovs-vsctl set port sp trunk={vlan_str}')

        for link in net.links:
            node1, node2 = link.intf1.node, link.intf2.node
            
            if isinstance(node1, OVSSwitch) and isinstance(node2, OVSSwitch):
                node1.cmd(f'ovs-vsctl set port {link.intf1.name} trunk={vlan_str}')
                node2.cmd(f'ovs-vsctl set port {link.intf2.name} trunk={vlan_str}')

        gateways = {
            10: '10.40.10.1/27',
            20: '10.40.20.1/25',
            30: '10.40.30.1/25',
            40: '10.40.40.1/27',
            50: '10.40.50.1/28',
            60: '10.40.60.1/28',
            70: '10.40.70.1/27',
            100: '10.40.100.1/26',
            110: '10.40.110.1/28',
            120: '10.40.120.1/26',
            130: '10.40.130.1/26'
        }

        for vlan, ip in gateways.items():
            # Create the virtual VLAN interface on the sp switch
            sp.cmd(f'ip link add link sp name sp.{vlan} type vlan id {vlan}')
            # Assign the gateway IP to it
            sp.cmd(f'ip addr add {ip} dev sp.{vlan}')
            # Turn the interface ON
            sp.cmd(f'ip link set sp.{vlan} up')

        # sp.cmd('iptables -A FORWARD -s 10.40.20.0/25 -d 10.10.20.0/23 -j ACCEPT')
        # sp.cmd('iptables -A FORWARD -s 10.40.20.0/25 -d 10.10.0.0/16 -j DROP')

        CLI(net)
        net.stop()

def execute():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink)
    site = Texas()
    site.build(net)

if __name__ == "__main__":
    setLogLevel("info")
    execute()
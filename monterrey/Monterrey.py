#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import OVSSwitch, Node
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel


class SwitchL3(OVSSwitch):
    def config(self, **params):
        super(SwitchL3, self).config(**params)
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


class Monterrey:
    def __init__(self):
        self.gateway = None

    def set_access(self, sw, port, vlan):
        sw.cmd(f'ovs-vsctl set port {port} vlan_mode=access tag={vlan}')

    def set_trunk(self, sw, port, vlan_str):
        sw.cmd(f'ovs-vsctl set port {port} vlan_mode=trunk trunks={vlan_str}')

    def build(self, net: Mininet):
        vlan_str = "10,20,30,40,50,60,70,100,110,120,130"

        # ================= ROUTER / WAN =================
        self.gateway = net.addHost(
            'monterrey',
            cls=Router,
            ip='10.20.255.254/16'
        )

        # IMPORTANTE: sp necesita dpid porque "sp" no es nombre tipo s1, s2, etc.
        sp = net.addSwitch(
            'sp',
            dpid='00000000000000b1',
            cls=SwitchL3,
            failMode='standalone'
        )

        # ================= DISTRIBUTION SWITCHES =================
        s1 = net.addSwitch('s1', failMode='standalone')  # piso 1
        s2 = net.addSwitch('s2', failMode='standalone')  # piso 2
        s3 = net.addSwitch('s3', failMode='standalone')  # piso 3
        s4 = net.addSwitch('s4', failMode='standalone')  # piso 4

        net.addLink(self.gateway, sp)
        net.addLink(sp, s1)
        net.addLink(sp, s2)
        net.addLink(sp, s3)
        net.addLink(sp, s4)

        # ================= PISO 1 =================
        s1f1 = net.addSwitch('s1f1', failMode='standalone')
        s1f2 = net.addSwitch('s1f2', failMode='standalone')
        s1f3 = net.addSwitch('s1f3', failMode='standalone')

        net.addLink(s1, s1f1)
        net.addLink(s1, s1f2)
        net.addLink(s1, s1f3)

        hf1rec1 = net.addHost(
            'hf1rec1',
            ip='10.20.50.5/28',
            defaultRoute='via 10.20.50.1'
        )

        hf1guest1 = net.addHost(
            'hf1guest1',
            ip='10.20.110.10/26',
            defaultRoute='via 10.20.110.1'
        )

        hf1srv1 = net.addHost(
            'hf1srv1',
            ip='10.20.130.10/27',
            defaultRoute='via 10.20.130.1'
        )

        hf1srv2 = net.addHost(
            'hf1srv2',
            ip='10.20.130.20/27',
            defaultRoute='via 10.20.130.1'
        )

        hf1voip1 = net.addHost(
            'hf1voip1',
            ip='10.20.120.10/24',
            defaultRoute='via 10.20.120.1'
        )

        hf1cam1 = net.addHost(
            'hf1cam1',
            ip='10.20.100.10/27',
            defaultRoute='via 10.20.100.1'
        )

        net.addLink(hf1rec1, s1f1)
        net.addLink(hf1guest1, s1f1)
        net.addLink(hf1srv1, s1f2)
        net.addLink(hf1srv2, s1f2)
        net.addLink(hf1voip1, s1f3)
        net.addLink(hf1cam1, s1f3)

        # ================= PISO 2 =================
        s2f1 = net.addSwitch('s2f1', failMode='standalone')
        s2f2 = net.addSwitch('s2f2', failMode='standalone')

        net.addLink(s2, s2f1)
        net.addLink(s2, s2f2)

        hf2iot1 = net.addHost(
            'hf2iot1',
            ip='10.20.30.10/26',
            defaultRoute='via 10.20.30.1'
        )

        hf2iot2 = net.addHost(
            'hf2iot2',
            ip='10.20.30.20/26',
            defaultRoute='via 10.20.30.1'
        )

        hf2print1 = net.addHost(
            'hf2print1',
            ip='10.20.60.5/28',
            defaultRoute='via 10.20.60.1'
        )

        hf2rec1 = net.addHost(
            'hf2rec1',
            ip='10.20.50.6/28',
            defaultRoute='via 10.20.50.1'
        )

        hf2voip1 = net.addHost(
            'hf2voip1',
            ip='10.20.120.20/24',
            defaultRoute='via 10.20.120.1'
        )

        hf2cam1 = net.addHost(
            'hf2cam1',
            ip='10.20.100.11/27',
            defaultRoute='via 10.20.100.1'
        )

        net.addLink(hf2iot1, s2f1)
        net.addLink(hf2iot2, s2f1)
        net.addLink(hf2print1, s2f1)
        net.addLink(hf2rec1, s2f1)
        net.addLink(hf2voip1, s2f2)
        net.addLink(hf2cam1, s2f2)

        # ================= PISO 3 =================
        s3f1 = net.addSwitch('s3f1', failMode='standalone')
        s3f2 = net.addSwitch('s3f2', failMode='standalone')
        s3f3 = net.addSwitch('s3f3', failMode='standalone')
        s3f4 = net.addSwitch('s3f4', failMode='standalone')

        net.addLink(s3, s3f1)
        net.addLink(s3, s3f2)
        net.addLink(s3, s3f3)
        net.addLink(s3, s3f4)

        hf3eng1 = net.addHost(
            'hf3eng1',
            ip='10.20.20.10/23',
            defaultRoute='via 10.20.20.1'
        )

        hf3eng2 = net.addHost(
            'hf3eng2',
            ip='10.20.20.20/23',
            defaultRoute='via 10.20.20.1'
        )

        hf3eng3 = net.addHost(
            'hf3eng3',
            ip='10.20.20.30/23',
            defaultRoute='via 10.20.20.1'
        )

        hf3rec1 = net.addHost(
            'hf3rec1',
            ip='10.20.50.7/28',
            defaultRoute='via 10.20.50.1'
        )

        hf3mtg1 = net.addHost(
            'hf3mtg1',
            ip='10.20.70.10/26',
            defaultRoute='via 10.20.70.1'
        )

        hf3voip1 = net.addHost(
            'hf3voip1',
            ip='10.20.120.30/24',
            defaultRoute='via 10.20.120.1'
        )

        hf3cam1 = net.addHost(
            'hf3cam1',
            ip='10.20.100.12/27',
            defaultRoute='via 10.20.100.1'
        )

        net.addLink(hf3eng1, s3f1)
        net.addLink(hf3eng2, s3f2)
        net.addLink(hf3rec1, s3f2)
        net.addLink(hf3eng3, s3f3)
        net.addLink(hf3mtg1, s3f3)
        net.addLink(hf3voip1, s3f4)
        net.addLink(hf3cam1, s3f4)


        # ================= PISO 4 =================
        s4f1 = net.addSwitch('s4f1', failMode='standalone')
        s4f2 = net.addSwitch('s4f2', failMode='standalone')
        s4f3 = net.addSwitch('s4f3', failMode='standalone')
        s4f4 = net.addSwitch('s4f4', failMode='standalone')

        net.addLink(s4, s4f1)
        net.addLink(s4, s4f2)
        net.addLink(s4, s4f3)
        net.addLink(s4, s4f4)

        hf4eng1 = net.addHost(
            'hf4eng1',
            ip='10.20.20.40/23',
            defaultRoute='via 10.20.20.1'
        )

        hf4eng2 = net.addHost(
            'hf4eng2',
            ip='10.20.20.50/23',
            defaultRoute='via 10.20.20.1'
        )

        hf4eng3 = net.addHost(
            'hf4eng3',
            ip='10.20.20.60/23',
            defaultRoute='via 10.20.20.1'
        )

        hf4exec1 = net.addHost(
            'hf4exec1',
            ip='10.20.10.10/27',
            defaultRoute='via 10.20.10.1'
        )

        hf4hr1 = net.addHost(
            'hf4hr1',
            ip='10.20.40.10/27',
            defaultRoute='via 10.20.40.1'
        )

        hf4rec1 = net.addHost(
            'hf4rec1',
            ip='10.20.50.8/28',
            defaultRoute='via 10.20.50.1'
        )

        hf4voip1 = net.addHost(
            'hf4voip1',
            ip='10.20.120.40/24',
            defaultRoute='via 10.20.120.1'
        )

        hf4cam1 = net.addHost(
            'hf4cam1',
            ip='10.20.100.13/27',
            defaultRoute='via 10.20.100.1'
        )

        net.addLink(hf4eng1, s4f1)
        net.addLink(hf4eng2, s4f2)
        net.addLink(hf4eng3, s4f3)
        net.addLink(hf4exec1, s4f3)
        net.addLink(hf4hr1, s4f3)
        net.addLink(hf4rec1, s4f3)
        net.addLink(hf4voip1, s4f4)
        net.addLink(hf4cam1, s4f4)



        # ================= START =================
        net.start()

        # ================= ACCESS PORTS =================
        # Piso 1
        self.set_access(s1f1, 's1f1-eth2', 50)    # Reception
        self.set_access(s1f1, 's1f1-eth3', 110)   # Guests
        self.set_access(s1f2, 's1f2-eth2', 130)   # Servers
        self.set_access(s1f2, 's1f2-eth3', 130)   # Servers
        self.set_access(s1f3, 's1f3-eth2', 120)   # VoIP
        self.set_access(s1f3, 's1f3-eth3', 100)   # Cameras

        # Piso 2
        self.set_access(s2f1, 's2f1-eth2', 30)    # IoT
        self.set_access(s2f1, 's2f1-eth3', 30)    # IoT
        self.set_access(s2f1, 's2f1-eth4', 60)    # Print Servers
        self.set_access(s2f1, 's2f1-eth5', 50)    # Reception
        self.set_access(s2f2, 's2f2-eth2', 120)   # VoIP
        self.set_access(s2f2, 's2f2-eth3', 100)   # Cameras

        # Piso 3
        self.set_access(s3f1, 's3f1-eth2', 20)    # Engineering
        self.set_access(s3f2, 's3f2-eth2', 20)    # Engineering overflow
        self.set_access(s3f2, 's3f2-eth3', 50)    # Reception
        self.set_access(s3f3, 's3f3-eth2', 20)    # Engineering overflow
        self.set_access(s3f3, 's3f3-eth3', 70)    # Meeting Rooms
        self.set_access(s3f4, 's3f4-eth2', 120)   # VoIP
        self.set_access(s3f4, 's3f4-eth3', 100)   # Cameras

        # Piso 4
        self.set_access(s4f1, 's4f1-eth2', 20)    # Engineering
        self.set_access(s4f2, 's4f2-eth2', 20)    # Engineering
        self.set_access(s4f3, 's4f3-eth2', 20)    # Engineering overflow
        self.set_access(s4f3, 's4f3-eth3', 10)    # Executives
        self.set_access(s4f3, 's4f3-eth4', 40)    # HR
        self.set_access(s4f3, 's4f3-eth5', 50)    # Reception
        self.set_access(s4f4, 's4f4-eth2', 120)   # VoIP
        self.set_access(s4f4, 's4f4-eth3', 100)   # Cameras

        # ================= TRUNK PORTS BETWEEN SWITCHES =================
        for link in net.links:
            node1 = link.intf1.node
            node2 = link.intf2.node

            if isinstance(node1, OVSSwitch) and isinstance(node2, OVSSwitch):
                self.set_trunk(node1, link.intf1.name, vlan_str)
                self.set_trunk(node2, link.intf2.name, vlan_str)

        # ================= L3 GATEWAYS ON CORE SWITCH =================
        gateways = {
            10: '10.20.10.1/27',
            20: '10.20.20.1/23',
            30: '10.20.30.1/26',
            40: '10.20.40.1/27',
            50: '10.20.50.1/28',
            60: '10.20.60.1/28',
            70: '10.20.70.1/26',
            100: '10.20.100.1/27',
            110: '10.20.110.1/26',
            120: '10.20.120.1/24',
            130: '10.20.130.1/27',
        }

        for vlan, ip in gateways.items():
            sp.cmd(
                f'ovs-vsctl add-port sp sp.{vlan} tag={vlan} '
                f'-- set interface sp.{vlan} type=internal'
            )
            sp.cmd(f'ip addr add {ip} dev sp.{vlan}')
            sp.cmd(f'ip link set sp.{vlan} up')

        # ================= ROUTING / SWITCHING =================
        sp.cmd('sysctl -w net.ipv4.ip_forward=1')
        sp.cmd('sysctl -w net.ipv4.conf.all.rp_filter=0')
        sp.cmd('sysctl -w net.ipv4.conf.default.rp_filter=0')
        sp.cmd('iptables -P FORWARD ACCEPT')
        sp.cmd('iptables -F FORWARD')

        # Force all switches to behave as normal learning switches
        for sw in net.switches:
            sw.cmd(f'ovs-vsctl set-fail-mode {sw.name} standalone')
            sw.cmd(f'ovs-ofctl del-flows {sw.name}')
            sw.cmd(f'ovs-ofctl add-flow {sw.name} priority=0,actions=NORMAL')

        print("\n*** Monterrey topology is ready.")
        print("*** Test same-VLAN:")
        print("    hf3eng1 ping -c3 hf4eng1")
        print("    hf3cam1 ping -c3 hf4cam1")
        print("    hf1rec1 ping -c3 hf2rec1")
        print("*** Test inter-VLAN:")
        print("    hf3eng1 ping -c3 hf3cam1")
        print("    hf4exec1 ping -c3 hf4hr1")
        print("    hf1guest1 ping -c3 hf1srv1")
        print("*** Test gateways:")
        print("    hf3eng1 ping -c3 10.20.20.1")
        print("    hf3cam1 ping -c3 10.20.100.1\n")

        CLI(net)
        net.stop()


def run():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink)
    site = Monterrey()
    site.build(net)


if __name__ == '__main__':
    setLogLevel('info')
    run()

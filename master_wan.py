from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

## Import our modular site topologies
from site_a import SiteA, Router
from site_b import SiteB

def build_master():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink)

    site_a = SiteA()
    site_b = SiteB()
    site_a.build(net)
    site_b.build(net)

    r2 = net.addHost('r2', cls=Router)
    r3 = net.addHost('r3', cls=Router)

    net.addLink(site_a.gateway,r2)
    net.addLink(site_a.gateway,r3)
    net.addLink(site_b.gateway,r2)
    net.addLink(site_b.gateway,r3)

    net.start()
    r1, r4 = site_a.gateway, site_b.gateway

    r1.setIP('172.16.1.1/30', intf='r1-eth1')
    r1.setIP('172.16.2.1/30', intf='r1-eth2')
    r4.setIP('172.16.1.6/30', intf='r4-eth1')
    r4.setIP('172.16.2.6/30', intf='r4-eth2')

    r2.setIP('172.16.1.2/30', intf='r2-eth0')
    r2.setIP('172.16.1.5/30', intf='r2-eth1')
    r3.setIP('172.16.2.2/30', intf='r3-eth0')
    r3.setIP('172.16.2.5/30', intf='r3-eth1')

    r2.cmd('ip route replace 10.0.1.0/24 nexthop via 172.16.1.1 dev r2-eth0')
    r2.cmd('ip route replace 10.0.2.0/24 nexthop via 172.16.1.6 dev r2-eth1')

    r3.cmd('ip route replace 10.0.1.0/24 nexthop via 172.16.2.1 dev r3-eth0')
    r3.cmd('ip route replace 10.0.2.0/24 nexthop via 172.16.2.6 dev r3-eth1')

    r1.cmd('ip route replace 10.0.2.0/24 nexthop via 172.16.1.2 dev r1-eth1 nexthop via 172.16.2.2 dev r1-eth2')
    r4.cmd('ip route replace 10.0.1.0/24 nexthop via 172.16.1.5 dev r4-eth1 nexthop via 172.16.2.5 dev r4-eth2')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    build_master()

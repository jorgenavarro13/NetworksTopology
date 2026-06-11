from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from illinois import Illinois
from saltillo import Saltillo

def build_master():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink, autoSetMacs=True)

    saltillo = Saltillo()
    saltillo.build(net)

    illinois = Illinois()
    illinois.build(net)

    net.addLink(
        illinois.gateway, saltillo.gateway,
        intfName1='illi-sal', intfName2='sal-illi',
        cls=TCLink
    )


    net.start()

    illinois.gateway.setIP('10.10.255.254/16', intf='illinois-eth0')
    saltillo.gateway.setIP('10.30.99.1/30',    intf='saltillo-eth0')
    illinois.gateway.setIP('192.168.100.1/30', intf='illi-sal')
    saltillo.gateway.setIP('192.168.100.2/30', intf='sal-illi')

    illinois.gateway.cmd('sysctl -w net.ipv4.ip_forward=1')
    saltillo.gateway.cmd('sysctl -w net.ipv4.ip_forward=1')

    saltillo.config(net)
    illinois.config(net)

    illinois.gateway.cmd('ip route add 10.30.0.0/16 via 192.168.100.2')
    saltillo.gateway.cmd('ip route add 10.10.0.0/16 via 192.168.100.1')

    saltillo.gateway.cmd('ip route add 10.30.20.0/25 via 10.30.99.2')
    saltillo.gateway.cmd('ip route add 10.30.50.0/27 via 10.30.99.2')
    saltillo.gateway.cmd('ip route add 10.30.130.0/24 via 10.30.99.2')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    build_master()


# ihf3eng1 ping -c 3 hSALf1eng1
# hSALf1eng1 ping -c 3 ihf3eng1
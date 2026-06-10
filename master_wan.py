from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

## Sites
from illinois import Illinois
from saltillo import Saltillo

def build_master():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink, autoSetMacs=True)

    saltillo = Saltillo()
    saltillo.build(net)

    illinois = Illinois()
    illinois.build()

    net.addLink(illinois.gateway, saltillo.gateway, intfName1='illi-sal', intfName2='sal-illi', cls=TCLink)

    net.start()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    build_master()

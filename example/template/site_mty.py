import os
from base_nodes import Router, SwitchL3

class SiteMTY:
    def __init__(self):
        self.gateway = None

    def build(self, net):
        self.gateway = net.addHost('rWANMTY', cls=Router)
        sCoreMTY = net.addSwitch('s10', cls=SwitchL3, failMode='standalone')
        hMTYs1 = net.addHost('hMTYs1', ip=None)

        net.addLink(sCoreMTY, self.gateway)
        net.addLink(sCoreMTY, hMTYs1)

    def config(self, net):
        self.gateway.setIP('10.1.99.1/30', intf='rWANMTY-eth0')
        self.gateway.cmd('ip route add 10.2.0.0/16 via 172.16.50.2')
        self.gateway.cmd('ip route add 10.1.100.0/24 via 10.1.99.2')

        sCoreMTY = net.get('s10')
        
        sCoreMTY.cmd('ovs-vsctl add-port s10 s10.vlan99 tag=99 -- set interface s10.vlan99 type=internal')
        sCoreMTY.cmd('ip addr add 10.1.99.2/30 dev s10.vlan99')
        sCoreMTY.cmd('ip link set s10.vlan99 up')

        # 3. Configure Server Subnet Gateway SVI (VLAN 100)
        sCoreMTY.cmd('ovs-vsctl add-port s10 s10.vlan100 tag=100 -- set interface s10.vlan100 type=internal')
        sCoreMTY.cmd('ip addr add 10.1.100.254/24 dev s10.vlan100')
        sCoreMTY.cmd('ip link set s10.vlan100 up')

        # 4. Map Physical Interfaces
        sCoreMTY.cmd('ovs-vsctl set port s10-eth1 tag=99')  # Untagged link to Router
        sCoreMTY.cmd('ovs-vsctl set port s10-eth2 tag=100') # Access link to DNS Server
        sCoreMTY.cmd('ip route add default via 10.1.99.1')

        # 5. Bring up DNS Server Daemon
        hMTYs1 = net.get('hMTYs1')
        hMTYs1.setIP('10.1.100.1/24')
        hMTYs1.setDefaultRoute('via 10.1.100.254')
        hMTYs1.cmd('dnsmasq -d --conf-file=./mty/site.conf --pid-file=/tmp/dnsmasq-mty.pid &')

        source_resolv = os.path.abspath('./mty/resolv.conf')
        hMTYs1.cmd('umount /etc/resolv.conf')
        hMTYs1.cmd('touch /etc/resolv.conf')
        hMTYs1.cmd(f'mount --bind {source_resolv} /etc/resolv.conf')
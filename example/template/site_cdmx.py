import os
from base_nodes import Router

class SiteCDMX:
    def __init__(self):
        self.gateway = None

    def build(self, net):
        self.gateway = net.addHost('rWANCDMX', cls=Router, ip=None)
        hCDMXc1 = net.addHost('hCDMXc1', ip=None)
        
        net.addLink(hCDMXc1, self.gateway)

    def config(self, net):
        self.gateway.setIP('10.2.0.254/24', intf='rWANCDMX-eth0')
        self.gateway.cmd('ip route add 10.1.0.0/16 via 172.16.50.1')

        hCDMXc1 = net.get('hCDMXc1')
        hCDMXc1.setIP('10.2.0.1/24')
        hCDMXc1.setDefaultRoute('via 10.2.0.254')

        source_resolv = os.path.abspath('./cdmx/resolv.conf')
        hCDMXc1.cmd('umount /etc/resolv.conf')
        hCDMXc1.cmd('touch /etc/resolv.conf')
        hCDMXc1.cmd(f'mount --bind {source_resolv} /etc/resolv.conf')
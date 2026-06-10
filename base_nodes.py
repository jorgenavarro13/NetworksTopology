from mininet.node import Node
from mininet.node import OVSSwitch

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
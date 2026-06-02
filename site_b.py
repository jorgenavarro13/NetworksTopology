from mininet.node import Node

class Router(Node):

    def config(self, **params):
        super(Router, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')
        self.cmd('sysctl net.ipv4.conf.all.rp_filter=0')
        self.cmd('sysctl net.ipv4.conf.default.rp_filter=0')


    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(Router, self).terminate()

class SiteB:
    def __init__(self):
        self.gateway = None
    
    def build (self,net):
        self.gateway = net.addHost('r4', cls=Router, ip='10.0.2.254/24' )

        s2 = net.addSwitch('s2', failMode='standalone')

        h1b = net.addHost('h1b', ip='10.0.2.10/24', defaultRoute='via 10.0.2.254')
        h2b = net.addHost('h2b', ip='10.0.2.20/24', defaultRoute='via 10.0.2.254')

        net.addLink(h1b, s2)
        net.addLink(h2b, s2)
        net.addLink(s2, self.gateway)
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

class SiteA:
    def __init__(self):
        self.gateway = None

    def build(self, net):
        self.gateway = net.addHost('r1', cls=Router, ip='10.0.1.254/24')

        s1 = net.addSwitch('s1', failMode='standalone')

        h1a = net.addHost('h1a', ip='10.0.1.10/24', defaultRoute='via 10.0.1.254')
        h2a = net.addHost('h2a', ip='10.0.1.20/24', defaultRoute='via 10.0.1.254')

        net.addLink(h1a, s1)
        net.addLink(h2a, s1)
        net.addLink(s1,self.gateway)
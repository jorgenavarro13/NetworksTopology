from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

# Saltillo site

# 1 Router
# 1 Core switch
# 3 Distribution switch
# 11 Access switches

from base_nodes import SwitchL3, Router

class Saltillo:
    def __init__(self):
        self.gateway = None

    def build(self, net):
        self.gateway = net.addHost('saltillo', cls=Router, ip='10.30.255.254/16')

        sSALc1 = net.addSwitch('sSALc1', cls=SwitchL3, failMode='standalone') # Core switch

        sSALd1 = net.addSwitch('sSALd1', failMode='standalone') ## Floor 1 & lobby
        sSALd2 = net.addSwitch('sSALd2', failMode='standalone') ## Floor 2 
        sSALd3 = net.addSwitch('sSALd3', failMode='standalone') ## Floor 3

        ## FLOOR 1
        #s_lpoe12 = net.addSwitch('sSALLlPoE12', failMode='standalone') ## Lobby PoE switch 
        sSALf11 = net.addSwitch('sSALf11',failMode='standalone') ## Floor 1 non-PoE 48P (1)
        sSALf12 = net.addSwitch('sSALf12',failMode='standalone') # Floor 1 Non-PoE 48P (2)
        sSALf13 = net.addSwitch('sSALf13', failMode='standalone') # Floor 1 PoE 48P
        
        ##FLOOR 2 
        sSALf21 = net.addSwitch('sSALf21', failMode='standalone') # Floor 2 Non-PoE 24P
        sSALf22 = net.addSwitch('sSALf22', failMode='standalone') # Floor 2 Non-PoE 48P (1)
        sSALf23 = net.addSwitch('sSALf23', failMode='standalone') # Floor 2 Non-PoE 48P (2)
        sSALf24 = net.addSwitch('sSALf24', failMode='standalone')  #Floor 2 PoE 12P

        
        ##FLOOR 3 
        sSALf31 = net.addSwitch('sSALf31', failMode='standalone') # Floor 3 Non-PoE 24P
        sSALf32 = net.addSwitch('sSALf32', failMode='standalone') # Floor 3 PoE 24P
        sSALf33 = net.addSwitch('sSALf33', failMode='standalone') # Floor 3 Non-PoE 48P

        #-Linking process
        
        net.addLink(self.gateway, sSALc1) # Core to router

        net.addLink(sSALc1, sSALd1) # Core to distribution
        net.addLink(sSALc1, sSALd2)
        net.addLink(sSALc1, sSALd3)

        #net.addLink(sSALDis1,sSALLlPoE12) # Distribution to access floor 1
        net.addLink(sSALd1,sSALf11)
        #net.addLink(sSALDis1,sSALLf1NPoE482)
        #net.addLink(sSALDis1,sSALLf1PoE48)

        #net.addLink(sSALDis2,sSALLf2poe12) # Distribution to access floor 2
        net.addLink(sSALd2,sSALf21)
        #net.addLink(sSALDis2,sSALLf2npoe481)
        #net.addLink(sSALDis2,sSALLf2npoe482)

        #net.addLink(sSALDis3,sSALLf3poe24) # Distribution to access floor 3
        net.addLink(sSALd3,sSALf31)
        #net.addLink(sSALDis3,sSALLf3npoe48)

        # Representative hosts

        ## Representative nodes engineering - VLAN 20
        hSALf1eng1 = net.addHost('hSALf1eng1', ip='10.30.20.10/25')                   
        hSALf2eng1 = net.addHost('hSALf2eng1', ip='10.30.20.20/25')
        hSALf3eng1 = net.addHost('hSALf3eng1', ip='10.30.20.30/25')

        ## Representative nodes reception  - VLAN 50        
        hSALf1rec1 = net.addHost('hSALf1rec1', ip='10.30.50.10/27')
        hSALf2rec1 = net.addHost('hSALf2rec1', ip='10.30.50.20/27')
        hSALf3rec1 = net.addHost('hSALf3rec1', ip='10.30.50.30/27')

        net.addLink(hSALf1eng1, sSALf11)
        net.addLink(hSALf2eng1, sSALf21)
        net.addLink(hSALf3eng1, sSALf31)
        net.addLink(hSALf1rec1, sSALf11)
        net.addLink(hSALf2rec1, sSALf21)
        net.addLink(hSALf3rec1, sSALf31)

        net.start()
        print("Saltillo site built successfully!")

        CLI(net)
        net.stop()


def run():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink)
    site = Saltillo()
    site.build(net)

if __name__ == '__main__':
    setLogLevel('info')
    run()

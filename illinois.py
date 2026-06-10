from base_nodes import Router, SwitchL3

from mininet.net import Mininet
from mininet.node import OVSSwitch, Node
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class Illinois:
    def __init__(self):
        self.gateway = None
    
    def build(self, net):
        #self.gateway = net.addHost('r1', cls=Router, ip='10.0.1.254/24')
        self.gateway = net.addHost('illinois', cls=Router, ip='10.10.255.254/16')

        s1 = net.addSwitch('s1', cls=SwitchL3, failMode='standalone')

        s2 = net.addSwitch('s2', failMode='standalone')
        s3 = net.addSwitch('s3', failMode='standalone')
        s4 = net.addSwitch('s4', failMode='standalone')
        s5 = net.addSwitch('s5', failMode='standalone')
        s6 = net.addSwitch('s6', failMode='standalone')
        s7 = net.addSwitch('s7', failMode='standalone')
        s8 = net.addSwitch('s8', failMode='standalone')


        ## FLOOR 1
        s9  = net.addSwitch('s9',    failMode='standalone')  ## Lobby PoE switch
        s10 = net.addSwitch('s10', failMode='standalone')  ## Floor 1 non-PoE 48P (1)
        s11 = net.addSwitch('s11', failMode='standalone')
        s12 = net.addSwitch('s12',   failMode='standalone')


        ## FLOOR 2
        s13  = net.addSwitch('s13',    failMode='standalone')  ## Lobby PoE switch
        s14 = net.addSwitch('s14', failMode='standalone')  ## Floor 1 non-PoE 48P (1)
        s15 = net.addSwitch('s15', failMode='standalone')
        s16 = net.addSwitch('s16',   failMode='standalone')

        ## FLOOR 3
        s17  = net.addSwitch('s17',    failMode='standalone')  ## Lobby PoE switch
        s18 = net.addSwitch('s18', failMode='standalone')  ## Floor 1 non-PoE 48P (1)
        s19 = net.addSwitch('s19', failMode='standalone')
        s20 = net.addSwitch('s20',   failMode='standalone')

        ## FLOOR 4
        s21  = net.addSwitch('s21',    failMode='standalone')  ## Lobby PoE switch
        s22 = net.addSwitch('s22', failMode='standalone')  ## Floor 1 non-PoE 48P (1)
        s23 = net.addSwitch('s23', failMode='standalone')
        s24 = net.addSwitch('s24',   failMode='standalone')

        ## FLOOR 5
        s25  = net.addSwitch('s25',    failMode='standalone')  ## Lobby PoE switch
        s26 = net.addSwitch('s26', failMode='standalone')  ## Floor 1 non-PoE 48P (1)
        s27 = net.addSwitch('s27', failMode='standalone')
        s28 = net.addSwitch('s28',   failMode='standalone')

        ## FLOOR 6
        s29  = net.addSwitch('s29',    failMode='standalone')  ## Lobby PoE switch
        s30 = net.addSwitch('s30', failMode='standalone')  ## Floor 1 non-PoE 48P (1)
        s31 = net.addSwitch('s31', failMode='standalone')
        s32 = net.addSwitch('s32',   failMode='standalone')
        s33 = net.addSwitch('s33',   failMode='standalone')

        ## FLOOR 7
        s34  = net.addSwitch('s34',    failMode='standalone')  ## Lobby PoE switch
        s35 = net.addSwitch('s35', failMode='standalone')  ## Floor 1 non-PoE 48P (1)
        s36 = net.addSwitch('s36', failMode='standalone')

        ############# Linking process ##########################

        net.addLink(self.gateway, s1) # illinois-eth0 <--> s1-eth1

        net.addLink(s1, s2) # s1-eth2 <--> s2-eth1
        net.addLink(s1, s3) # s1-eth3 <--> s3-eth1
        net.addLink(s1, s4) # s1-eth4 <--> s4-eth1
        net.addLink(s1, s5) # s1-eth5 <--> s5-eth1
        net.addLink(s1, s6) # s1-eth6 <--> s6-eth1
        net.addLink(s1, s7) # s1-eth7 <--> s7-eth1
        net.addLink(s1, s8) # s1-eth8 <--> s8-eth1

        net.addLink(s2, s9)  # s2-eth2 <--> s9-eth1
        net.addLink(s2, s10) # s2-eth3 <--> s10-eth1
        net.addLink(s2, s11) # s2-eth4 <--> s11-eth1
        net.addLink(s2, s12) # s2-eth5 <--> s12-eth1

        net.addLink(s3, s13) # s3-eth2 <--> s13-eth1
        net.addLink(s3, s14) # s3-eth3 <--> s14-eth1
        net.addLink(s3, s15) # s3-eth4 <--> s15-eth1
        net.addLink(s3, s16) # s3-eth5 <--> s16-eth1

        net.addLink(s4, s17) # s4-eth2 <--> s17-eth1
        net.addLink(s4, s18) # s4-eth3 <--> s18-eth1
        net.addLink(s4, s19) # s4-eth4 <--> s19-eth1
        net.addLink(s4, s20) # s4-eth5 <--> s20-eth1

        net.addLink(s5, s21) # s5-eth2 <--> s21-eth1
        net.addLink(s5, s22) # s5-eth3 <--> s22-eth1
        net.addLink(s5, s23) # s5-eth4 <--> s23-eth1
        net.addLink(s5, s24) # s5-eth5 <--> s24-eth1

        net.addLink(s6, s25) # s6-eth2 <--> s25-eth1
        net.addLink(s6, s26) # s6-eth3 <--> s26-eth1
        net.addLink(s6, s27) # s6-eth4 <--> s27-eth1
        net.addLink(s6, s28) # s6-eth5 <--> s28-eth1

        net.addLink(s7, s29) # s7-eth2 <--> s29-eth1
        net.addLink(s7, s30) # s7-eth3 <--> s30-eth1
        net.addLink(s7, s31) # s7-eth4 <--> s31-eth1
        net.addLink(s7, s32) # s7-eth5 <--> s32-eth1
        net.addLink(s7, s33) # s7-eth6 <--> s33-eth1

        net.addLink(s8, s34) # s8-eth2 <--> s34-eth1
        net.addLink(s8, s35) # s8-eth3 <--> s35-eth1
        net.addLink(s8, s36) # s8-eth4 <--> s36-eth1


        ######### Adding representative hosts #########################
        
        ## Representative nodes executives - VLAN 10
        ihf7exe1 = net.addHost('ihf7exe1', ip='10.10.10.10/25', defaultRoute='via 10.10.255.254')
        ihf7exe2 = net.addHost('ihf7exe2', ip='10.10.10.50/25', defaultRoute='via 10.10.255.254')

        net.addLink(ihf7exe1, s34) # ihf7exe1-eth0 <--> s34-eth2
        net.addLink(ihf7exe2, s35) # ihf7exe2-eth0 <--> s35-eth2

        ## Representative nodes engineering - VLAN 20
        ihf3eng1 = net.addHost('ihf3eng1', ip='10.10.20.30/23', defaultRoute='via 10.10.255.254')
        ihf4eng1 = net.addHost('ihf4eng1', ip='10.10.20.40/23', defaultRoute='via 10.10.255.254')
        ihf5eng1 = net.addHost('ihf5eng1', ip='10.10.20.50/23', defaultRoute='via 10.10.255.254')
        
        ihf3eng2 = net.addHost('ihf3eng2', ip='10.10.20.110/23', defaultRoute='via 10.10.255.254')
        ihf4eng2 = net.addHost('ihf4eng2', ip='10.10.20.120/23', defaultRoute='via 10.10.255.254')
        ihf5eng2 = net.addHost('ihf5eng2', ip='10.10.20.130/23', defaultRoute='via 10.10.255.254')

        ihf3eng3 = net.addHost('ihf3eng3', ip='10.10.20.210/23', defaultRoute='via 10.10.255.254')
        ihf4eng3 = net.addHost('ihf4eng3', ip='10.10.20.220/23', defaultRoute='via 10.10.255.254')
        ihf5eng3 = net.addHost('ihf5eng3', ip='10.10.20.230/23', defaultRoute='via 10.10.255.254')

        net.addLink(ihf3eng1, s17) # ihf3eng1-eth0 <--> s17-eth2
        net.addLink(ihf4eng1, s21) # ihf4eng1-eth0 <--> s21-eth2
        net.addLink(ihf5eng1, s25) # ihf5eng1-eth0 <--> s25-eth2

        net.addLink(ihf3eng2, s18) # ihf3eng2-eth0 <--> s18-eth2
        net.addLink(ihf4eng2, s22) # ihf4eng2-eth0 <--> s22-eth2
        net.addLink(ihf5eng2, s26) # ihf5eng2-eth0 <--> s26-eth2

        net.addLink(ihf3eng3, s19) # ihf3eng3-eth0 <--> s19-eth2
        net.addLink(ihf4eng3, s23) # ihf4eng3-eth0 <--> s23-eth2
        net.addLink(ihf5eng3, s27) # ihf5eng3-eth0 <--> s27-eth2

        ## Representative nodes IoT Labs - VLAN 30
        ihf2iot1 = net.addHost('ihf2iot1', ip='10.10.30.10/25', defaultRoute='via 10.10.255.254')
        ihf2iot2 = net.addHost('ihf2iot2', ip='10.10.30.20/25', defaultRoute='via 10.10.255.254')
        ihf2iot3 = net.addHost('ihf2iot3', ip='10.10.30.90/25', defaultRoute='via 10.10.255.254')

        net.addLink(ihf2iot1, s13) # ihf2iot1-eth0 <--> s13-eth2
        net.addLink(ihf2iot2, s14) # ihf2iot2-eth0 <--> s14-eth2
        net.addLink(ihf2iot3, s15) # ihf2iot3-eth0 <--> s15-eth2

        ## Representative nodes HR - VLAN 40
        ihf6hr1 = net.addHost('ihf6hr1', ip='10.10.40.10/25', defaultRoute='via 10.10.255.254')
        ihf6hr2 = net.addHost('ihf6hr2', ip='10.10.40.50/25', defaultRoute='via 10.10.255.254')
        ihf6hr3 = net.addHost('ihf6hr3', ip='10.10.40.100/25', defaultRoute='via 10.10.255.254')

        net.addLink(ihf6hr1, s30) # ihf6hr1-eth0 <--> s30-eth2
        net.addLink(ihf6hr2, s31) # ihf6hr2-eth0 <--> s31-eth2
        net.addLink(ihf6hr3, s32) # ihf6hr3-eth0 <--> s32-eth2

        ## Representative nodes Reception - VLAN 50
        ihf1rec1 = net.addHost('ihf1rec1', ip='10.10.50.5/26', defaultRoute='via 10.10.255.254')
        ihf2rec1 = net.addHost('ihf2rec1', ip='10.10.50.15/26', defaultRoute='via 10.10.255.254')
        ihf3rec1 = net.addHost('ihf3rec1', ip='10.10.50.22/26', defaultRoute='via 10.10.255.254')
        ihf4rec1 = net.addHost('ihf4rec1', ip='10.10.50.28/26', defaultRoute='via 10.10.255.254')
        ihf5rec1 = net.addHost('ihf5rec1', ip='10.10.50.34/26', defaultRoute='via 10.10.255.254')
        ihf6rec1 = net.addHost('ihf6rec1', ip='10.10.50.40/26', defaultRoute='via 10.10.255.254')
        ihf7rec1 = net.addHost('ihf7rec1', ip='10.10.50.46/26', defaultRoute='via 10.10.255.254')

        net.addLink(ihf1rec1, s9)  # ihf1rec1-eth0 <--> s9-eth2
        net.addLink(ihf2rec1, s13) # ihf2rec1-eth0 <--> s13-eth3
        net.addLink(ihf3rec1, s17) # ihf3rec1-eth0 <--> s17-eth3
        net.addLink(ihf4rec1, s21) # ihf4rec1-eth0 <--> s21-eth3
        net.addLink(ihf5rec1, s25) # ihf5rec1-eth0 <--> s25-eth3
        net.addLink(ihf6rec1, s29) # ihf6rec1-eth0 <--> s29-eth2
        net.addLink(ihf7rec1, s34) # ihf7rec1-eth0 <--> s34-eth3

        ## Representative nodes print servers - VLAN 60
        ihf7ps1 = net.addHost('ihf7ps1', ip='10.10.60.5/27', defaultRoute='via 10.10.255.254')
        ihf6ps1 = net.addHost('ihf6ps1', ip='10.10.60.12/27', defaultRoute='via 10.10.255.254')
        ihf2ps1 = net.addHost('ihf2ps1', ip='10.10.60.20/27', defaultRoute='via 10.10.255.254')
        ihf1ps1 = net.addHost('ihf1ps1', ip='10.10.60.27/27', defaultRoute='via 10.10.255.254')

        net.addLink(ihf7ps1, s11) # ihf7ps1-eth0 <--> s11-eth2
        net.addLink(ihf6ps1, s15) # ihf6ps1-eth0 <--> s15-eth3
        net.addLink(ihf2ps1, s29) # ihf2ps1-eth0 <--> s29-eth3
        net.addLink(ihf1ps1, s35) # ihf1ps1-eth0 <--> s35-eth3

        ## Representative nodes meeting rooms - VLAN 70
        ihf7mr1 = net.addHost('ihf7mr1', ip='10.10.70.10/26', defaultRoute='via 10.10.255.254')
        ihf6mr1 = net.addHost('ihf6mr1', ip='10.10.70.20/26', defaultRoute='via 10.10.255.254')
        ihf4mr1 = net.addHost('ihf4mr1', ip='10.10.70.30/26', defaultRoute='via 10.10.255.254')
        ihf2mr1 = net.addHost('ihf2mr1', ip='10.10.70.40/26', defaultRoute='via 10.10.255.254')
        ihf1mr1 = net.addHost('ihf1mr1', ip='10.10.70.50/26', defaultRoute='via 10.10.255.254')

        net.addLink(ihf7mr1, s11) # ihf7mr1-eth0 <--> s11-eth3
        net.addLink(ihf6mr1, s15) # ihf6mr1-eth0 <--> s15-eth4
        net.addLink(ihf4mr1, s23) # ihf4mr1-eth0 <--> s23-eth3
        net.addLink(ihf2mr1, s32) # ihf2mr1-eth0 <--> s32-eth3
        net.addLink(ihf1mr1, s35) # ihf1mr1-eth0 <--> s35-eth4

        ## Representative nodes cameras - VLAN 100
        ihf1cm1 = net.addHost('ihf1cm1', ip='10.10.100.10/25', defaultRoute='via 10.10.255.254')
        ihf2cm1 = net.addHost('ihf2cm1', ip='10.10.100.20/25', defaultRoute='via 10.10.255.254')
        ihf3cm1 = net.addHost('ihf3cm1', ip='10.10.100.30/25', defaultRoute='via 10.10.255.254')
        ihf4cm1 = net.addHost('ihf4cm1', ip='10.10.100.40/25', defaultRoute='via 10.10.255.254')
        ihf5cm1 = net.addHost('ihf5cm1', ip='10.10.100.50/25', defaultRoute='via 10.10.255.254')
        ihf6cm1 = net.addHost('ihf6cm1', ip='10.10.100.60/25', defaultRoute='via 10.10.255.254')
        ihf7cm1 = net.addHost('ihf7cm1', ip='10.10.100.70/25', defaultRoute='via 10.10.255.254')

        net.addLink(ihf1cm1,  s12) # ihf1cm1-eth0  <--> s12-eth2
        net.addLink(ihf2cm1,  s16) # ihf2cm1-eth0  <--> s16-eth2
        net.addLink(ihf3cm1,  s20) # ihf3cm1-eth0  <--> s20-eth2
        net.addLink(ihf4cm1,  s24) # ihf4cm1-eth0  <--> s24-eth2
        net.addLink(ihf5cm1,  s28) # ihf5cm1-eth0  <--> s28-eth2
        net.addLink(ihf6cm1,  s33) # ihf6cm1-eth0  <--> s33-eth2
        net.addLink(ihf7cm1,  s36) # ihf7cm1-eth0  <--> s36-eth2

        ## Representative nodes guests - VLAN 110
        ihf1gs1 = net.addHost('ihf1gs1', ip='10.10.110.10/25', defaultRoute='via 10.10.255.254')
        ihf1gs2 = net.addHost('ihf1gs2', ip='10.10.110.50/25', defaultRoute='via 10.10.255.254')
        ihf6gs1 = net.addHost('ihf6gs1', ip='10.10.110.110/25', defaultRoute='via 10.10.255.254')

        net.addLink(ihf1gs1, s9)  # ihf1gs1-eth0 <--> s9-eth3
        net.addLink(ihf1gs2, s10) # ihf1gs2-eth0 <--> s10-eth2
        net.addLink(ihf6gs1, s29) # ihf6gs1-eth0 <--> s29-eth3

        ## Representative nodes voip - VLAN 120
        ihf1voip1 = net.addHost('ihf1voip1', ip='10.10.120.10/25', defaultRoute='via 10.10.255.254')
        ihf2voip1 = net.addHost('ihf2voip1', ip='10.10.120.20/25', defaultRoute='via 10.10.255.254')
        ihf3voip1 = net.addHost('ihf3voip1', ip='10.10.120.30/25', defaultRoute='via 10.10.255.254')
        ihf4voip1 = net.addHost('ihf4voip1', ip='10.10.120.40/25', defaultRoute='via 10.10.255.254')
        ihf5voip1 = net.addHost('ihf5voip1', ip='10.10.120.50/25', defaultRoute='via 10.10.255.254')
        ihf6voip1 = net.addHost('ihf6voip1', ip='10.10.120.60/25', defaultRoute='via 10.10.255.254')
        ihf7voip1 = net.addHost('ihf7voip1', ip='10.10.120.70/25', defaultRoute='via 10.10.255.254')

        net.addLink(ihf1voip1, s12) # ihf1voip1-eth0 <--> s12-eth3
        net.addLink(ihf2voip1, s16) # ihf2voip1-eth0 <--> s16-eth3
        net.addLink(ihf3voip1, s20) # ihf3voip1-eth0 <--> s20-eth3
        net.addLink(ihf4voip1, s24) # ihf4voip1-eth0 <--> s24-eth3
        net.addLink(ihf5voip1, s28) # ihf5voip1-eth0 <--> s28-eth3
        net.addLink(ihf6voip1, s33) # ihf6voip1-eth0 <--> s33-eth3
        net.addLink(ihf7voip1, s36) # ihf7voip1-eth0 <--> s36-eth3

        ## Representative nodes servers - VLAN 130
        ihf1sr1 = net.addHost('ihf1sr1', ip='10.10.130.10/26', defaultRoute='via 10.10.255.254')
        ihf1sr2 = net.addHost('ihf1sr2', ip='10.10.130.50/26', defaultRoute='via 10.10.255.254')

        net.addLink(ihf1sr1, s10) # ihf1sr1-eth0 <--> s10-eth3
        net.addLink(ihf1sr2, s11) # ihf1sr2-eth0 <--> s11-eth4


        net.start()
        CLI(net, script='commands.txt')
        #CLI(net)
        net.stop()

def run():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink)
    site = Illinois()
    site.build(net)


if __name__ == '__main__':
    setLogLevel('info')
    run()
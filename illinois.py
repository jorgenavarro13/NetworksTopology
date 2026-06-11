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
        self.gateway = net.addHost('illinois',cls=Router)

        s1 = net.addSwitch('s1', cls=SwitchL3, failMode='standalone')

        s2  = net.addSwitch('s2',  failMode='standalone')
        s3  = net.addSwitch('s3',  failMode='standalone')
        s4  = net.addSwitch('s4',  failMode='standalone')
        s5  = net.addSwitch('s5',  failMode='standalone')
        s6  = net.addSwitch('s6',  failMode='standalone')
        s7  = net.addSwitch('s7',  failMode='standalone')
        s8  = net.addSwitch('s8',  failMode='standalone')

        ## FLOOR 1
        s9  = net.addSwitch('s9',  failMode='standalone')
        s10 = net.addSwitch('s10', failMode='standalone')
        s11 = net.addSwitch('s11', failMode='standalone')
        s12 = net.addSwitch('s12', failMode='standalone')

        ## FLOOR 2
        s13 = net.addSwitch('s13', failMode='standalone')
        s14 = net.addSwitch('s14', failMode='standalone')
        s15 = net.addSwitch('s15', failMode='standalone')
        s16 = net.addSwitch('s16', failMode='standalone')

        ## FLOOR 3
        s17 = net.addSwitch('s17', failMode='standalone')
        s18 = net.addSwitch('s18', failMode='standalone')
        s19 = net.addSwitch('s19', failMode='standalone')
        s20 = net.addSwitch('s20', failMode='standalone')

        ## FLOOR 4
        s21 = net.addSwitch('s21', failMode='standalone')
        s22 = net.addSwitch('s22', failMode='standalone')
        s23 = net.addSwitch('s23', failMode='standalone')
        s24 = net.addSwitch('s24', failMode='standalone')

        ## FLOOR 5
        s25 = net.addSwitch('s25', failMode='standalone')
        s26 = net.addSwitch('s26', failMode='standalone')
        s27 = net.addSwitch('s27', failMode='standalone')
        s28 = net.addSwitch('s28', failMode='standalone')

        ## FLOOR 6
        s29 = net.addSwitch('s29', failMode='standalone')
        s30 = net.addSwitch('s30', failMode='standalone')
        s31 = net.addSwitch('s31', failMode='standalone')
        s32 = net.addSwitch('s32', failMode='standalone')
        s33 = net.addSwitch('s33', failMode='standalone')

        ## FLOOR 7
        s34 = net.addSwitch('s34', failMode='standalone')
        s35 = net.addSwitch('s35', failMode='standalone')
        s36 = net.addSwitch('s36', failMode='standalone')

        ############# Linking process ##########################

        net.addLink(self.gateway, s1)  # illinois-eth0 <--> s1-eth1

        net.addLink(s1, s2)  # s1-eth2 <--> s2-eth1
        net.addLink(s1, s3)  # s1-eth3 <--> s3-eth1
        net.addLink(s1, s4)  # s1-eth4 <--> s4-eth1
        net.addLink(s1, s5)  # s1-eth5 <--> s5-eth1
        net.addLink(s1, s6)  # s1-eth6 <--> s6-eth1
        net.addLink(s1, s7)  # s1-eth7 <--> s7-eth1
        net.addLink(s1, s8)  # s1-eth8 <--> s8-eth1

        net.addLink(s2, s9)   # s2-eth2 <--> s9-eth1
        net.addLink(s2, s10)  # s2-eth3 <--> s10-eth1
        net.addLink(s2, s11)  # s2-eth4 <--> s11-eth1
        net.addLink(s2, s12)  # s2-eth5 <--> s12-eth1

        net.addLink(s3, s13)  # s3-eth2 <--> s13-eth1
        net.addLink(s3, s14)  # s3-eth3 <--> s14-eth1
        net.addLink(s3, s15)  # s3-eth4 <--> s15-eth1
        net.addLink(s3, s16)  # s3-eth5 <--> s16-eth1

        net.addLink(s4, s17)  # s4-eth2 <--> s17-eth1
        net.addLink(s4, s18)  # s4-eth3 <--> s18-eth1
        net.addLink(s4, s19)  # s4-eth4 <--> s19-eth1
        net.addLink(s4, s20)  # s4-eth5 <--> s20-eth1

        net.addLink(s5, s21)  # s5-eth2 <--> s21-eth1
        net.addLink(s5, s22)  # s5-eth3 <--> s22-eth1
        net.addLink(s5, s23)  # s5-eth4 <--> s23-eth1
        net.addLink(s5, s24)  # s5-eth5 <--> s24-eth1

        net.addLink(s6, s25)  # s6-eth2 <--> s25-eth1
        net.addLink(s6, s26)  # s6-eth3 <--> s26-eth1
        net.addLink(s6, s27)  # s6-eth4 <--> s27-eth1
        net.addLink(s6, s28)  # s6-eth5 <--> s28-eth1

        net.addLink(s7, s29)  # s7-eth2 <--> s29-eth1
        net.addLink(s7, s30)  # s7-eth3 <--> s30-eth1
        net.addLink(s7, s31)  # s7-eth4 <--> s31-eth1
        net.addLink(s7, s32)  # s7-eth5 <--> s32-eth1
        net.addLink(s7, s33)  # s7-eth6 <--> s33-eth1

        net.addLink(s8, s34)  # s8-eth2 <--> s34-eth1
        net.addLink(s8, s35)  # s8-eth3 <--> s35-eth1
        net.addLink(s8, s36)  # s8-eth4 <--> s36-eth1

        ######### Adding representative hosts #########################

        ## Executives - VLAN 10
        ihf7exe1 = net.addHost('ihf7exe1', ip='10.10.10.10/25')
        ihf7exe2 = net.addHost('ihf7exe2', ip='10.10.10.50/25')
        net.addLink(ihf7exe1, s34)
        net.addLink(ihf7exe2, s35)

        ## Engineering - VLAN 20
        ihf3eng1 = net.addHost('ihf3eng1', ip='10.10.20.30/23')
        ihf4eng1 = net.addHost('ihf4eng1', ip='10.10.20.40/23')
        ihf5eng1 = net.addHost('ihf5eng1', ip='10.10.20.50/23')
        ihf3eng2 = net.addHost('ihf3eng2', ip='10.10.20.110/23')
        ihf4eng2 = net.addHost('ihf4eng2', ip='10.10.20.120/23')
        ihf5eng2 = net.addHost('ihf5eng2', ip='10.10.20.130/23')
        ihf3eng3 = net.addHost('ihf3eng3', ip='10.10.20.210/23')
        ihf4eng3 = net.addHost('ihf4eng3', ip='10.10.20.220/23')
        ihf5eng3 = net.addHost('ihf5eng3', ip='10.10.20.230/23')
        net.addLink(ihf3eng1, s17)
        net.addLink(ihf4eng1, s21)
        net.addLink(ihf5eng1, s25)
        net.addLink(ihf3eng2, s18)
        net.addLink(ihf4eng2, s22)
        net.addLink(ihf5eng2, s26)
        net.addLink(ihf3eng3, s19)
        net.addLink(ihf4eng3, s23)
        net.addLink(ihf5eng3, s27)

        ## IoT Labs - VLAN 30
        ihf2iot1 = net.addHost('ihf2iot1', ip='10.10.30.10/25')
        ihf2iot2 = net.addHost('ihf2iot2', ip='10.10.30.20/25')
        ihf2iot3 = net.addHost('ihf2iot3', ip='10.10.30.90/25')
        net.addLink(ihf2iot1, s13)
        net.addLink(ihf2iot2, s14)
        net.addLink(ihf2iot3, s15)

        ## HR - VLAN 40
        ihf6hr1 = net.addHost('ihf6hr1', ip='10.10.40.10/25')
        ihf6hr2 = net.addHost('ihf6hr2', ip='10.10.40.50/25')
        ihf6hr3 = net.addHost('ihf6hr3', ip='10.10.40.100/25')
        net.addLink(ihf6hr1, s30)
        net.addLink(ihf6hr2, s31)
        net.addLink(ihf6hr3, s32)

        ## Reception - VLAN 50
        ihf1rec1 = net.addHost('ihf1rec1', ip='10.10.50.5/26')
        ihf2rec1 = net.addHost('ihf2rec1', ip='10.10.50.15/26')
        ihf3rec1 = net.addHost('ihf3rec1', ip='10.10.50.22/26')
        ihf4rec1 = net.addHost('ihf4rec1', ip='10.10.50.28/26')
        ihf5rec1 = net.addHost('ihf5rec1', ip='10.10.50.34/26')
        ihf6rec1 = net.addHost('ihf6rec1', ip='10.10.50.40/26')
        ihf7rec1 = net.addHost('ihf7rec1', ip='10.10.50.46/26')
        net.addLink(ihf1rec1, s9)
        net.addLink(ihf2rec1, s13)
        net.addLink(ihf3rec1, s17)
        net.addLink(ihf4rec1, s21)
        net.addLink(ihf5rec1, s25)
        net.addLink(ihf6rec1, s29)
        net.addLink(ihf7rec1, s34)

        ## Print servers - VLAN 60
        ihf7ps1 = net.addHost('ihf7ps1', ip='10.10.60.5/27')
        ihf6ps1 = net.addHost('ihf6ps1', ip='10.10.60.12/27')
        ihf2ps1 = net.addHost('ihf2ps1', ip='10.10.60.20/27')
        ihf1ps1 = net.addHost('ihf1ps1', ip='10.10.60.27/27')
        net.addLink(ihf7ps1, s11)
        net.addLink(ihf6ps1, s15)
        net.addLink(ihf2ps1, s29)
        net.addLink(ihf1ps1, s35)

        ## Meeting rooms - VLAN 70
        ihf7mr1 = net.addHost('ihf7mr1', ip='10.10.70.10/26')
        ihf6mr1 = net.addHost('ihf6mr1', ip='10.10.70.20/26')
        ihf4mr1 = net.addHost('ihf4mr1', ip='10.10.70.30/26')
        ihf2mr1 = net.addHost('ihf2mr1', ip='10.10.70.40/26')
        ihf1mr1 = net.addHost('ihf1mr1', ip='10.10.70.50/26')
        net.addLink(ihf7mr1, s11)
        net.addLink(ihf6mr1, s15)
        net.addLink(ihf4mr1, s23)
        net.addLink(ihf2mr1, s32)
        net.addLink(ihf1mr1, s35)

        ## Cameras - VLAN 100
        ihf1cm1 = net.addHost('ihf1cm1', ip='10.10.100.10/25')
        ihf2cm1 = net.addHost('ihf2cm1', ip='10.10.100.20/25')
        ihf3cm1 = net.addHost('ihf3cm1', ip='10.10.100.30/25')
        ihf4cm1 = net.addHost('ihf4cm1', ip='10.10.100.40/25')
        ihf5cm1 = net.addHost('ihf5cm1', ip='10.10.100.50/25')
        ihf6cm1 = net.addHost('ihf6cm1', ip='10.10.100.60/25')
        ihf7cm1 = net.addHost('ihf7cm1', ip='10.10.100.70/25')
        net.addLink(ihf1cm1, s12)
        net.addLink(ihf2cm1, s16)
        net.addLink(ihf3cm1, s20)
        net.addLink(ihf4cm1, s24)
        net.addLink(ihf5cm1, s28)
        net.addLink(ihf6cm1, s33)
        net.addLink(ihf7cm1, s36)

        ## Guests - VLAN 110
        ihf1gs1 = net.addHost('ihf1gs1', ip='10.10.110.10/25')
        ihf1gs2 = net.addHost('ihf1gs2', ip='10.10.110.50/25')
        ihf6gs1 = net.addHost('ihf6gs1', ip='10.10.110.110/25')
        net.addLink(ihf1gs1, s9)
        net.addLink(ihf1gs2, s10)
        net.addLink(ihf6gs1, s29)

        ## VoIP - VLAN 120
        ihf1voip1 = net.addHost('ihf1voip1', ip='10.10.120.10/25')
        ihf2voip1 = net.addHost('ihf2voip1', ip='10.10.120.20/25')
        ihf3voip1 = net.addHost('ihf3voip1', ip='10.10.120.30/25')
        ihf4voip1 = net.addHost('ihf4voip1', ip='10.10.120.40/25')
        ihf5voip1 = net.addHost('ihf5voip1', ip='10.10.120.50/25')
        ihf6voip1 = net.addHost('ihf6voip1', ip='10.10.120.60/25')
        ihf7voip1 = net.addHost('ihf7voip1', ip='10.10.120.70/25')
        net.addLink(ihf1voip1, s12)
        net.addLink(ihf2voip1, s16)
        net.addLink(ihf3voip1, s20)
        net.addLink(ihf4voip1, s24)
        net.addLink(ihf5voip1, s28)
        net.addLink(ihf6voip1, s33)
        net.addLink(ihf7voip1, s36)

        ## Servers - VLAN 130
        ihf1sr1 = net.addHost('ihf1sr1', ip='10.10.130.10/26')
        ihf1sr2 = net.addHost('ihf1sr2', ip='10.10.130.50/26')
        net.addLink(ihf1sr1, s10)
        net.addLink(ihf1sr2, s11)
        
        print("Illinois site built successfully!")

    def config(self, net):
        s1  = net.get('s1')

        s2  = net.get('s2')
        s3  = net.get('s3')
        s4  = net.get('s4')
        s5  = net.get('s5')
        s6  = net.get('s6')
        s7  = net.get('s7')
        s8  = net.get('s8')

        # FLOOR 1
        s9  = net.get('s9')
        s10 = net.get('s10')
        s11 = net.get('s11')
        s12 = net.get('s12')

        # FLOOR 2
        s13 = net.get('s13')
        s14 = net.get('s14')
        s15 = net.get('s15')
        s16 = net.get('s16')

        # FLOOR 3
        s17 = net.get('s17')
        s18 = net.get('s18')
        s19 = net.get('s19')
        s20 = net.get('s20')

        # FLOOR 4
        s21 = net.get('s21')
        s22 = net.get('s22')
        s23 = net.get('s23')
        s24 = net.get('s24')

        # FLOOR 5
        s25 = net.get('s25')
        s26 = net.get('s26')
        s27 = net.get('s27')
        s28 = net.get('s28')

        # FLOOR 6
        s29 = net.get('s29')
        s30 = net.get('s30')
        s31 = net.get('s31')
        s32 = net.get('s32')
        s33 = net.get('s33')

        # FLOOR 7
        s34 = net.get('s34')
        s35 = net.get('s35')
        s36 = net.get('s36')

        # ── Gateway (WAN router) ──────────────────────────────────────
        self.gateway.setIP('10.10.99.1/30', intf='illinois-eth0')
        self.gateway.cmd('ip route add 10.10.0.0/16 via 10.10.99.2')

        # VLAN 99 – p2p uplink to gateway
        s1.cmd('ovs-vsctl add-port s1 s1.v99 tag=99 -- set interface s1.v99 type=internal')
        s1.cmd('ip addr add 10.10.99.2/30 dev s1.v99 && ip link set s1.v99 up')

        # VLAN 10 – Executives
        s1.cmd('ovs-vsctl add-port s1 s1.v10 tag=10 -- set interface s1.v10 type=internal')
        s1.cmd('ip addr add 10.10.10.1/25 dev s1.v10 && ip link set s1.v10 up')

        # VLAN 20 – Engineering
        s1.cmd('ovs-vsctl add-port s1 s1.v20 tag=20 -- set interface s1.v20 type=internal')
        s1.cmd('ip addr add 10.10.20.1/23 dev s1.v20 && ip link set s1.v20 up')

        # VLAN 30 – IoT Labs
        s1.cmd('ovs-vsctl add-port s1 s1.v30 tag=30 -- set interface s1.v30 type=internal')
        s1.cmd('ip addr add 10.10.30.1/25 dev s1.v30 && ip link set s1.v30 up')

        # VLAN 40 – HR
        s1.cmd('ovs-vsctl add-port s1 s1.v40 tag=40 -- set interface s1.v40 type=internal')
        s1.cmd('ip addr add 10.10.40.1/25 dev s1.v40 && ip link set s1.v40 up')

        # VLAN 50 – Reception
        s1.cmd('ovs-vsctl add-port s1 s1.v50 tag=50 -- set interface s1.v50 type=internal')
        s1.cmd('ip addr add 10.10.50.1/26 dev s1.v50 && ip link set s1.v50 up')

        # VLAN 60 – Print Servers
        s1.cmd('ovs-vsctl add-port s1 s1.v60 tag=60 -- set interface s1.v60 type=internal')
        s1.cmd('ip addr add 10.10.60.1/27 dev s1.v60 && ip link set s1.v60 up')

        # VLAN 70 – Meeting Rooms
        s1.cmd('ovs-vsctl add-port s1 s1.v70 tag=70 -- set interface s1.v70 type=internal')
        s1.cmd('ip addr add 10.10.70.1/26 dev s1.v70 && ip link set s1.v70 up')

        # VLAN 100 – Cameras
        s1.cmd('ovs-vsctl add-port s1 s1.v100 tag=100 -- set interface s1.v100 type=internal')
        s1.cmd('ip addr add 10.10.100.1/25 dev s1.v100 && ip link set s1.v100 up')

        # VLAN 110 – Guests
        s1.cmd('ovs-vsctl add-port s1 s1.v110 tag=110 -- set interface s1.v110 type=internal')
        s1.cmd('ip addr add 10.10.110.1/25 dev s1.v110 && ip link set s1.v110 up')

        # VLAN 120 – VoIP
        s1.cmd('ovs-vsctl add-port s1 s1.v120 tag=120 -- set interface s1.v120 type=internal')
        s1.cmd('ip addr add 10.10.120.1/25 dev s1.v120 && ip link set s1.v120 up')

        # VLAN 130 – Servers
        s1.cmd('ovs-vsctl add-port s1 s1.v130 tag=130 -- set interface s1.v130 type=internal')
        s1.cmd('ip addr add 10.10.130.254/26 dev s1.v130 && ip link set s1.v130 up')

        # Default route hacia el gateway WAN
        s1.cmd('ip route add default via 10.10.99.1')
        

        # ── Core switch: port assignments ─────────────────────────────
        # enlace al gateway
        s1.cmd('ovs-vsctl set port s1-eth1 tag=99')
        # uplinks a distribución
        s1.cmd('ovs-vsctl set port s1-eth2 trunks=50,60,70,100,110,120,130')
        s1.cmd('ovs-vsctl set port s1-eth3 trunks=30,50,60,70,100,120')
        s1.cmd('ovs-vsctl set port s1-eth4 trunks=20,50,100,120')
        s1.cmd('ovs-vsctl set port s1-eth5 trunks=20,50,70,100,120')
        s1.cmd('ovs-vsctl set port s1-eth6 trunks=20,50,100,120')
        s1.cmd('ovs-vsctl set port s1-eth7 trunks=40,50,60,70,100,110,120')
        s1.cmd('ovs-vsctl set port s1-eth8 trunks=10,50,60,70,100,120')

        # ── Distribution 1 – Floor 1 ──────────────────────────────────
        s2.cmd('ovs-vsctl set port s2-eth1 trunks=50,60,70,100,110,120,130')  # uplink
        s2.cmd('ovs-vsctl set port s2-eth2 trunks=50,110')                    # to s9
        s2.cmd('ovs-vsctl set port s2-eth3 trunks=110,130')                   # to s10
        s2.cmd('ovs-vsctl set port s2-eth4 trunks=60,70,130')                 # to s11
        s2.cmd('ovs-vsctl set port s2-eth5 trunks=100,120')                   # to s12

        # ── Floor 1 access switches ───────────────────────────────────
        # s9
        s9.cmd('ovs-vsctl set port s9-eth1 trunks=50,110')
        s9.cmd('ovs-vsctl set port s9-eth2 tag=50')     # ihf1rec1
        s9.cmd('ovs-vsctl set port s9-eth3 tag=110')    # ihf1gs1

        # s10
        s10.cmd('ovs-vsctl set port s10-eth1 trunks=110,130')
        s10.cmd('ovs-vsctl set port s10-eth2 tag=110')  # ihf1gs2
        s10.cmd('ovs-vsctl set port s10-eth3 tag=130')  # ihf1sr1

        # s11
        s11.cmd('ovs-vsctl set port s11-eth1 trunks=60,70,130')
        s11.cmd('ovs-vsctl set port s11-eth2 tag=60')   # ihf7ps1
        s11.cmd('ovs-vsctl set port s11-eth3 tag=70')   # ihf7mr1
        s11.cmd('ovs-vsctl set port s11-eth4 tag=130')  # ihf1sr2

        # s12
        s12.cmd('ovs-vsctl set port s12-eth1 trunks=100,120')
        s12.cmd('ovs-vsctl set port s12-eth2 tag=100')  # ihf1cm1
        s12.cmd('ovs-vsctl set port s12-eth3 tag=120')  # ihf1voip1

        # ── Distribution 2 – Floor 2 ──────────────────────────────────
        s3.cmd('ovs-vsctl set port s3-eth1 trunks=30,50,60,70,100,120')  # uplink
        s3.cmd('ovs-vsctl set port s3-eth2 trunks=30,50')                # to s13
        s3.cmd('ovs-vsctl set port s3-eth3 trunks=30')                   # to s14
        s3.cmd('ovs-vsctl set port s3-eth4 trunks=30,60,70')            # to s15
        s3.cmd('ovs-vsctl set port s3-eth5 trunks=100,120')             # to s16

        # ── Floor 2 access switches ───────────────────────────────────
        # s13
        s13.cmd('ovs-vsctl set port s13-eth1 trunks=30,50')
        s13.cmd('ovs-vsctl set port s13-eth2 tag=30')   # ihf2iot1
        s13.cmd('ovs-vsctl set port s13-eth3 tag=50')   # ihf2rec1

        # s14
        s14.cmd('ovs-vsctl set port s14-eth1 trunks=30')
        s14.cmd('ovs-vsctl set port s14-eth2 tag=30')   # ihf2iot2

        # s15
        s15.cmd('ovs-vsctl set port s15-eth1 trunks=30,60,70')
        s15.cmd('ovs-vsctl set port s15-eth2 tag=30')   # ihf2iot3
        s15.cmd('ovs-vsctl set port s15-eth3 tag=60')   # ihf2ps1
        s15.cmd('ovs-vsctl set port s15-eth4 tag=70')   # ihf2mr1

        # s16
        s16.cmd('ovs-vsctl set port s16-eth1 trunks=100,120')
        s16.cmd('ovs-vsctl set port s16-eth2 tag=100')  # ihf2cm1
        s16.cmd('ovs-vsctl set port s16-eth3 tag=120')  # ihf2voip1

        # ── Distribution 3 – Floor 3 ──────────────────────────────────
        s4.cmd('ovs-vsctl set port s4-eth1 trunks=20,50,100,120')  # uplink

        s4.cmd('ovs-vsctl set port s4-eth2 trunks=20,50')          # to s17
        s4.cmd('ovs-vsctl set port s4-eth3 trunks=20')             # to s18
        s4.cmd('ovs-vsctl set port s4-eth4 trunks=20')             # to s19
        s4.cmd('ovs-vsctl set port s4-eth5 trunks=100,120')        # to s20


        # ── Floor 3 access switches ───────────────────────────────────
        # s17
        s17.cmd('ovs-vsctl set port s17-eth1 trunks=20,50')
        s17.cmd('ovs-vsctl set port s17-eth2 tag=20')   # ihf3eng1
        s17.cmd('ovs-vsctl set port s17-eth3 tag=50')   # ihf3rec1

        # s18
        s18.cmd('ovs-vsctl set port s18-eth1 trunks=20')
        s18.cmd('ovs-vsctl set port s18-eth2 tag=20')   # ihf3eng2

        # s19
        s19.cmd('ovs-vsctl set port s19-eth1 trunks=20')
        s19.cmd('ovs-vsctl set port s19-eth2 tag=20')   # ihf3eng3

        # s20
        s20.cmd('ovs-vsctl set port s20-eth1 trunks=100,120')
        s20.cmd('ovs-vsctl set port s20-eth2 tag=100')  # ihf3cm1
        s20.cmd('ovs-vsctl set port s20-eth3 tag=120')  # ihf3voip1


        # ── Distribution 4 – Floor 4 ──────────────────────────────────
        s5.cmd('ovs-vsctl set port s5-eth1 trunks=20,50,70,100,120')  # uplink

        s5.cmd('ovs-vsctl set port s5-eth2 trunks=20,50')             # to s21
        s5.cmd('ovs-vsctl set port s5-eth3 trunks=20')                # to s22
        s5.cmd('ovs-vsctl set port s5-eth4 trunks=20,70')             # to s23
        s5.cmd('ovs-vsctl set port s5-eth5 trunks=100,120')           # to s24


        # ── Floor 4 access switches ───────────────────────────────────

        # s21
        s21.cmd('ovs-vsctl set port s21-eth1 trunks=20,50')
        s21.cmd('ovs-vsctl set port s21-eth2 tag=20')   # ihf4eng1
        s21.cmd('ovs-vsctl set port s21-eth3 tag=50')   # ihf4rec1

        # s22
        s22.cmd('ovs-vsctl set port s22-eth1 trunks=20')
        s22.cmd('ovs-vsctl set port s22-eth2 tag=20')   # ihf4eng2

        # s23
        s23.cmd('ovs-vsctl set port s23-eth1 trunks=20,70')
        s23.cmd('ovs-vsctl set port s23-eth2 tag=20')   # ihf4eng3
        s23.cmd('ovs-vsctl set port s23-eth3 tag=70')   # ihf4mr1

        # s24
        s24.cmd('ovs-vsctl set port s24-eth1 trunks=100,120')
        s24.cmd('ovs-vsctl set port s24-eth2 tag=100')  # ihf4cm1
        s24.cmd('ovs-vsctl set port s24-eth3 tag=120')  # ihf4voip1


        # ── Distribution 5 – Floor 5 ──────────────────────────────────
        s6.cmd('ovs-vsctl set port s6-eth1 trunks=20,50,100,120')  # uplink

        s6.cmd('ovs-vsctl set port s6-eth2 trunks=20,50')          # to s25
        s6.cmd('ovs-vsctl set port s6-eth3 trunks=20')             # to s26
        s6.cmd('ovs-vsctl set port s6-eth4 trunks=20')             # to s27
        s6.cmd('ovs-vsctl set port s6-eth5 trunks=100,120')        # to s28


        # ── Floor 5 access switches ───────────────────────────────────

        # s25
        s25.cmd('ovs-vsctl set port s25-eth1 trunks=20,50')
        s25.cmd('ovs-vsctl set port s25-eth2 tag=20')   # ihf5eng1
        s25.cmd('ovs-vsctl set port s25-eth3 tag=50')   # ihf5rec1

        # s26
        s26.cmd('ovs-vsctl set port s26-eth1 trunks=20')
        s26.cmd('ovs-vsctl set port s26-eth2 tag=20')   # ihf5eng2

        # s27
        s27.cmd('ovs-vsctl set port s27-eth1 trunks=20')
        s27.cmd('ovs-vsctl set port s27-eth2 tag=20')   # ihf5eng3

        # s28
        s28.cmd('ovs-vsctl set port s28-eth1 trunks=100,120')
        s28.cmd('ovs-vsctl set port s28-eth2 tag=100')  # ihf5cm1
        s28.cmd('ovs-vsctl set port s28-eth3 tag=120')  # ihf5voip1


        # ── Distribution 6 – Floor 6 ──────────────────────────────────
        s7.cmd('ovs-vsctl set port s7-eth1 trunks=40,50,60,70,100,110,120')  # uplink

        s7.cmd('ovs-vsctl set port s7-eth2 trunks=50,60,110')                # to s29
        s7.cmd('ovs-vsctl set port s7-eth3 trunks=40')                       # to s30
        s7.cmd('ovs-vsctl set port s7-eth4 trunks=40')                       # to s31
        s7.cmd('ovs-vsctl set port s7-eth5 trunks=40,70')                    # to s32
        s7.cmd('ovs-vsctl set port s7-eth6 trunks=100,120')                  # to s33


        # ── Floor 6 access switches ───────────────────────────────────

        # s29
        s29.cmd('ovs-vsctl set port s29-eth1 trunks=50,60,110')
        s29.cmd('ovs-vsctl set port s29-eth2 tag=50')   # ihf6rec1
        s29.cmd('ovs-vsctl set port s29-eth3 tag=60')   # ihf6ps1
        s29.cmd('ovs-vsctl set port s29-eth4 tag=110')  # ihf6gs1

        # s30
        s30.cmd('ovs-vsctl set port s30-eth1 trunks=40')
        s30.cmd('ovs-vsctl set port s30-eth2 tag=40')   # ihf6hr1

        # s31
        s31.cmd('ovs-vsctl set port s31-eth1 trunks=40')
        s31.cmd('ovs-vsctl set port s31-eth2 tag=40')   # ihf6hr2

        # s32
        s32.cmd('ovs-vsctl set port s32-eth1 trunks=40,70')
        s32.cmd('ovs-vsctl set port s32-eth2 tag=40')   # ihf6hr3
        s32.cmd('ovs-vsctl set port s32-eth3 tag=70')   # ihf6mr1

        # s33
        s33.cmd('ovs-vsctl set port s33-eth1 trunks=100,120')
        s33.cmd('ovs-vsctl set port s33-eth2 tag=100')  # ihf6cm1
        s33.cmd('ovs-vsctl set port s33-eth3 tag=120')  # ihf6voip1


        # ── Distribution 7 – Floor 7 ──────────────────────────────────
        s8.cmd('ovs-vsctl set port s8-eth1 trunks=10,50,60,70,100,120')  # uplink

        s8.cmd('ovs-vsctl set port s8-eth2 trunks=10,50')                # to s34
        s8.cmd('ovs-vsctl set port s8-eth3 trunks=10,60,70')             # to s35
        s8.cmd('ovs-vsctl set port s8-eth4 trunks=100,120')              # to s36


        # ── Floor 7 access switches ───────────────────────────────────

        # s34
        s34.cmd('ovs-vsctl set port s34-eth1 trunks=10,50')
        s34.cmd('ovs-vsctl set port s34-eth2 tag=10')   # ihf7exe1
        s34.cmd('ovs-vsctl set port s34-eth3 tag=50')   # ihf7rec1

        # s35
        s35.cmd('ovs-vsctl set port s35-eth1 trunks=10,60,70')
        s35.cmd('ovs-vsctl set port s35-eth2 tag=10')   # ihf7exe2
        s35.cmd('ovs-vsctl set port s35-eth3 tag=60')   # ihf7ps1
        s35.cmd('ovs-vsctl set port s35-eth4 tag=70')   # ihf7mr1

        # s36
        s36.cmd('ovs-vsctl set port s36-eth1 trunks=100,120')
        s36.cmd('ovs-vsctl set port s36-eth2 tag=100')  # ihf7cm1
        s36.cmd('ovs-vsctl set port s36-eth3 tag=120')  # ihf7voip1


        # ── Static host default routes ────────────────────────────────

        # VLAN 10 - Executives
        net.get('ihf7exe1').setDefaultRoute('via 10.10.10.1')
        net.get('ihf7exe2').setDefaultRoute('via 10.10.10.1')

        # VLAN 20 - Engineering
        net.get('ihf3eng1').setDefaultRoute('via 10.10.20.1')
        net.get('ihf4eng1').setDefaultRoute('via 10.10.20.1')
        net.get('ihf5eng1').setDefaultRoute('via 10.10.20.1')
        net.get('ihf3eng2').setDefaultRoute('via 10.10.20.1')
        net.get('ihf4eng2').setDefaultRoute('via 10.10.20.1')
        net.get('ihf5eng2').setDefaultRoute('via 10.10.20.1')
        net.get('ihf3eng3').setDefaultRoute('via 10.10.20.1')
        net.get('ihf4eng3').setDefaultRoute('via 10.10.20.1')
        net.get('ihf5eng3').setDefaultRoute('via 10.10.20.1')

        # VLAN 30 - IoT
        net.get('ihf2iot1').setDefaultRoute('via 10.10.30.1')
        net.get('ihf2iot2').setDefaultRoute('via 10.10.30.1')
        net.get('ihf2iot3').setDefaultRoute('via 10.10.30.1')

        # VLAN 40 - HR
        net.get('ihf6hr1').setDefaultRoute('via 10.10.40.1')
        net.get('ihf6hr2').setDefaultRoute('via 10.10.40.1')
        net.get('ihf6hr3').setDefaultRoute('via 10.10.40.1')

        # VLAN 50 - Reception
        net.get('ihf1rec1').setDefaultRoute('via 10.10.50.1')
        net.get('ihf2rec1').setDefaultRoute('via 10.10.50.1')
        net.get('ihf3rec1').setDefaultRoute('via 10.10.50.1')
        net.get('ihf4rec1').setDefaultRoute('via 10.10.50.1')
        net.get('ihf5rec1').setDefaultRoute('via 10.10.50.1')
        net.get('ihf6rec1').setDefaultRoute('via 10.10.50.1')
        net.get('ihf7rec1').setDefaultRoute('via 10.10.50.1')

        # VLAN 60 - Print Servers
        net.get('ihf7ps1').setDefaultRoute('via 10.10.60.1')
        net.get('ihf6ps1').setDefaultRoute('via 10.10.60.1')
        net.get('ihf2ps1').setDefaultRoute('via 10.10.60.1')
        net.get('ihf1ps1').setDefaultRoute('via 10.10.60.1')

        # VLAN 70 - Meeting Rooms
        net.get('ihf7mr1').setDefaultRoute('via 10.10.70.1')
        net.get('ihf6mr1').setDefaultRoute('via 10.10.70.1')
        net.get('ihf4mr1').setDefaultRoute('via 10.10.70.1')
        net.get('ihf2mr1').setDefaultRoute('via 10.10.70.1')
        net.get('ihf1mr1').setDefaultRoute('via 10.10.70.1')

        # VLAN 100 - Cameras
        net.get('ihf1cm1').setDefaultRoute('via 10.10.100.1')
        net.get('ihf2cm1').setDefaultRoute('via 10.10.100.1')
        net.get('ihf3cm1').setDefaultRoute('via 10.10.100.1')
        net.get('ihf4cm1').setDefaultRoute('via 10.10.100.1')
        net.get('ihf5cm1').setDefaultRoute('via 10.10.100.1')
        net.get('ihf6cm1').setDefaultRoute('via 10.10.100.1')
        net.get('ihf7cm1').setDefaultRoute('via 10.10.100.1')

        # VLAN 110 - Guests
        net.get('ihf1gs1').setDefaultRoute('via 10.10.110.1')
        net.get('ihf1gs2').setDefaultRoute('via 10.10.110.1')
        net.get('ihf6gs1').setDefaultRoute('via 10.10.110.1')

        # VLAN 120 - VoIP
        net.get('ihf1voip1').setDefaultRoute('via 10.10.120.1')
        net.get('ihf2voip1').setDefaultRoute('via 10.10.120.1')
        net.get('ihf3voip1').setDefaultRoute('via 10.10.120.1')
        net.get('ihf4voip1').setDefaultRoute('via 10.10.120.1')
        net.get('ihf5voip1').setDefaultRoute('via 10.10.120.1')
        net.get('ihf6voip1').setDefaultRoute('via 10.10.120.1')
        net.get('ihf7voip1').setDefaultRoute('via 10.10.120.1')

        # VLAN 130 - Servers
        net.get('ihf1sr1').setDefaultRoute('via 10.10.130.254')
        net.get('ihf1sr2').setDefaultRoute('via 10.10.130.254')

        # ── Server host ───────────────────────────────────────────────
        ihf1sr1 = net.get('ihf1sr1')
        ihf1sr2 = net.get('ihf1sr2')

        ihf1sr1.setDefaultRoute('via 10.10.130.254')
        ihf1sr2.setDefaultRoute('via 10.10.130.254')


        print("Illinois config applied successfully!")


def run():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink, autoSetMacs=True)
    site = Illinois()
    site.build(net)
    net.start()
    site.config(net)


if __name__ == '__main__':
    setLogLevel('info')
    run()
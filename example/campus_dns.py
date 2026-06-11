from mininet.net import Mininet 
from mininet.node import OVSSwitch 
from mininet.link import TCLink
from mininet.cli import CLI 
from mininet.log import setLogLevel 

def build_campus():
    net = Mininet(controller = None, switch=OVSSwitch, link=TCLink, autoSetMacs=True, autoStaticArp=False)
    
    core_1=net.addSwitch('core1', failMode='standalone')
    dist_1=net.addSwitch('dist1', failMode='standalone')
    acc_1=net.addSwitch('acc1', failMode='standalone')

    dns_srv=net.addHost('dns_srv', ip='192.168.100.10/24', defaultRoute='via 192.168.100.254')
    web_srv = net.addHost('web_srv', ip='192.168.100.20/24', defaultRoute='via 192.168.100.254')
    ftp_srv = net.addHost('ftp_srv', ip='192.168.100.30/24', defaultRoute='via 192.168.100.254')

    client = net.addHost('client1', ip=None, privateDirs=['/etc'])

    net.addLink(dns_srv, core_1, port1=0, port2=1)
    net.addLink(web_srv, core_1, port1=0, port2=2)
    net.addLink(ftp_srv, core_1, port1=0, port2=3)

    net.addLink(client, acc_1, port1=0, port2=1)
    net.addLink(acc_1,dist_1)
    net.addLink(dist_1,core_1)

    net.start()

    # Fix dhclient fstab bug: privateDirs=['/etc'] creates isolated /etc without fstab
    client.cmd('touch /etc/fstab')

    acc_1.cmd('ovs-vsctl set port acc1-eth1 tag=10')
    core_1.cmd('ovs-vsctl set port core1-eth1 tag=100')
    core_1.cmd('ovs-vsctl set port core1-eth2 tag=100')
    core_1.cmd('ovs-vsctl set port core1-eth3 tag=100')

    # trunks
    acc_1.cmd('ovs-vsctl set port acc1-eth2 trunks=10,100')
    dist_1.cmd('ovs-vsctl set port dist1-eth1 trunks=10,100')
    dist_1.cmd('ovs-vsctl set port dist1-eth2 trunks=10,100')
    core_1.cmd('ovs-vsctl set port core1-eth4 trunks=10,100')

    core_1.cmd('ovs-vsctl add-port core1 vlan10 tag=10 -- set interface vlan10 type=internal')
    core_1.cmd('ip addr add 10.0.10.254/24 dev vlan10')
    core_1.cmd('ip link set vlan10 up')

    core_1.cmd('ovs-vsctl add-port core1 vlan100 tag=100 -- set interface vlan100 type=internal')
    core_1.cmd('ip addr add 192.168.100.254/24 dev vlan100')
    core_1.cmd('ip link set vlan100 up')

    core_1.cmd('sysctl -w net.ipv4.ip_forward=1')
    

    # removes docker's specific rules that were blocking traffic
    core_1.cmd('iptables -P FORWARD ACCEPT')
    core_1.cmd('iptables -F FORWARD')
    core_1.cmd('dhcrelay -4 -i vlan10 -i vlan100 192.168.100.10 &')

    CLI(net)

    core_1.cmd('killall dhcrelay 2>/dev/null')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    build_campus()
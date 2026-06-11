from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

from site_mty import SiteMTY
from site_cdmx import SiteCDMX

def deploy_wan_network():
    net = Mininet(controller=None, 
                  switch=OVSSwitch, 
                  link=TCLink, 
                  autoSetMacs=True)
    mtyBranch = SiteMTY()
    mtyBranch.build(net)

    cdmxBranch = SiteCDMX()
    cdmxBranch.build(net)
    
    net.addLink(mtyBranch.gateway, cdmxBranch.gateway, intfName1='mty-cdmx', intfName2='cdmx-mty', cls=TCLink)
    mtyBranch.gateway.setIP('172.16.50.1/30', intf='mty-cdmx')
    cdmxBranch.gateway.setIP('172.16.50.2/30', intf='cdmx-mty')

    net.start()

    for site in (mtyBranch, cdmxBranch):
        site.config(net)

    CLI(net)
    
    for host in ['hMTYs1', 'hCDMXc1']:
        net.get(host).cmd('umount /etc/resolv.conf')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    deploy_wan_network()
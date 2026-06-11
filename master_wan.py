from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from illinois import Illinois
from saltillo import Saltillo
from texas import Texas
from monterrey import Monterrey

# WAN topology (hub + two direct branch links):
#
#   Illinois (HQ)  ←—192.168.100.0/30—→  Saltillo    (10.30.0.0/16)  primary
#   Illinois (HQ)  ←—192.168.150.0/30—→  Monterrey   (10.20.0.0/16)
#   Illinois (HQ)  ←—192.168.200.0/30—→  Texas       (10.40.0.0/16)
#   Monterrey ETEC ←—192.168.110.0/30—→  Saltillo    secondary (engineering peering)
#   Monterrey ETEC ←—192.168.210.0/30—→  Texas       (direct)
#
# Routing policy:
#   Saltillo  → Illinois  (primary),  Monterrey (direct secondary)
#             — NO route to Texas (isolated from TX)
#   Monterrey → Illinois, Saltillo (direct), Texas (direct)
#   Texas     → Illinois, Monterrey (direct)
#             — NO route to Saltillo (isolated from SAL)
#   Illinois  → all branches (hub)

def build_master():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink, autoSetMacs=True)

    illinois  = Illinois()
    illinois.build(net)

    saltillo  = Saltillo()
    saltillo.build(net)

    monterrey = Monterrey()
    monterrey.build(net)

    texas     = Texas()
    texas.build(net)

    # ── WAN links ─────────────────────────────────────────────────────────
    # Illinois hub links
    net.addLink(illinois.gateway,  saltillo.gateway,
                intfName1='illi-sal', intfName2='sal-illi',  cls=TCLink)
    net.addLink(illinois.gateway,  monterrey.gateway,
                intfName1='illi-mty', intfName2='mty-illi',  cls=TCLink)
    net.addLink(illinois.gateway,  texas.gateway,
                intfName1='illi-tex', intfName2='tex-illi',  cls=TCLink)

    # Direct branch links
    net.addLink(monterrey.gateway, saltillo.gateway,
                intfName1='mty-sal',  intfName2='sal-mty',   cls=TCLink)
    net.addLink(monterrey.gateway, texas.gateway,
                intfName1='mty-tex',  intfName2='tex-mty',   cls=TCLink)

    net.start()

    # ── WAN interface IPs ─────────────────────────────────────────────────
    illinois.gateway.setIP('192.168.100.1/30', intf='illi-sal')
    saltillo.gateway.setIP('192.168.100.2/30', intf='sal-illi')

    illinois.gateway.setIP('192.168.150.1/30', intf='illi-mty')
    monterrey.gateway.setIP('192.168.150.2/30', intf='mty-illi')

    illinois.gateway.setIP('192.168.200.1/30', intf='illi-tex')
    texas.gateway.setIP('192.168.200.2/30', intf='tex-illi')

    monterrey.gateway.setIP('192.168.110.1/30', intf='mty-sal')
    saltillo.gateway.setIP('192.168.110.2/30', intf='sal-mty')

    monterrey.gateway.setIP('192.168.210.1/30', intf='mty-tex')
    texas.gateway.setIP('192.168.210.2/30', intf='tex-mty')

    # ── Site configs (SVIs, VLANs, services, internal routes) ─────────────
    for site in (illinois, saltillo, monterrey, texas):
        site.config(net)

    # ── Cross-site routes ─────────────────────────────────────────────────

    # Illinois → all branches
    illinois.gateway.cmd('ip route add 10.30.0.0/16 via 192.168.100.2')
    illinois.gateway.cmd('ip route add 10.20.0.0/16 via 192.168.150.2')
    illinois.gateway.cmd('ip route add 10.40.0.0/16 via 192.168.200.2')

    # Saltillo: Illinois primary, Monterrey direct secondary — NO Texas route
    saltillo.gateway.cmd('ip route add 10.10.0.0/16 via 192.168.100.1')  # Illinois
    saltillo.gateway.cmd('ip route add 10.20.0.0/16 via 192.168.110.1')  # Monterrey direct

    # Monterrey: direct to all three sites
    monterrey.gateway.cmd('ip route add 10.10.0.0/16 via 192.168.150.1')  # Illinois
    monterrey.gateway.cmd('ip route add 10.30.0.0/16 via 192.168.110.2')  # Saltillo direct
    monterrey.gateway.cmd('ip route add 10.40.0.0/16 via 192.168.210.2')  # Texas direct

    # Texas: Illinois and Monterrey only — NO Saltillo route
    texas.gateway.cmd('ip route add 10.10.0.0/16 via 192.168.200.1')  # Illinois
    texas.gateway.cmd('ip route add 10.20.0.0/16 via 192.168.210.1')  # Monterrey direct

    CLI(net)

    # ── Cleanup ───────────────────────────────────────────────────────────
    net.get('s1').cmd('pkill dhcrelay 2>/dev/null')
    net.get('sSALc1').cmd('pkill dhcrelay 2>/dev/null')
    net.get('sMTYc1').cmd('pkill dhcrelay 2>/dev/null')
    net.get('sTEXc1').cmd('pkill dhcrelay 2>/dev/null')
    net.get('s1').cmd('sed -i "/agco./d" /etc/hosts')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    build_master()


# Connectivity tests from the Mininet CLI:
#   ihf3eng1   ping -c 3 10.30.20.10     Illinois Eng → Saltillo Eng   (via illi-sal)
#   ihf3eng1   ping -c 3 10.20.20.10     Illinois Eng → Monterrey Eng  (via illi-mty)
#   ihf3eng1   ping -c 3 10.40.20.2      Illinois Eng → Texas Eng      (via illi-tex)
#   hSALf1eng1 ping -c 3 10.20.20.10     Saltillo Eng → Monterrey Eng  (via sal-mty)
#   hMTYf2eng1 ping -c 3 10.30.20.10     Monterrey Eng → Saltillo Eng  (via mty-sal)
#   hTEXf3eng1 ping -c 3 10.20.20.10     Texas Eng → Monterrey Eng     (via tex-mty)
#
# Isolation checks (should fail):
#   hSALf1eng1 ping -c 2 10.40.20.2      Saltillo → Texas  (no route)
#   hTEXf3eng1 ping -c 2 10.30.20.10     Texas → Saltillo  (no route)

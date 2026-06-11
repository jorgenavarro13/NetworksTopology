# Illinois Site — Test Plan

## Topology Overview

| Element | Count |
|---------|-------|
| Router | 1 (`illinois`) |
| Core switch (L3) | 1 (`s1`) |
| Distribution switches | 7 (`s2–s8`, one per floor) |
| Access switches | 28 (`s9–s36`) |
| Server switch | 1 (`iSRVs1`) |
| Server hosts | 4 (`ihf1dns1`, `ihf1web1`, `ihf1ftp1`, `ihf1dhcp1`) |
| Floors | 7 |

## VLANs

| VLAN | Name | Subnet | Gateway |
|------|------|--------|---------|
| 10 | Executives | `10.10.10.0/25` | `10.10.10.1` |
| 20 | Engineering | `10.10.20.0/23` | `10.10.20.1` |
| 30 | IoT Labs | `10.10.30.0/25` | `10.10.30.1` |
| 40 | HR | `10.10.40.0/25` | `10.10.40.1` |
| 50 | Reception | `10.10.50.0/26` | `10.10.50.1` |
| 60 | Print Servers | `10.10.60.0/27` | `10.10.60.1` |
| 70 | Meeting Rooms | `10.10.70.0/26` | `10.10.70.1` |
| 99 | Uplink | `10.10.99.0/30` | — |
| 100 | Cameras | `10.10.100.0/25` | `10.10.100.1` |
| 110 | Guests | `10.10.110.0/25` | `10.10.110.1` |
| 120 | VoIP | `10.10.120.0/25` | `10.10.120.1` |
| 130 | Servers | `10.10.130.0/24` | `10.10.130.254` |

## Services

| Service | Host | IP | Port |
|---------|------|----|------|
| DHCP + DNS | `ihf1dhcp1` | `10.10.130.40` | 53 / 67 |
| Web (HTTP) | `ihf1web1` | `10.10.130.20` | 80 |
| FTP | `ihf1ftp1` | `10.10.130.30` | 21 |

---

## Test 1 — Layer 2: VLAN Reachability (same VLAN, same floor)

Verify hosts on the same VLAN reach each other through access → distribution → core.

| Step | Command | Expected |
|------|---------|----------|
| Engineering floor 3 → floor 4 | `ihf3eng1 ping -c 3 10.10.20.40` | 0% loss |
| Reception floor 1 → floor 6 | `ihf1rec1 ping -c 3 10.10.50.40` | 0% loss |
| Cameras floor 1 → floor 7 | `ihf1cm1 ping -c 3 10.10.100.70` | 0% loss |

---

## Test 2 — Layer 3: Inter-VLAN Routing (through core SVIs)

Verify the core switch `s1` routes between VLANs via its SVIs.

| Step | Command | Expected |
|------|---------|----------|
| Engineering → HR | `ihf3eng1 ping -c 3 10.10.40.10` | 0% loss |
| Executives → Reception | `ihf7exe1 ping -c 3 10.10.50.5` | 0% loss |
| IoT Labs → Servers gateway | `ihf2iot1 ping -c 3 10.10.130.254` | 0% loss |
| VoIP → Meeting Rooms | `ihf1voip1 ping -c 3 10.10.70.10` | 0% loss |

---

## Test 3 — DHCP: Address Assignment via Relay

The relay on `s1` forwards VLAN 50 DHCP requests to `ihf1dhcp1` (10.10.130.40). Any Reception host without a static IP can be used as a test client.

| Step | Command | Expected |
|------|---------|----------|
| Request lease | `ihf1rec1 dhclient -v ihf1rec1-eth0` | Lease in `10.10.50.50–10.10.50.60` |
| Confirm address | `ihf1rec1 ip addr show ihf1rec1-eth0` | Address in VLAN 50 range |
| Check lease file | `ihf1dhcp1 cat illinois/ILL_dhcp.leases` | Entry for client MAC visible |

---

## Test 4 — DNS: Hostname Resolution

dnsmasq on `ihf1dhcp1` serves `records.txt` for the server VLAN.

| Step | Command | Expected |
|------|---------|----------|
| Resolve web server | `ihf3eng1 nslookup web.agco.illinois 10.10.130.40` | `10.10.130.20` |
| Resolve FTP server | `ihf3eng1 nslookup ftp.agco.illinois 10.10.130.40` | `10.10.130.30` |
| Resolve DNS server itself | `ihf3eng1 nslookup dns.agco.illinois 10.10.130.40` | `10.10.130.10` |

---

## Test 5 — Web Service: HTTP

`ihf1web1` serves `illinois/web/index.html` on port 80.

| Step | Command | Expected |
|------|---------|----------|
| Fetch by IP | `ihf3eng1 curl -s http://10.10.130.20` | HTML content returned |
| Fetch by hostname | `ihf3eng1 curl -s --dns-servers 10.10.130.40 http://web.agco.illinois` | Same content |

---

## Test 6 — FTP Service: File Transfer

`ihf1ftp1` runs pyftpdlib on port 21. Credentials: `admin / secret123`.

| Step | Command | Expected |
|------|---------|----------|
| Connect and list | `ihf3eng1 ftp -n 10.10.130.30` → `user admin secret123` → `ls` | Directory listing returned |
| Download a file | `get <filename>` | Transfer completes without errors |

---

## Test 7 — Gateway Uplink

Verify the site gateway routes traffic to and from the core switch.

| Step | Command | Expected |
|------|---------|----------|
| Gateway → core | `illinois ping -c 3 10.10.99.2` | 0% loss |
| Core → gateway | `s1 ping -c 3 10.10.99.1` | 0% loss |
| Host → gateway | `ihf3eng1 ping -c 3 10.10.99.1` | 0% loss (routed through SVIs) |

---

## Test 8 — WAN: Cross-site Connectivity (master_wan.py only)

Verify Illinois hosts can reach Saltillo hosts through the WAN link (`illi-sal` / `sal-illi`).

| Step | Command | Expected |
|------|---------|----------|
| Illinois Eng → Saltillo Eng | `ihf3eng1 ping -c 3 10.30.20.10` | 0% loss |
| Saltillo Eng → Illinois Eng | `hSALf1eng1 ping -c 3 10.10.20.30` | 0% loss |
| WAN link health | `illinois ping -c 3 192.168.100.2` | 0% loss |

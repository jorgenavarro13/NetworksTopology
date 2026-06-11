# Monterrey Site — Test Plan

## Topology Overview

| Element | Count |
|---------|-------|
| Router | 1 (`monterrey`) |
| Core switch (L3) | 1 (`sMTYc1`) |
| Server switch | 1 (`sMTYs1`) |
| Distribution switches | 4 (`sMTYd1–4`) |
| Access switches | 10 (`sMTYl1`, `sMTYf11–12`, `sMTYf21–23`, `sMTYf31–32`, `sMTYf41–42`) |
| Floors | 4 + Lobby |

## VLANs

| VLAN | Name | Subnet | Gateway |
|------|------|--------|---------|
| 10 | Executives | `10.20.10.0/27` | `10.20.10.1` |
| 20 | Engineering | `10.20.20.0/23` | `10.20.20.1` |
| 30 | IoT Labs | `10.20.30.0/26` | `10.20.30.1` |
| 40 | HR | `10.20.40.0/27` | `10.20.40.1` |
| 50 | Reception | `10.20.50.0/28` | `10.20.50.1` |
| 60 | Print Servers | `10.20.60.0/28` | `10.20.60.1` |
| 70 | Meeting Rooms | `10.20.70.0/26` | `10.20.70.1` |
| 99 | Uplink | `10.20.99.0/30` | — |
| 100 | Cameras | `10.20.100.0/27` | `10.20.100.1` |
| 110 | Guests | `10.20.110.0/26` | `10.20.110.1` |
| 120 | VoIP | `10.20.120.0/24` | `10.20.120.1` |
| 130 | Servers | `10.20.130.0/27` | `10.20.130.1` |

## Services

| Service | Host | IP | Port |
|---------|------|----|------|
| DHCP + DNS | `hMTYdhcp1` | `10.20.130.5` | 53 / 67 |
| Web (HTTP) | `hMTYweb1` | `10.20.130.3` | 80 |
| FTP | `hMTYftp1` | `10.20.130.4` | 21 |

## Inter-VLAN Policy

| Source VLAN | Allowed destinations |
|-------------|----------------------|
| Executives (10) | All VLANs |
| Engineering (20) | Engineering, IoT (30), Servers (130) |
| IoT (30) | IoT, Engineering (20), Servers (130) |
| HR (40) | HR, Executives (10), Servers (130) |
| Reception (50) | Reception, VoIP (120), Cameras (100), Servers (130) |
| VoIP (120) | VoIP, Reception (50), Servers (130) |
| Cameras (100) | Cameras, Reception (50), Servers (130) |
| Guests (110) | TCP/80 to Servers only (no ping, no other VLANs) |
| Print (60), Meeting (70) | Unrestricted |

---

## Test 1 — Layer 2: Same-VLAN Reachability

| Step | Command | Expected |
|------|---------|----------|
| Eng floor 2 → floor 3 | `hMTYf2eng1 ping -c 3 10.20.20.20` | 0% loss |
| Cameras floor 1 → floor 2 | `hMTYf1cam1 ping -c 3 10.20.100.3` | 0% loss |
| Reception lobby → floor 3 | `hMTYlrec1 ping -c 3 10.20.50.3` | 0% loss |

---

## Test 2 — Layer 3: Allowed Inter-VLAN Paths

| Step | Command | Expected |
|------|---------|----------|
| Executives → Engineering | `hMTYf4exe1 ping -c 3 10.20.20.10` | 0% loss |
| Executives → HR | `hMTYf4exe1 ping -c 3 10.20.40.2` | 0% loss |
| Engineering → IoT | `hMTYf2eng1 ping -c 3 10.20.30.2` | 0% loss |
| IoT → Engineering | `hMTYf1iot1 ping -c 3 10.20.20.10` | 0% loss |
| HR → Executives | `hMTYf3hr1 ping -c 3 10.20.10.2` | 0% loss |
| Reception → VoIP | `hMTYlrec1 ping -c 3 10.20.120.2` | 0% loss |
| Reception → Cameras | `hMTYlrec1 ping -c 3 10.20.100.2` | 0% loss |
| VoIP → Reception | `hMTYf1voi1 ping -c 3 10.20.50.2` | 0% loss |

---

## Test 3 — Policy: Blocked Inter-VLAN Paths

| Step | Command | Expected |
|------|---------|----------|
| Engineering → HR (blocked) | `hMTYf2eng1 ping -c 2 10.20.40.2` | 100% loss / REJECT |
| Engineering → Reception (blocked) | `hMTYf2eng1 ping -c 2 10.20.50.2` | 100% loss / REJECT |
| HR → Engineering (blocked) | `hMTYf3hr1 ping -c 2 10.20.20.10` | 100% loss / REJECT |
| Reception → Engineering (blocked) | `hMTYlrec1 ping -c 2 10.20.20.10` | 100% loss / REJECT |
| IoT → HR (blocked) | `hMTYf1iot1 ping -c 2 10.20.40.2` | 100% loss / REJECT |

---

## Test 4 — Guest Isolation

| Step | Command | Expected |
|------|---------|----------|
| Guest ping to any VLAN (blocked) | `hMTYlgs1 ping -c 2 10.20.20.10` | 100% loss (silent DROP) |
| Guest ping to server (blocked) | `hMTYlgs1 ping -c 2 10.20.130.3` | 100% loss (silent DROP) |
| Guest HTTP to web server (allowed) | `hMTYlgs1 curl -s http://10.20.130.3` | HTML returned |
| Guest curl other port (blocked) | `hMTYlgs1 curl -s --connect-timeout 2 ftp://10.20.130.4` | Timeout / refused |

---

## Test 5 — DHCP via Relay

| Step | Command | Expected |
|------|---------|----------|
| Reception DHCP | `hMTYlrec1 dhclient -v hMTYlrec1-eth0` | Lease in `10.20.50.5–13` |
| Guest DHCP | `hMTYlgs1 dhclient -v hMTYlgs1-eth0` | Lease in `10.20.110.5–60` |
| Check lease file | `hMTYdhcp1 cat monterrey/MTY_dhcp.leases` | Entries visible |

---

## Test 6 — DNS

| Step | Command | Expected |
|------|---------|----------|
| Resolve web | `hMTYf2eng1 nslookup web.agco.monterrey 10.20.130.5` | `10.20.130.3` |
| Resolve FTP | `hMTYf2eng1 nslookup ftp.agco.monterrey 10.20.130.5` | `10.20.130.4` |

---

## Test 7 — Web & FTP Services

| Step | Command | Expected |
|------|---------|----------|
| HTTP by IP | `hMTYf2eng1 curl -s http://10.20.130.3` | HTML content |
| FTP login | `hMTYf2eng1 ftp -n 10.20.130.4` → `user admin secret123` → `ls` | Directory listing |

---

## Test 8 — Gateway Uplink

| Step | Command | Expected |
|------|---------|----------|
| Gateway → core | `monterrey ping -c 3 10.20.99.2` | 0% loss |
| Host → gateway | `hMTYf2eng1 ping -c 3 10.20.99.1` | 0% loss |

---

## Test 9 — WAN Cross-Site (master_wan.py only)

| Step | Command | Expected |
|------|---------|----------|
| Monterrey Eng → Illinois Eng | `hMTYf2eng1 ping -c 3 10.10.20.30` | 0% loss |
| Monterrey Eng → Saltillo Eng | `hMTYf2eng1 ping -c 3 10.30.20.10` | 0% loss |
| Monterrey Eng → Texas Eng | `hMTYf2eng1 ping -c 3 10.40.20.2` | 0% loss |
| Illinois Eng → Monterrey Eng | `ihf3eng1 ping -c 3 10.20.20.10` | 0% loss |

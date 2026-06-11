# Texas Site — Test Plan

## Topology Overview

| Element | Count |
|---------|-------|
| Router | 1 (`texas`) |
| Core switch (L3) | 1 (`sTEXc1`) |
| Server switch | 1 (`sTEXs1`) |
| Distribution switches | 5 (`sTEXd1–5`) |
| Access switches | 10 (`sTEXf11–12`, `sTEXf21–22`, `sTEXf31–32`, `sTEXf41–42`, `sTEXf51–52`) |
| Floors | 5 |

## VLANs

| VLAN | Name | Subnet | Gateway |
|------|------|--------|---------|
| 10 | Executives | `10.40.10.0/27` | `10.40.10.1` |
| 20 | Engineering | `10.40.20.0/25` | `10.40.20.1` |
| 30 | Labs | `10.40.30.0/25` | `10.40.30.1` |
| 40 | HR | `10.40.40.0/27` | `10.40.40.1` |
| 50 | Reception | `10.40.50.0/28` | `10.40.50.1` |
| 60 | Print Servers | `10.40.60.0/28` | `10.40.60.1` |
| 70 | Meeting Rooms | `10.40.70.0/27` | `10.40.70.1` |
| 99 | Uplink | `10.40.99.0/30` | — |
| 100 | Cameras | `10.40.100.0/26` | `10.40.100.1` |
| 110 | Guests | `10.40.110.0/28` | `10.40.110.1` |
| 120 | VoIP | `10.40.120.0/26` | `10.40.120.1` |
| 130 | Servers | `10.40.130.0/26` | `10.40.130.1` |

## Services

| Service | Host | IP | Port |
|---------|------|----|------|
| DHCP + DNS | `hTEXdhcp1` | `10.40.130.40` | 53 / 67 |
| Web (HTTP) | `hTEXweb1` | `10.40.130.20` | 80 |
| FTP | `hTEXftp1` | `10.40.130.30` | 21 |

## Inter-VLAN Policy

| Source VLAN | Allowed destinations |
|-------------|----------------------|
| Executives (10) | All VLANs |
| Engineering (20) | Engineering, Labs (30), Servers (130) |
| Labs (30) | Labs, Engineering (20), Servers (130) |
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
| Eng floor 3 → floor 4 | `hTEXf3eng1 ping -c 3 10.40.20.3` | 0% loss |
| Cameras floor 1 → floor 2 | `hTEXf1cam1 ping -c 3 10.40.100.3` | 0% loss |
| VoIP floor 2 → floor 3 | `hTEXf2voi1 ping -c 3 10.40.120.3` | 0% loss |

---

## Test 2 — Layer 3: Allowed Inter-VLAN Paths

| Step | Command | Expected |
|------|---------|----------|
| Executives → Engineering | `hTEXf5exe1 ping -c 3 10.40.20.2` | 0% loss |
| Executives → HR | `hTEXf5exe1 ping -c 3 10.40.40.2` | 0% loss |
| Engineering → Labs | `hTEXf3eng1 ping -c 3 10.40.30.2` | 0% loss |
| Labs → Engineering | `hTEXf2lab1 ping -c 3 10.40.20.2` | 0% loss |
| HR → Executives | `hTEXf5hr1 ping -c 3 10.40.10.2` | 0% loss |
| Reception → VoIP | `hTEXf1rec1 ping -c 3 10.40.120.2` | 0% loss |
| Reception → Cameras | `hTEXf1rec1 ping -c 3 10.40.100.2` | 0% loss |
| VoIP → Reception | `hTEXf2voi1 ping -c 3 10.40.50.2` | 0% loss |

---

## Test 3 — Policy: Blocked Inter-VLAN Paths

| Step | Command | Expected |
|------|---------|----------|
| Engineering → HR (blocked) | `hTEXf3eng1 ping -c 2 10.40.40.2` | 100% loss / REJECT |
| Engineering → Reception (blocked) | `hTEXf3eng1 ping -c 2 10.40.50.2` | 100% loss / REJECT |
| HR → Engineering (blocked) | `hTEXf5hr1 ping -c 2 10.40.20.2` | 100% loss / REJECT |
| Reception → Engineering (blocked) | `hTEXf1rec1 ping -c 2 10.40.20.2` | 100% loss / REJECT |
| Labs → HR (blocked) | `hTEXf2lab1 ping -c 2 10.40.40.2` | 100% loss / REJECT |

---

## Test 4 — Guest Isolation

| Step | Command | Expected |
|------|---------|----------|
| Guest ping to any VLAN (blocked) | `hTEXf1gs1 ping -c 2 10.40.20.2` | 100% loss (silent DROP) |
| Guest ping to server (blocked) | `hTEXf1gs1 ping -c 2 10.40.130.20` | 100% loss (silent DROP) |
| Guest HTTP to web server (allowed) | `hTEXf1gs1 curl -s http://10.40.130.20` | HTML returned |
| Guest curl other port (blocked) | `hTEXf1gs1 curl -s --connect-timeout 2 ftp://10.40.130.30` | Timeout / refused |

---

## Test 5 — DHCP via Relay

| Step | Command | Expected |
|------|---------|----------|
| Reception DHCP | `hTEXf1rec1 dhclient -v hTEXf1rec1-eth0` | Lease in `10.40.50.5–13` |
| Guest DHCP | `hTEXf1gs1 dhclient -v hTEXf1gs1-eth0` | Lease in `10.40.110.5–13` |
| Check lease file | `hTEXdhcp1 cat texas/TEX_dhcp.leases` | Entries visible |

---

## Test 6 — DNS

| Step | Command | Expected |
|------|---------|----------|
| Resolve web | `hTEXf3eng1 nslookup web.agco.texas 10.40.130.40` | `10.40.130.20` |
| Resolve FTP | `hTEXf3eng1 nslookup ftp.agco.texas 10.40.130.40` | `10.40.130.30` |

---

## Test 7 — Web & FTP Services

| Step | Command | Expected |
|------|---------|----------|
| HTTP by IP | `hTEXf3eng1 curl -s http://10.40.130.20` | HTML content |
| FTP login | `hTEXf3eng1 ftp -n 10.40.130.30` → `user admin secret123` → `ls` | Directory listing |

---

## Test 8 — Gateway Uplink

| Step | Command | Expected |
|------|---------|----------|
| Gateway → core | `texas ping -c 3 10.40.99.2` | 0% loss |
| Host → gateway | `hTEXf3eng1 ping -c 3 10.40.99.1` | 0% loss |

---

## Test 9 — WAN Cross-Site (master_wan.py only)

| Step | Command | Expected |
|------|---------|----------|
| Texas Eng → Illinois Eng | `hTEXf3eng1 ping -c 3 10.10.20.30` | 0% loss |
| Texas Eng → Saltillo Eng | `hTEXf3eng1 ping -c 3 10.30.20.10` | 0% loss |
| Illinois Eng → Texas Eng | `ihf3eng1 ping -c 3 10.40.20.2` | 0% loss |
| Saltillo Eng → Texas Eng | `hSALf1eng1 ping -c 3 10.40.20.2` | 0% loss |

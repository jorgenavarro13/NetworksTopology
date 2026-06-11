# Saltillo Site — Test Plan

## Topology Overview

| Element | Count |
|---------|-------|
| Router | 1 (`saltillo`) |
| Core switch (L3) | 1 (`sSALc1`) |
| Server switch | 1 (`sSALs1`) |
| Distribution switches | 3 (`sSALd1–3`) |
| Access switches | 11 (`sSALl1`, `sSALf11–13`, `sSALf21–24`, `sSALf31–33`) |
| Floors | 3 + Lobby |

## VLANs

| VLAN | Name | Subnet | Gateway |
|------|------|--------|---------|
| 10 | Executives | `10.30.10.0/28` | `10.30.10.1` |
| 20 | Engineering | `10.30.20.0/25` | `10.30.20.1` |
| 30 | IoT Labs | `10.30.30.0/24` | `10.30.30.1` |
| 40 | HR | `10.30.40.0/27` | `10.30.40.1` |
| 50 | Reception | `10.30.50.0/27` | `10.30.50.1` |
| 60 | Print Servers | `10.30.60.0/28` | `10.30.60.1` |
| 70 | Meeting Rooms | `10.30.70.0/27` | `10.30.70.1` |
| 99 | Uplink | `10.30.99.0/30` | — |
| 100 | Cameras | `10.30.100.0/26` | `10.30.100.1` |
| 110 | Guests | `10.30.110.0/28` | `10.30.110.1` |
| 120 | VoIP | `10.30.120.0/26` | `10.30.120.1` |
| 130 | Servers | `10.30.130.0/27` | `10.30.130.1` |

## Services

| Service | Host | IP | Port |
|---------|------|----|------|
| DHCP + DNS | `hSALdhcp1` | `10.30.130.5` | 53 / 67 |
| Web (HTTP) | `hSALweb1` | `10.30.130.3` | 80 |
| FTP | `hSALftp1` | `10.30.130.4` | 21 |

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
| Eng floor 1 → floor 2 | `hSALf1eng1 ping -c 3 10.30.20.20` | 0% loss |
| Reception lobby → floor 1 | `hSALlrec1 ping -c 3 10.30.50.11` | 0% loss |
| Cameras floor 1 → floor 2 | `hSALf1cam1 ping -c 3 10.30.100.20` | 0% loss |

---

## Test 2 — Layer 3: Allowed Inter-VLAN Paths

| Step | Command | Expected |
|------|---------|----------|
| Executives → Engineering | `hSALf3exe1 ping -c 3 10.30.20.10` | 0% loss |
| Executives → HR | `hSALf3exe1 ping -c 3 10.30.40.10` | 0% loss |
| Engineering → IoT | `hSALf1eng1 ping -c 3 10.30.30.10` | 0% loss |
| IoT → Engineering | `hSALf1iot1 ping -c 3 10.30.20.10` | 0% loss |
| HR → Executives | `hSALf2hr1 ping -c 3 10.30.10.2` | 0% loss |
| Reception → VoIP | `hSALf1rec1 ping -c 3 10.30.120.10` | 0% loss |
| Reception → Cameras | `hSALf1rec1 ping -c 3 10.30.100.10` | 0% loss |
| VoIP → Reception | `hSALf1voi1 ping -c 3 10.30.50.11` | 0% loss |

---

## Test 3 — Policy: Blocked Inter-VLAN Paths

| Step | Command | Expected |
|------|---------|----------|
| Engineering → HR (blocked) | `hSALf1eng1 ping -c 2 10.30.40.10` | 100% loss / REJECT |
| Engineering → Reception (blocked) | `hSALf1eng1 ping -c 2 10.30.50.11` | 100% loss / REJECT |
| HR → Engineering (blocked) | `hSALf2hr1 ping -c 2 10.30.20.10` | 100% loss / REJECT |
| Reception → Engineering (blocked) | `hSALf1rec1 ping -c 2 10.30.20.10` | 100% loss / REJECT |
| IoT → HR (blocked) | `hSALf1iot1 ping -c 2 10.30.40.10` | 100% loss / REJECT |

---

## Test 4 — Guest Isolation

| Step | Command | Expected |
|------|---------|----------|
| Guest ping to any VLAN (blocked) | `hSALlgs1 ping -c 2 10.30.20.10` | 100% loss (silent DROP) |
| Guest ping to server (blocked) | `hSALlgs1 ping -c 2 10.30.130.3` | 100% loss (silent DROP) |
| Guest HTTP to web server (allowed) | `hSALlgs1 curl -s http://10.30.130.3` | HTML returned |
| Guest curl other port (blocked) | `hSALlgs1 curl -s --connect-timeout 2 ftp://10.30.130.4` | Timeout / refused |

---

## Test 5 — DHCP via Relay

| Step | Command | Expected |
|------|---------|----------|
| Reception DHCP | `hSALlrec1 dhclient -v hSALlrec1-eth0` | Lease in `10.30.50.20–28` |
| Guest DHCP | `hSALlgs1 dhclient -v hSALlgs1-eth0` | Lease in `10.30.110.5–13` |
| Check lease file | `hSALdhcp1 cat saltillo/SAL_dhcp.leases` | Entries visible |

---

## Test 6 — DNS

| Step | Command | Expected |
|------|---------|----------|
| Resolve web | `hSALf1eng1 nslookup web.agco.saltillo 10.30.130.5` | `10.30.130.3` |
| Resolve FTP | `hSALf1eng1 nslookup ftp.agco.saltillo 10.30.130.5` | `10.30.130.4` |

---

## Test 7 — Web & FTP Services

| Step | Command | Expected |
|------|---------|----------|
| HTTP by IP | `hSALf1eng1 curl -s http://10.30.130.3` | HTML content |
| FTP login | `hSALf1eng1 ftp -n 10.30.130.4` → `user admin secret123` → `ls` | Directory listing |

---

## Test 8 — Gateway Uplink

| Step | Command | Expected |
|------|---------|----------|
| Gateway → core | `saltillo ping -c 3 10.30.99.2` | 0% loss |
| Host → gateway | `hSALf1eng1 ping -c 3 10.30.99.1` | 0% loss |

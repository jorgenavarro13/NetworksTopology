# AGCO Network — Presentation Test Plan
**Runtime: ~6 min | ~1:30 per site | Run from Mininet CLI**

---

## Host Reference

| Role | Illinois | Saltillo | Monterrey | Texas |
|------|----------|----------|-----------|-------|
| Engineering | `ihf3eng1` | `hSALf1eng1` | `hMTYf2eng1` | `hTEXf3eng1` |
| IoT / Lab | `ihf2iot1` | `hSALf1iot1` | `hMTYf1iot1` | `hTEXf2lab1` |
| HR | `ihf6hr1` | `hSALf2hr1` | `hMTYf3hr1` | `hTEXf5hr1` |
| Reception | `ihf1rec1` | `hSALlrec1` | `hMTYlrec1` | `hTEXf1rec1` |
| Guest | `ihf1gs1` | `hSALlgs1` | `hMTYlgs1` | `hTEXf1gs1` |
| Camera | `ihf1cm1` | `hSALf1cam1` | `hMTYf1cam1` | `hTEXf1cam1` |
| Web server | `ihf1web1` | `hSALweb1` | `hMTYweb1` | `hTEXweb1` |
| DHCP / DNS | `ihf1dhcp1` | `hSALdhcp1` | `hMTYdhcp1` | `hTEXdhcp1` |

---

## Site 1 — Illinois HQ (~1:30)
> Open WAN hub — no inter-VLAN restrictions. Central web, FTP, DHCP, and DNS.

| # | Test | Command | Expected |
|---|------|---------|----------|
| 1 | Web service | `ihf3eng1 curl -s http://web.agco.illinois` | HTML content |
| 2 | FTP service | `ihf3eng1 ftp -n ihf1ftp1` → `user admin secret123` → `ls` | Directory listing |
| 4 | WAN hub → Saltillo | `ihf3eng1 ping -c 2 hSALf1eng1` | 0% loss |
| 5 | WAN hub → Texas | `ihf3eng1 ping -c 2 hTEXf3eng1` | 0% loss |

---

## Site 2 — Saltillo Plant (~1:30)
> Dual WAN: Illinois (primary), Monterrey (secondary). Engineering peers with both HQs. No Texas route.

| # | Test | Command | Expected |
|---|------|---------|----------|
| 1 | Web service | `hSALf1eng1 curl -s http://web.agco.saltillo` | HTML content |
| 2 | Allowed: Eng → IoT | `hSALf1eng1 ping -c 2 hSALf1iot1` | 0% loss |
| 3 | Blocked: Eng → HR | `hSALf1eng1 ping -c 2 hSALf2hr1` | 100% loss (REJECT) |
| 4 | WAN Eng → Illinois Eng | `hSALf1eng1 ping -c 2 ihf3eng1` | 0% loss (primary link) |
| 5 | WAN isolation → Texas | `hSALf1eng1 ping -c 2 hTEXf3eng1` | 100% loss (no route) |

---

## Site 3 — Monterrey ETEC (~1:30)
> Direct WAN to all three sites. IoT lab accessible from Illinois Engineering. Guests: HTTP to servers only.

| # | Test | Command | Expected |
|---|------|---------|----------|
| 1 | Web service | `hMTYf2eng1 curl -s http://web.agco.monterrey` | HTML content |
| 2 | Allowed: Eng → IoT | `hMTYf2eng1 ping -c 2 hMTYf1iot1` | 0% loss |
| 3 | Blocked: HR → Eng | `hMTYf3hr1 ping -c 2 hMTYf2eng1` | 100% loss (REJECT) |
| 4 | Guest HTTP ✓ / Ping ✗ | `hMTYlgs1 curl -s http://web.agco.monterrey` then `hMTYlgs1 ping -c 2 hMTYf2eng1` | HTML returned / silent DROP |
| 5 | WAN Eng → Saltillo Eng | `hMTYf2eng1 ping -c 2 hSALf1eng1` | 0% loss (direct link) |

---

## Site 4 — Texas Test Facility (~1:30)
> Connects to Illinois + Monterrey only. Cameras replicate to Illinois Servers. No Saltillo route.

| # | Test | Command | Expected |
|---|------|---------|----------|
| 1 | Web service | `hTEXf3eng1 curl -s http://web.agco.texas` | HTML content |
| 2 | Allowed: Eng → Labs | `hTEXf3eng1 ping -c 2 hTEXf2lab1` | 0% loss |
| 3 | Blocked: Eng → HR | `hTEXf3eng1 ping -c 2 hTEXf5hr1` | 100% loss (REJECT) |
| 4 | Camera → Illinois Servers | `hTEXf1cam1 ping -c 2 ihf1web1` | 0% loss (replication path) |
| 5 | WAN → Monterrey / isolation → Saltillo | `hTEXf3eng1 ping -c 2 hMTYf2eng1` then `hTEXf3eng1 ping -c 2 hSALf1eng1` | 0% loss / 100% loss (no route) |

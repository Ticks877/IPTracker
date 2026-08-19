# Tracker v1 🌐

A Python public-network OSINT and diagnostic toolkit for IPs, domains, URLs, TLS, and local files.

## Features

- 🔎 IP intelligence and IPv4/IPv6 validation
- 🌐 DNS lookup
- 🔄 Reverse DNS
- 🧮 CIDR/subnet calculator
- 🛡️ Reputation workflow notes
- 📜 TLS certificate information
- 🌍 Website diagnostics
- 🔐 MD5/SHA-1/SHA-256 hashing for local files
- 🔗 URL parser
- 📊 JSON report generation
- 🔗 Separate consent-based link diagnostic server

## Run

```bash
python3 tracker_v1.py
```

No third-party Python packages are required for Tracker v1.

The original `main.py` IP lookup remains available.

## Chromebook

Enable the ChromeOS Linux development environment, open Terminal, download/extract the repository, then run:

```bash
python3 tracker_v1.py
```

If Python is missing on Debian-based ChromeOS Linux:

```bash
sudo apt update
sudo apt install python3
```

## Scope

Tracker v1 is intended for public network/domain information and targets you own or are authorized to test. It does not include covert tracking, credential collection, private-account scraping, or precise personal-location hunting.

The link diagnostic component is explicitly consent-based and should only be used on infrastructure you control.

## Important notes

IP geolocation is approximate. An IP address does **not** provide a person's exact home address, and VPNs, mobile networks, proxies and carrier NAT can make location information inaccurate.

## EXTRA

its called ip tracker because in main.py it has a good iptracker 
but in Tracker_v1.py it just has some extra tools 

#!/usr/bin/env python3
"""Tracker v1: public network/domain OSINT and diagnostic toolkit.

Uses only Python's standard library. Features are limited to public network
information and targets supplied by the operator.
"""

import hashlib
import ipaddress
import json
import socket
import ssl
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone


def prompt_target(label="Target"): return input(f"{label}: ").strip()

def resolve_host(host):
    try:
        return sorted({x[4][0] for x in socket.getaddrinfo(host, None)})
    except socket.gaierror as e:
        return [f"Error: {e}"]

def dns_lookup():
    host = prompt_target("Domain/IP")
    print("\nAddresses:")
    for x in resolve_host(host): print(" ", x)

def reverse_dns():
    target = prompt_target("IP")
    try: print("Hostname:", socket.gethostbyaddr(target)[0])
    except (socket.herror, socket.gaierror) as e: print("Unavailable:", e)

def ip_intel():
    target = prompt_target("IP")
    try:
        obj = ipaddress.ip_address(target)
        print(f"Version: IPv{obj.version}")
        print(f"Private: {obj.is_private}")
        print(f"Global: {obj.is_global}")
        print(f"Loopback: {obj.is_loopback}")
        print(f"Multicast: {obj.is_multicast}")
        print(f"Reverse DNS name: {obj.reverse_pointer}")
    except ValueError: print("Invalid IP address.")

def subnet_calc():
    target = prompt_target("Network/CIDR (e.g. 192.168.1.0/24)")
    try:
        net = ipaddress.ip_network(target, strict=False)
        print("Network:", net.network_address)
        print("Netmask:", net.netmask)
        print("Broadcast:", net.broadcast_address)
        print("Prefix:", net.prefixlen)
        print("Hosts:", net.num_addresses if net.version == 6 else max(0, net.num_addresses - 2))
    except ValueError as e: print("Invalid network:", e)

def tls_info():
    host = prompt_target("Domain")
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=8) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as tls:
                cert = tls.getpeercert()
                print("TLS version:", tls.version())
                print("Cipher:", tls.cipher())
                print("Subject:", cert.get("subject"))
                print("Issuer:", cert.get("issuer"))
                print("Expires:", cert.get("notAfter"))
    except Exception as e: print("TLS lookup failed:", e)

def website_diag():
    url = prompt_target("URL")
    if not urllib.parse.urlparse(url).scheme: url = "https://" + url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Tracker-v1/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read(4096)
            print("Status:", r.status)
            print("Final URL:", r.geturl())
            print("Content-Type:", r.headers.get("Content-Type"))
            print("Server:", r.headers.get("Server", "Unavailable"))
            print("Sample bytes:", len(data))
    except Exception as e: print("Request failed:", e)

def hash_tool():
    path = input("File path: ").strip()
    try:
        hashes = {"md5": hashlib.md5(), "sha1": hashlib.sha1(), "sha256": hashlib.sha256()}
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                for h in hashes.values(): h.update(chunk)
        for name, h in hashes.items(): print(f"{name.upper()}: {h.hexdigest()}")
    except OSError as e: print("File error:", e)

def url_parser():
    raw = prompt_target("URL")
    p = urllib.parse.urlparse(raw)
    print("Scheme:", p.scheme or "(none)")
    print("Hostname:", p.hostname or "(none)")
    print("Port:", p.port or "(default)")
    print("Path:", p.path or "/")
    print("Query:", p.query or "(none)")


def reputation_note():
    target = prompt_target("IP/domain")
    print(f"Target: {target}")
    print("Use a public reputation provider to check this target manually.")
    print("Tracker v1 does not submit targets to third-party services automatically.")

def export_report():
    target = prompt_target("Target")
    report = {"tool": "Tracker v1", "target": target, "created_utc": datetime.now(timezone.utc).isoformat(), "note": "Public network/domain diagnostics only."}
    path = input("Output JSON filename [tracker_report.json]: ").strip() or "tracker_report.json"
    try:
        with open(path, "w", encoding="utf-8") as f: json.dump(report, f, indent=2)
        print("Saved:", path)
    except OSError as e: print("Could not save:", e)

def menu():
    actions = {"1": ip_intel, "2": dns_lookup, "3": reverse_dns, "4": subnet_calc, "5": reputation_note, "6": tls_info, "7": website_diag, "8": hash_tool, "9": url_parser, "10": export_report}
    while True:
        print("""
╔══════════════════════════════════════╗
║             TRACKER v1               ║
╠══════════════════════════════════════╣
║ [1] 🔎 IP Intelligence               ║
║ [2] 🌐 DNS Lookup                    ║
║ [3] 🔄 Reverse DNS                   ║
║ [4] 🧮 Subnet Calculator             ║
║ [5] 🛡️ Reputation Notes              ║
║ [6] 📜 TLS Certificate               ║
║ [7] 🌍 Website Diagnostics           ║
║ [8] 🔐 Hash Tools                    ║
║ [9] 🔗 URL Parser                    ║
║ [10] 📊 Report Generator             ║
║                                      ║
║ [0] Exit                             ║
╚══════════════════════════════════════╝""")
        choice = input("\nTracker > ").strip()
        if choice == "0": return
        action = actions.get(choice)
        if action:
            action()
            input("\nPress Enter to continue...")
        else: print("Unknown option.")

if __name__ == "__main__": menu()

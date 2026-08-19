#!/usr/bin/env python3
"""IPTracker - look up information about an IP address you provide.

Uses the public ipwho.is API. Only query IPs you are allowed to investigate.
"""

import ipaddress
import json
import sys
import urllib.error
import urllib.request

API = "https://ipwho.is/{}"


def lookup(ip):
    url = API.format(ip)
    request = urllib.request.Request(url, headers={"User-Agent": "IPTracker/1.0"})
    with urllib.request.urlopen(request, timeout=8) as response:
        return json.load(response)


def show(data):
    if not data.get("success", False):
        print(f"Lookup failed: {data.get('message', 'Unknown error')}")
        return

    connection = data.get("connection") or {}
    timezone = data.get("timezone") or {}
    print("\n╔══════════════════════════════════════╗")
    print("║             IPTRACKER               ║")
    print("╚══════════════════════════════════════╝")
    print(f"IP         : {data.get('ip', 'N/A')}")
    print(f"Type       : {'IPv6' if ':' in data.get('ip', '') else 'IPv4'}")
    print(f"Country    : {data.get('country', 'N/A')}")
    print(f"Region     : {data.get('region', 'N/A')}")
    print(f"City       : {data.get('city', 'N/A')}")
    print(f"Postal     : {data.get('postal', 'N/A')}")
    print(f"Latitude   : {data.get('latitude', 'N/A')}")
    print(f"Longitude  : {data.get('longitude', 'N/A')}")
    print(f"Timezone   : {timezone.get('id', 'N/A')}")
    print(f"ISP        : {connection.get('isp', 'N/A')}")
    print(f"Organization: {connection.get('org', 'N/A')}")
    print(f"ASN        : {connection.get('asn', 'N/A')}")
    print("\nNote: IP geolocation is approximate and does not reveal a person's exact address.")


def main():
    print("IPTracker v1.0")
    print("Look up approximate public IP information. Use only with permission.\n")
    while True:
        value = input("IPTracker > ").strip()
        if value.lower() in {"exit", "quit", "0"}:
            break
        if not value:
            continue
        try:
            ip = ipaddress.ip_address(value)
        except ValueError:
            print("Please enter a valid IPv4 or IPv6 address.")
            continue
        if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_multicast:
            print("That is a private/reserved address and cannot be meaningfully geolocated.")
            continue
        try:
            show(lookup(str(ip)))
        except urllib.error.URLError as exc:
            print(f"Network/API error: {exc}")
        except TimeoutError:
            print("The lookup timed out.")
        except Exception as exc:
            print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()

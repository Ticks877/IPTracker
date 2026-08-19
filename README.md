# IPTracker 🌐

A small Python CLI that looks up approximate public IP information.

## Features

- IPv4 and IPv6 validation
- Country, region and city lookup
- Approximate latitude/longitude
- Timezone
- ISP, organization and ASN
- No third-party Python packages required

## Run

```bash
python3 main.py
```

Enter a public IP address when prompted. Type `exit` to close the program.

## Chromebook

With the Linux development environment enabled, open Terminal and run:

```bash
python3 main.py
```

If Python is missing on Debian-based ChromeOS Linux:

```bash
sudo apt update
sudo apt install python3
```

## Important notes

IP geolocation is approximate. An IP address does **not** provide a person's exact home address, and VPNs, mobile networks, proxies and carrier NAT can make location information inaccurate.

Use IPTracker only for IP addresses you are authorized to investigate. The project does not perform port scanning, device exploitation, or attempts to identify private individuals.

## API

IPTracker uses the public `ipwho.is` API over HTTPS. Availability and rate limits are controlled by that service.

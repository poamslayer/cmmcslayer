# IT Environment

## Network

Flat network, 192.168.1.0/24. One Ubiquiti-class router/firewall ("EdgeRouter"), managed by Northstar Managed IT, running an L2TP/IPsec VPN server that Dana Ortiz uses from home. One 24-port unmanaged switch. Wi-Fi SSID "Saguaro" on the same LAN, WPA2-PSK, password on a sticky note in the break room. Guests use the same SSID as staff.

## Microsoft 365

Microsoft 365 Business Premium, commercial tenant `saguaropm.onmicrosoft.com`. Entra ID, Exchange Online, SharePoint (a "Jobs" library that mirrors part of the NAS), OneDrive, and Intune (licensed but only partially deployed). Conditional Access requires MFA (Microsoft Authenticator) for all users for cloud sign-in. Northstar's two Global Administrator accounts have MFA. There is no Purview DLP and no sensitivity labeling.

## Endpoints

Eight Windows 11 Pro machines, Entra-joined, BitLocker on (the FIPS Algorithm Policy is not enabled): OFFICE-DANA, OFFICE-LUIS, ENG-PRIYA (also runs the CAD/CAM software), PROG-TOM, QC-MARIA, SHIP-JORDAN, PURCH-ELLEN, ACCT-ROB, plus NADIA-LT. Microsoft Defender for Endpoint is present through Business Premium. The local administrator password is the same on every machine, from Northstar's build image.

SHOP-PC-01: Windows 10 Pro desktop at the Haas machine. Local account "shop" is shared by Kevin Marsh and Ana Delgado. Holds the g-code library on its local disk. USB ports enabled. On the LAN. Not Entra-joined. No BitLocker.

## CNC and CMM

Haas VF-2 with a Haas NextGen embedded control, on the LAN over Ethernet for network share access. Programs are loaded by USB stick or from SHOP-PC-01's share. It cannot run EDR and cannot be patched by the shop.

CMM: a Zeiss-class CMM with a dedicated Windows 7 PC ("CMM-PC") running the measurement software. Windows 7 cannot be patched. Inspection reports are saved to the NAS "Quality" share. On the LAN.

## NAS

Synology-class NAS "SAG-NAS," on the LAN. Shares: Jobs (drawings, travelers, CAM files), Quality, Admin. SMB with local NAS accounts and passwords, no MFA. SMB encryption uses the NAS vendor's own module, which is not FIPS validated. The admin console is reachable on the LAN over HTTPS with a password only, and Northstar reaches it through the RMM. No audit logging is enabled on the NAS. Backups are a USB drive that Nadia Haddad swaps weekly and takes home.

## MFP and printer

MFP-FRONT: a Canon-class color multifunction printer near the front office, on the LAN. Scan-to-email works to any address. Scan-to-folder goes to SAG-NAS/Quality. It has an internal hard drive and a USB print/scan port enabled. A copier company services it and dials in through a vendor cloud portal for meter reads. It prints CUI drawings daily.

PRN-SHOP: a small laser printer in the shop office, USB-attached to SHOP-PC-01.

## ERP

"ShopTrak," on-prem, on a Windows Server 2019 VM ("SAG-SRV1") hosted on a single Hyper-V host in the office closet. Traveler thumbnails, including the drawing image, are stored in ShopTrak's database.

## Personal devices

Dana Ortiz's home PC: VPNs into the LAN, then RDPs to OFFICE-DANA. Maria Chen's home laptop: opens FAI report scans sent to her personal Gmail address. Phones: everyone reads Outlook on personal phones; there is no MDM.

## Physical security

Front door keypad code is shared by all staff. The bay door is open in summer. There is no visitor log in active use, though a visitor sign-in sheet exists. The drawing sits on a clipboard at the machine. Old travelers go into the shop's regular recycling dumpster.

## Logging

The Microsoft 365 unified audit log is on by default. Windows event logs on endpoints stay local with a 20 MB rollover. There is no SIEM and no log review.

## Vulnerability management

No vulnerability scanning of any kind. Patching: Windows Update is managed by the Northstar RMM monthly. Nothing patches the NAS, CMM-PC, SHOP-PC-01, or the Haas control.

## Incident response

A two-page IR plan, supplied by Northstar from a template, has never been exercised. Nobody at Saguaro knows what DIBNET is.

## Training

No security awareness training has ever been delivered. Nobody has heard the term CUI except Luis Ferreira, who thinks it means ITAR.

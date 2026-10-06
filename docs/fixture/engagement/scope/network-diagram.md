# Network Diagram (Copy)

Copied from `docs/fixture/company/network-diagram.md`.

```mermaid
flowchart LR
  subgraph Internet
    MeridianLink[MeridianLink portal]
    M365[Microsoft 365 commercial tenant]
    CopierPortal[Copier vendor cloud portal]
    CloudVaultProposed[CloudVault Backup, proposed]
  end

  subgraph NorthstarSide[Northstar Managed IT]
    NorthstarRMM[Northstar RMM]
    SentrySOC[Sentry SOC LLC, alerts only]
  end

  Edge[EdgeRouter / firewall, L2TP VPN]

  subgraph LAN[Saguaro LAN, 192.168.1.0/24, flat]
    Switch[24-port unmanaged switch]
    WiFi[Wi-Fi SSID Saguaro, WPA2-PSK, staff and guests]
    OfficeEndpoints[8 office endpoints: OFFICE-DANA, OFFICE-LUIS, ENG-PRIYA, PROG-TOM, QC-MARIA, SHIP-JORDAN, PURCH-ELLEN, ACCT-ROB, NADIA-LT]
    ShopPC[SHOP-PC-01, shared shop login]
    Haas[Haas VF-2, NextGen control]
    CMMPC[CMM-PC, Windows 7]
    CMMHead[CMM measuring head]
    NAS[SAG-NAS: Jobs, Quality, Admin shares]
    MFP[MFP-FRONT]
    PrnShop[PRN-SHOP]
    SAGSRV1[SAG-SRV1: ShopTrak ERP]
  end

  HomeDana[Dana's home PC]
  HomeMaria[Maria's home laptop]
  Phones[Personal phones, Outlook, no MDM]
  Sonoran[Sonoran Anodize and Plating]
  USBBackup[USB backup drive, weekly, taken home]

  HomeDana -- VPN --> Edge
  Edge --> Switch
  Switch --> WiFi
  Switch --> OfficeEndpoints
  Switch --> ShopPC
  Switch --> Haas
  Switch --> CMMPC
  CMMPC --> CMMHead
  Switch --> NAS
  Switch --> MFP
  ShopPC --> PrnShop
  Switch --> SAGSRV1
  ShopPC -- USB stick --> Haas
  NAS -- weekly swap --> USBBackup
  MFP -- scan to email --> Phones
  OfficeEndpoints -- MeridianLink download --> MeridianLink
  OfficeEndpoints -- M365 sign-in --> M365
  MFP -- dial-in for meter reads --> CopierPortal
  NorthstarRMM -- unattended remote control --> OfficeEndpoints
  NorthstarRMM -- unattended remote control --> ShopPC
  NorthstarRMM -- unattended remote control --> NAS
  NorthstarRMM -- unattended remote control --> Edge
  NorthstarRMM -. alerts .-> SentrySOC
  NAS -. proposed backup .-> CloudVaultProposed
  OfficeEndpoints -- drawing PDF by email --> Sonoran
  HomeMaria -- personal Gmail, unauthorized --> MFP
```

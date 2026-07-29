---
title: Companion 5 - Es werde Licht, Kapitel 3
date: 2026-07-31
categories:
- Projekte
tags: 
- Raspberry Pi
- Streamdeck
- Lichtsteuerung
- Familienzentrum Erlangen
- Ehrenamt
summary: |
    Manche sehnen sich nach ihnen, anderen machen sie Angst: Updates.
---

Manche sehnen sich nach ihnen, anderen machen sie Angst: Updates.

[Companion v5.0.0](https://companion.free/whats-new/v5-0-0) ist da
und eine der Neuerungen ist das neue Button-Layout-Tool.
Damit kann man sich nun Systemwerte visuell darstellen lassen!

![](feature.jpg "Photo eines Streamdecks. Auf den obere Knopfen sind nun Auslastung von GPU und Arbeitsspeicher (sowie Temperatur) nicht nur als Zahl dargestellt, sondern zusätzlich von einem Ring hinterlegt, welcher die relative Auslastung darstellt.")

Also Mikro-SD-Karte in den Computer stecken, neues Raspberry Pi OS Lite drauf installieren, 
und dann alles mit [Ansible](https://docs.ansible.com/) einrichten lassen.
Die Konfiguration dazu hatte ich in [Kapitel 2](/blog/2025/2025-09-16_lichtsteuerung-2/) erstellt.
Fertig? Nee.

Eine weitere Neuerung sind *Secure Defaults*; wenn man nichts einstellt, betreibt man Companion sicher,.. oder sicherer als zuvor.
Darunter fallen insbesondere Shell-Commands, die man über die Weboberfläche programmieren kann.
Jene verwende ich, um den Raspi einfach auszuschalten oder neuzustarten; und jetzt neu um den Systemstatus sekündlich abzufragen.

Companion läuft als Systemd-Service. Also, wie pflegt man da eine Anpassung ein? 
Über ... Anpassungsdateien! In diesem Fall benötige ich eine
`/etc/systemd/system/companion.service.d/env.conf` mit dem Inhalt

```ini
[Service]
Environment="COMPANION_ENABLE_SHELL_COMMAND_SUPPORT=YES"
```

In diese Anpassunskonfigs könnte man noch vieles anderes schreiben, aber das genügt hier.
Und nu wird nicht nur Licht auf der Bühne, sondern auch Licht ins Dunkel des Raspberry-Pi-Systems gebracht!

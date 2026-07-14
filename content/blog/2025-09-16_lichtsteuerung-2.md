---
title: Es werde Licht - Kapitel 2
date: 2025-09-16T08:45:27.754Z
---

Vor einigen Wochen schrieb ich über das Projekt, eine Steuerung für das Veranstaltungslicht im Familienzentrum zu entwickeln - von 36 digitalen Kanälen zu ein paar beleuchteten Tasten.

Seit dem haben wir das bei den eigenen Veranstaltungen ausprobiert, und intern Feedback gesammelt.
 - Die Helligkeit sollte einstellbar sein
 - Die Farben der RGB-Scheinwerfer sollten eingestellt werden können und gespeichert bleiben.

In dieser zweiten Iteration ist das Ziel nun klarer. Also habe ich die Konfiguration weitestgehend mit Ansible automatisiert und dokumentiert. Mir fehlt lediglich ein Weg um Companion (Die Software, die das Streamdeck ansteuert) automatisch mit der Konfig aus dem Repo zu bespielen.

Ich bin gespannt, wo dieses Projekt noch hinführt. 
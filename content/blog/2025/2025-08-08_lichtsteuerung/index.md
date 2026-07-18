---
title: Es werde Licht - Kapitel 1
date: 2025-08-08T07:50:13.130Z
categories:
- Projekte
tags: 
- Raspberry Pi
- Streamdeck
- Lichtsteuerung
- Familienzentrum Erlangen
- Ehrenamt
summary: |
  Hallo Welt!
---


Wie kann man eigentlich die Komplexität einer Lichtanlage aus Veranstaltungstechnik geschickt verstecken?

Im großen Saal des evangelischen Familienzentrums haben wir inzwischen acht Scheinwerfer an der Decke montiert. Deren Hauptaufgabe ist es, für die Livestreams der Gottesdienste auf Youtube für ein schönes Bild zu sorgen: Gut ausgeleuchtet und in warmen Farben. Mit 36 DMX-Kanälen ist das eine vergleichsweise kleine Anlage. Aber 36 Kanäle sind bereits erschlagend viele.

Wie kann das nun vereinfacht werden, ohne wichtige Funktionalität zu verlieren? Für unsere Zwecke ist grundlegend, die Lichtanlage mit einer Voreinstellung zu starten. Ein erster Bonus ist ein weiches an- und ausschalten von verschiedenen Gruppen.

In einem ersten Versuch habe ich vier Gruppen definiert. Im Bild ist jene aktiv, die für die Beleuchtung des Kreuzes an der Wand verantwortlich ist. Als Kern dieses Prototypen dient ein Raspberry Pi 5. Daran hängt ein Streamdeck, welches durch von Bitfocus Companion angesteuert wird. QLC+ dient als Lichtsteuersoftware, welche durch die Knöpfe auf dem Streamdeck gesteuert wird, und ihrerseits einen Fade-Effekt hinzufügt, und die Daten über ein USB-DMX-Interface zu den Scheinwerfern schickt.

Offen sind gegenwärtig noch, wie Updates, Backups und Konfigänderungen geschickt verwaltet werden können; und ob uns die Funktionalität reicht.

In welchem Bereich hast du mal dein Wissen eingesetzt, den man von außen nicht erwartet hätte?


{{< figure 
    src="feature.jpg"
    alt=""
    caption=""
>}}
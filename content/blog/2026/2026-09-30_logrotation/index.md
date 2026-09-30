---
title: Logrotation
date: 2026-09-30
categories:
- Projekte
tags: 
- Linux
summary: >-
    Im Kreis drehen für mehr Datenschutz!
draft: true
---

Anwendungslogs sind aufschlussreich.
Darin kann man allerlei über ein Programm und dessen Nutzung erfahren.
Manchmal auch über die Nutzer selbst.

Aaaber Daten über Nutzer darf man nicht beliebig aufbewahren oder verwenden.
Daher wäre es doch geschickt, diese Daten verschwinden, sobald sie nicht mehr nützlich sind.
(... oder erst garnicht entstehen.)

Im Folgenden schreibe ich über meine Erfahrungen zu Logs von [RDMO](https://github.com/rdmorganiser/rdmo/) und [FDOrganizer](https://gitos.rrze.fau.de/hits-fdm/fdorganizer), die ich beruflich betreue.

# journalctl

Die Programme laufen immer irgendwie als Systemservice; direkt, als Container, oder über Webserver dazwischen.
In irgendeiner Weise kann `journalctl` an Logdaten kommen.

Im Fall vom FDOranizer waren es zunächst recht viele (dazu später noch mal), also... 
kann man diese Logs gut rotieren und löschen?

Nein, leider nicht.

Logs aller Services werden durcheinander gespeichert. Es gibt
```sh
journalctl --vacuum-time=4w
```
Aber das betrifft dann alle Services, und nicht einen spezifisch.
... und man müsste den Befehl über Cron automatisch triggern, da solches nicht im System konfigurierbar ist.

Besser landen dort also keine relevanten Logdaten.

# logrotate

Aber logrotation muss nicht von jedem Programm neu erfunden werden.
Es gibt ja [`logrotate`](https://linux.die.net/man/8/logrotate).
Für einige installierbare Services wird eine passende Konfig mitgeliefert, hier müssen wir jene selbst erstellen.

So weit ich es verstanden habe, kennt Logrotate zwei Modi:
Datei umbenennen (und optional neu erstellen), oder Inhalte kopieren und alte Datei leeren.
Beide haben ihre Schwächen.

Umbenennen kann man unter Linux beliebige Dateien, auch von Programmen geöffnete.
Letztere können das abfragen, müssen aber nicht.
Passt man nicht auf, landen die Logs weiter in der alten Datei, von der man wegrotieren wollte.

Bei `copytruncate` kann man sich eine [Race Condition](https://de.wikipedia.org/wiki/Wettlaufsituation) einfangen.
Zwischen Kopieren und Löschen entstehende Logs können dann fehlen.

# Logrotate mit wsgi-Python

Fängt man naiv an, nutzt man vermutlich den `logging.FileHandler`.
Das ist thread-safe, aber nicht prozess-safe.
Für die allermeisten Fälle sollte das reichen, bis man viele Logeinträge pro Sekunde hat.

Mit diesem Loghandler haben wir nur das Problem, dass der die Datei einmal öffnet, und dann munter da rein schreibt.
Für Verwendung mit Logrotate ist `logging.handlers.WatchedFileHandler` besser.
Bestärkt hat mich darin auch ein [Blogeintrag in diesem Internetz](https://medium.com/@wtfyogesh/rotating-logs-for-python-based-application-running-with-gunicorn-or-uwsgi-9f4947512ae9).

## RDMO

Logging in RDMO nutzt die [Loggingeinstellungen von Django](https://docs.djangoproject.com/en/6.1/topics/logging/).
Zum Wechsel des LogHandlers habe ich mir einen Einzeiler geschrieben.
```sh
sed -i 's/logging.FileHandler/logging.handlers.WatchedFileHandler/g' rdmo-app/config/settings/local.py
```

Die Konfigurationsdatei für Logrotate `/etc/logrotate.d/rdmo` hat zunächst folgenden Inhalt
```
/var/log/rdmo/*.log {
        weekly
        dateext
        nomail
        missingok
        rotate 4
        nocompress
        create 664 rdmo rdmo
}
```
Das `weekly` und `rotate 4` habe ich von `/etc/logrotate.d/syslog` abgeschaut.
Nach fünf Wochen werden die Inhalte schon nicht mehr relevant sein.

# FDOrganizer

Etwas schwieriger zu Bändigen war der FDOrganizer.
Nutzt man die Beispielkonfig aus dem Repository, landet eine Zeile pro Anfrage auf der Konsole, und damit in `journalctl`.
Wie anfänglich geschrieben, sind die Logs da nicht schön zu rotieren oder zu löschen.
Aber es gibt einen Eintrag für die Konfig, um das in eine Datei umzuleiten,... Wenn man die gefunden hat, ist es einfach.
```ini
[uwsgi]
# ...
logto = /var/log/fdo/uwsgi.log
# ...
```

So weit ich es herausgefunden habe, reagiert uwsgi nicht auf das umbenennen von Dateien.
Hier nutzte ich die Funktion von Logrotate, dass nach Rotation ein Befehl ausgeführt werden kann, und starte den Service neu.
```
/var/log/fdo/*.log {
        weekly
        dateext
        nomail
        missingok
        rotate 4
        nocompress
        create 644 fdo fdo
        postrotate
            /bin/systemctl restart fdo.service
        endscript
}
```

# Abschluss

Über viele Jahre waren die Logs zuletzt gewachsen, und wurden unhandlich groß.
Jetzt nicht mehr, und ich habe wieder mal etwas gelernt (und zum Vertiefen und Festhalten aufgeschrieben).

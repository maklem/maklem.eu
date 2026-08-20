---
title: Kaputte Datenbanken
date: 2026-08-20
categories:
- HomeLab
tags: 
- Raspberry Pi
- Mastodon
- PostgreSQL
summary: >
    Über einen Backup-Cronjob wurde ich auf Defekte in meiner Datenbank aufmerksam.
    Aber wie rettet man den Rest der Datenbank?
---

Da kam also eine Mail von meinem Server.

```
pg_dump: error: Dumping the contents of table "conversations" failed: PQgetResult() failed.
pg_dump: detail: Error message from server: PANIC:  corrupted line pointer: 0
pg_dump: detail: Command was: COPY public.conversations (id, uri, created_at, updated_at, parent_status_id, parent_account_id) TO stdout;
pg_dumpall: error: pg_dump failed on database "mastodon", exiting
```

Ein Teil von meinem täglichen Backup läuft nicht durch; Datenbank "mastodon".
Mastodon selbst läuft ohne erkennbare Probleme, aber kaputt ist das dennoch.
Nur wie rettet man dann die Datenbank?

Mit duck.ai (GPT 5.6-Luna) kam ich zum Nachfolgenden.
Die Irrwege habe ich jedoch herausgelassen.
(Bei mir läuft Postgres in einem Container, mit Dateisystemmount für die Daten.
Die KI-Antworten gingen von einem lokalen Datenbank-Service aus, nicht von einem in einem Container.
Das habe ich einfach angepasst, wenn auch die Zeilen so sehr lang werden.)

## 1. Rohdaten sichern

Bevor es an Datenbankinhalte geht, habe ich die Dateien der Datenbank kopiert. Natürlich bei ausgeschaltetem Datenbank-Service, sonst bekommt man noch zusätzliche Defekte dazu.

```sh
cd /var/social/
systemctl stop social-database
cp -r database database_2026-08-20
systemctl start social-database
```

## 2. intakte Datenbankinhalte exportieren

`pg_dumpall` geht nicht mehr.
`pg_dump` der Tabelle `public.conversations` auch nicht.
Also musste ich alles schrittweise in Abschnitte zerlegt exportieren.

Zunächst also ein Ordner (für Übersichtlichkeit in der Zukunft), und dann die funktionstüchtigen Tabellen.
```sh
mkdir 2026-08-20_db_corruption
podman exec -i systemd-social-database pg_dumpall --globals-only -U mastodon > 2026-08-20_db_corruption/globals.sql
podman exec -i systemd-social-database pg_dump --exclude-table=public.conversations -U mastodon mastodon > 2026-08-20_db_corruption/db_wo_conversations.sql
podman exec -i systemd-social-database pg_dump -U mastodon --schema-only --table=public.conversations mastodon > 2026-08-20_db_corruption/conversations_schema.sql
```

## 3. Daten aus defekter Tabelle exportieren

Wie bereits erwähnt, funktioniert eine der Tabellen nicht.
Das KI-Tool der Wahl lieferte aber eine Funktionierende Idee.
Statt einem Dump der ganzen Tabelle, nehme nur die Zeilen mit ID kleiner als der Defekt.
Es erfordert einiges Ausprobieren, bis man die größte funktionierende ID findet.
Erst 200000, dann 300000, dann 250000, ... bis man es gefunden hat.
Aus Neugier habe ich dann noch "ID > Defekt" probiert, und doch einige weitere Zeilen exportieren können.
```sh
podman exec -i systemd-social-database psql -U mastodon mastodon -c "\copy ( SELECT * from public.conversations WHERE id < 289641 ) TO stdout CSV;" > 2026-08-20_db_corruption/partial_conversations.sql
podman exec -i systemd-social-database psql -U mastodon mastodon -c "\copy ( SELECT * from public.conversations WHERE id > 475231 ) TO stdout CSV;" > 2026-08-20_db_corruption/partial_conversations_2.sql
```

## 4. Daten zurückspielen

Jetzt habe ich, was zu Retten war. Nur brauche ich nun eine neue Datenbank mit diesen Inhalten.
Zunächst also ein Reset der Datenbank-Daten; durch umbenennen des Ordners und erstellen eines Neuen.
```bash
systemctl stop social-database.service 
mv database database_pre_renew_2026-08-20
mkdir database
chown 200991:200991 database
systemctl start social-database.service 
```

Dann Schema, Daten, und Tabellen aus dem intakten Bereich wieder einspielen.
```sh
podman exec -i systemd-social-database psql -U mastodon mastodon < 2026-08-20_db_corruption/conversations_schema.sql 
podman exec -i systemd-social-database psql -U mastodon mastodon -c "\copy public.conversations ( id, uri, created_at, updated_at, parent_status_id, parent_account_id ) FROM stdin WITH (FORMAT csv, HEADER true);" < 2026-08-20_db_corruption/partial_conversations.sql 
podman exec -i systemd-social-database psql -U mastodon mastodon -c "\copy public.conversations ( id, uri, created_at, updated_at, parent_status_id, parent_account_id ) FROM stdin WITH (FORMAT csv, HEADER true);" < 2026-08-20_db_corruption/partial_conversations_2.sql 
podman exec -i systemd-social-database psql -U mastodon mastodon < 2026-08-20_db_corruption/db_wo_conversations.sql 
```

Dabei rauschten zwei Zeilen mit einer Fehlermeldung an mir vorbei.
```
ERROR:  insert or update on table "account_conversations" violates foreign key constraint "fk_rails_1491654f9f"
DETAIL:  Key (conversation_id)=(290218) is not present in table "conversations".
```
Eine relevante Zeile konnte nicht zurückgespielt werden, weil das Gegenstück aus der zuvor defekten Tabelle fehlt.
Ein verschmerzbarer Verlust, denke ich.

## 5. Alles neustarten

Zum Abschluss noch alles neustarten und schauen, ob es funktioniert hat.

```sh
systemctl restart social-web.service social-redis.service social-streaming.service social-sidekiq.service social-redis.service 
```

Ja, eine Mastodoninstanz hat viele Services. Und so weit ich sehe, ist nichts defekt. Aber okay, ich habe davor auch nichts Auffälliges bemerkt, außer der Email vom Backupsystem.

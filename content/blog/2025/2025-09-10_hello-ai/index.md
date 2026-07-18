---
title: '"Hello AI" mit Kubernetes'
date: 2025-09-10T09:07:59.572Z
categories:
- Lernen und Experimente
tags: 
- Raspberry Pi
---

Was können die KI-Tools eigentlich wirklich, und durch welches Projekt kann ich das herausfinden? Ich könnte mir Kubernetes auf einem Raspberry Pi installieren, und eine Hello World App über CI deployen. Sind mir die Tools dabei eine gute Hilfe?

Die generierten Texte klingen immer überzeugend. Aber den Test der Realität halten diese nicht sicher stand. Mitunter hilft es verschiedene Modelle zu befragen, und darin Hinweise auf die Lösung zu finden.
Installation - K3S

In einer Vorabrecherche fand ich bereits k3s, eine leichtere Distribution von Kubernetes für schwache Rechner wie Raspberry Pis. Wenn ich eines der Sprachmodelle nach Empfehlungen frage, komme ich auch darauf. Das klingt schon mal nicht schlecht.

Zunächst updatete ich jedoch ein frisches Raspberry Pi OS auf Debian Trixie. In früheren Projekten war das wichtig. Die Installation von K3s lief ohne Probleme. Entgegen allen Anleitungen verzichtete ich auf zusätzliche Worker-Nodes. So viel untätige Hardware habe ich nicht übrig, und dem Projektziel "Verstehen und Lernen" dient das aktuell auch nicht.
Hello World!

An Vorschlägen für eine Hello World App habe ich verschiedene erhalten: fertige Demo-Container, JavaScript, Python, Go. Die Konfiguration für Deployment, Service, und CI-Pipeline waren stimmig und funktionieren. Für das Deployment musste ich noch Secrets zwischen Gitea, Actions Runner und K3s einrichten, aber das lief ohne besondere Schwierigkeiten. Verwendete Komponenten sind nicht immer die neusten (z.B.: actions/checkout@v3, statt v4 oder v5), und sicherlich übersehe ich einige Best-Practice (deployment in namespace?).

Nur wie greife ich nun auf die App zu? Innerhalb der Node kann ich die IP vom Pod nutzen, aber von außen? NodePort habe ich ausprobiert, aber das ist nicht zufriedenstellend. ChatGPT schlägt mir vor MetalLB zu installieren, nur läuft da schon etwas. Auf Port 80 bekomme ich Page not found und kubectl get svc zeigt den als verwendet an. ChatGPT besteht auf MetalLB, also suche ich selbst mal im Netz. Und siehe da: Bei k3s ist Traefik dabei - hat nur ein paar Nerven und etwas Zeit gekostet. (`kubectl get pods -n kube-system` kannte ich da noch nicht.) Mit der Information sehe ich endlich die erhoffte "Hello World" Nachricht!
Speichern

Was mache ich mit einer App, die nichts rechnet und nichts speichert? Richtig! Erweitern! Ein persistenter Speicher für ... naja, was auch immer. Ich könnte zählen, wie oft die Seite aufgerufen wurde. Als verteilte Speicher gibt es zum Beispiel etcd oder Ceph, aber ich verwende nur eine Node, und habe bislang keine höheren Ambitionen. Ich entschied mich für PersistentVolume mit hostPath. Das genügt.

Am Ende habe ich noch etwas Python-CI (mypy, flake8, pytest) hinzugefügt. Ein Python-Projekt ohne die grundlegenden CI-Tools kommt mir inzwischen seltsam vor.
Abschluss

In dem beschriebenen Versuch habe ich hauptsächlich ChatGPT verwendet. Vor dem Zusammenschreiben hier habe ich zusätzlich noch Perplexity und Claude Sonet 3.5 befragt. Das Ergebnis ändert sich damit leicht.

Ich habe gelernt:

* Die Tools beantworten Fragen halbwegs gut.
* Alle Tools irren sich mal, und sind nicht auf dem aktuellen Stand.
* Antworten werden besser, wenn man nach üblichen Empfehlungen und Best Practices fragt.
* Manchmal muss man doch selber suchen. Dummerweise vor allem dann, wenn die Information schwierig zu finden ist.

{{< figure 
    src="feature.jpg"
    alt=""
    caption=""
>}}
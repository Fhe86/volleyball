#!/usr/bin/env python3
"""Baut alle Seiten der Volleyball-Liga (Klasse 8 Jungs) neu.

Aufruf:  python3 quellen/build.py
Inhalte (Stunden, Spiele, Bewertung) stehen oben als Daten. Aussehen steht in
style.css, Verhalten in app.js. Beides liegt neben den fertigen HTML-Seiten.
Die Grafiken (Spielfelder, Haltungsbilder) werden unten als SVG erzeugt.
"""
import html
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- Farben

BLAU, GELB, GRUEN, KORALL = "#2f6bff", "#f5a800", "#12a672", "#ff5a5f"
TINTE = "#1b2433"
FARBEN = {1: BLAU, 2: GELB, 3: GRUEN, 4: KORALL}
TEAMS = [("Blau", BLAU), ("Gelb", GELB), ("Grün", GRUEN), ("Rot", KORALL)]

# ---------------------------------------------------------------- Inhalte

LESSONS = [
    {
        "n": 1, "farbe": "blau",
        "title": "Der Ball bleibt oben",
        "short": "Pritschen",
        "goal": "Die Jungs lernen das Pritschen (oberes Zuspiel) und spielen schon in der ersten Stunde Mini-Volleyball.",
        "highlight": "Rekordjagd im Ballkreis",
        "halle": "oben, Netz auf 2,10 m",
        "lehrplan": "Lehrplan 4.3 Spielen: oberes Zuspiel frontal, Spielformen. Lernbereich 2: Fairness und Zusammenspiel im Team.",
        "steps": [
            ("0 bis 10", "Einstieg: Ballkreis", ["Teams finden sich, wählen einen Namen und denken sich einen **Schlachtruf** aus (5 Sekunden lang).", "Rekordjagd mit **Ballkreis**: Wie lange hält das Team den Ball oben?"], "kreis", None),
            ("10 bis 20", "Pritschen in drei Merkpunkten", ["Technikkarte zeigen und einmal **vormachen**.", "Alle üben allein an der Wand: **Wand-Pritschen**."], "wand", "Merkpunkte stehen auf der Seite Technik."),
            ("20 bis 35", "Partner-Pritschen", ["Paare üben mit Zuwurf, danach ohne Fangen.", "Du gehst durch und gibst jedem einen Tipp zur Handhaltung."], "pendel", None),
            ("35 bis 70", "Fang-Volleyball", ["Zwei Felder, je zwei Teams. Der Ball darf gefangen werden.", "Nach 6 Minuten wechseln die Gegner, so spielt jedes Team zweimal."], "fang", None),
            ("70 bis 85", "Liga-Runde: Rekord schlagen", ["Noch einmal **Ballkreis**, diesmal mit dem Ziel, den Rekord vom Anfang zu knacken.", "Punkte in die Ligatabelle eintragen."], "kreis", None),
            ("85 bis 90", "Abschluss", ["Kurz dehnen (Handgelenke, Schultern).", "Jeder nennt einen Ball, der ihm gelungen ist."], None, None),
        ],
        "material": ["Volleybälle, am besten einer pro Paar (mindestens 8)", "Netz auf 2,10 m, quer geteilt für 2 Felder", "Leibchen in 4 Farben (Blau, Gelb, Grün, Rot)", "Klebeband oder Kreide für die Wandlinie", "Pfeife, Stoppuhr, ausgedruckte Ligatabelle"],
        "safety": ["Bälle nur auf Ansage hochwerfen. Nie in Richtung anderer Gruppen.", "Beim Fang-Volleyball den Netzbereich freihalten, nicht unter dem Netz durchlaufen.", "Finger locker halten, nicht steif. So verletzt man sich seltener."],
    },
    {
        "n": 2, "farbe": "gelb",
        "title": "Bagger-Boost",
        "short": "Baggern",
        "goal": "Die Jungs lernen das Baggern (unteres Zuspiel) und spielen 2 gegen 2 mit Spielerwechsel.",
        "highlight": "Zielbagger-Challenge",
        "halle": "oben, Netz auf 2,10 m",
        "lehrplan": "Lehrplan 4.3 Spielen: unteres Zuspiel frontal und mit Richtungsänderung, Kleinfeldspiele. Lernbereich 2: Teamgeist.",
        "steps": [
            ("0 bis 10", "Einstieg: Pritschen auffrischen", ["Paare spielen **Partner-Pritschen**, Ziel: 10 saubere Pritschen.", "Wer es geschafft hat, holt einen Punkt fürs Team."], "pendel", None),
            ("10 bis 20", "Baggern in drei Merkpunkten", ["Technikkarte zeigen, **vormachen**, einmal ohne Ball üben.", "Dann **Bagger-Pendel** mit Zuwurf."], "bagpendel", "Merkpunkte stehen auf der Seite Technik."),
            ("20 bis 35", "Bagger-Zielscheibe", ["Der Werfer ruft links oder rechts, der Bagger lenkt den Ball in die Zone.", "So lernen die Jungs die **Richtung** zu ändern."], "bagziel", None),
            ("35 bis 70", "Wechsel-Duell 2 gegen 2", ["Zwei Felder, je zwei Teams. Zwei spielen, zwei warten am Rand.", "Nach jedem Punkt wird getauscht, so ist keiner lange draußen."], "wechsel", None),
            ("70 bis 85", "Liga-Runde: Netzrallye", ["Beide Teams auf einem Feld spielen zusammen gegen die Uhr, jeder Spieler hat einen Kontakt.", "Wie viele Bälle gehen am Stück über das Netz? Rekord an die Tafel, Punkte eintragen."], "rallye", None),
            ("85 bis 90", "Abschluss", ["Handgelenke und Unterarme ausschütteln.", "Frage: Was hilft beim Baggern, die Beine oder die Arme?"], None, None),
        ],
        "material": ["Volleybälle, einer pro Paar (mindestens 8)", "Hütchen (mindestens 8) für die Zielzonen", "Netz auf 2,10 m, quer geteilt", "Leibchen in 4 Farben, Pfeife, Stoppuhr", "Ligatabelle zum Eintragen"],
        "safety": ["Beim Baggern stehen die Arme tief. Nicht in das Gesicht des Partners werfen.", "Zielzonen nicht betreten, sonst rutscht man auf den Hütchen aus.", "Unterarme nach 10 Minuten kurz ausschütteln, das tut gut."],
    },
    {
        "n": 3, "farbe": "gruen",
        "title": "Annahme, Pass, Angriff",
        "short": "Angabe und Annahme",
        "goal": "Die Jungs lernen die Angabe von unten und die Dreierkette aus Annahme, Zuspiel und Rückgabe. Die Techniknote wird heute abgenommen.",
        "highlight": "Dreierkette und Technikprobe",
        "halle": "oben, Netz auf 2,10 m",
        "lehrplan": "Lehrplan 4.3 Spielen: Angabe von unten, Annahme des aufgeschlagenen Balls, Stellen eines zugespielten Balls, Kleinfeldspiel bis 3:3.",
        "steps": [
            ("0 bis 10", "Einspielen", ["Paare spielen 5 Minuten **Partner-Pritschen** und 5 Minuten **Bagger-Pendel**.", "Locker, ohne Zeitdruck. Du siehst gleich, wer sicher ist."], "pendel", None),
            ("10 bis 25", "Angabe von unten", ["Technik kurz zeigen: Ball loslassen, mit der flachen Hand von unten schlagen.", "**Angabe-Zielscheibe** über das Netz in drei Zonen."], "angabe", None),
            ("25 bis 45", "Dreierkette", ["Dreier-Gruppen, der vierte beobachtet und zählt.", "Angabe, Annahme, Zuspiel: so läuft später jedes Spiel."], "kette", None),
            ("45 bis 80", "Drei Kontakte Pflicht und Technikprobe", ["Zwei Felder, je zwei Teams, 3 gegen 3, der vierte pfeift.", "Parallel nimmst du die **Technikprobe** ab: Jedes Paar kommt 3 Minuten an die Station."], "drei", "Probe: 5 Zuwürfe pro Technik. Punkte stehen auf der Seite Bewertung."),
            ("80 bis 90", "Abschluss", ["Ligatabelle gemeinsam ausfüllen.", "Ausblick: Nächstes Mal ist der Spieltag mit Siegerehrung."], None, None),
        ],
        "material": ["Volleybälle (mindestens 8)", "Hütchen oder Matten für 3 Angabe-Zonen", "Netz auf 2,10 m, quer geteilt", "Bewertungsbogen (ausgedruckt) und Stift für die Technikprobe", "Leibchen in 4 Farben, Pfeife, Stoppuhr"],
        "safety": ["Angabe nur zum Netz hin schlagen, nie quer durch die Halle.", "Beim 3 gegen 3 vor der Annahme laut **Meiner!** rufen, das verhindert Zusammenstöße.", "Netzkante nicht berühren, Abstand halten."],
    },
    {
        "n": 4, "farbe": "korall",
        "title": "Spieltag",
        "short": "Das Turnier",
        "goal": "Die Jungs zeigen alles, was sie gelernt haben, im 3-gegen-3-Turnier mit Schiedsrichtern und Siegerehrung. Die Spielnote wird gemacht.",
        "highlight": "Turnier, Finale, Siegerehrung",
        "halle": "oben, Netz auf 2,10 m",
        "lehrplan": "Lehrplan 4.3 Spielen: Kleinfeldspiel 3:3, Annahme, Zuspiel. Lernbereich 2: Regeln einhalten, Entscheidungen akzeptieren, Fairness.",
        "steps": [
            ("0 bis 10", "Einspielen im Team", ["Jedes Team spielt **Ballkreis** und stellt sich vor.", "Rekord der Stunde 1 vergleichen."], "kreis", None),
            ("10 bis 20", "Spielplan und Regeln", ["Spielplan zeigen: Jeder gegen jeden, 3 Runden.", "**Schiri-Zeichen** kurz erklären: Punkt, Netzberührung, Ball im Aus."], None, "Der vierte Spieler jedes Teams pfeift und zählt."),
            ("20 bis 65", "Turnier: 3 Runden", ["Jede Runde 10 Minuten spielen und 5 Minuten Wechsel.", "Schiri wechselt nach jeder Runde. Für die **Spielnote** schaust du Runde 1 auf Feld A, Runde 2 und 3 auf Feld B zu. So siehst du jedes Team mindestens einmal."], "turnier", None),
            ("65 bis 80", "Finale", ["Platz 1 gegen Platz 2 auf Feld A, Platz 3 gegen Platz 4 auf Feld B.", "Alle anderen schauen zu und feuern an. Hier fällt dir das Spielverhalten besonders gut auf."], None, None),
            ("80 bis 90", "Siegerehrung", ["Ligatabelle zusammenzählen, Siegerteam ausrufen. Das Siegerteam ruft seinen Schlachtruf.", "Jeder bekommt einen persönlichen Satz zu seinem besten Moment."], None, None),
        ],
        "material": ["Volleybälle (mindestens 4)", "Netz auf 2,10 m, quer geteilt", "Leibchen in 4 Farben", "Pfeife, Stoppuhr, Punktetafel oder Zettel", "Ausgedruckter Bewertungsbogen"],
        "safety": ["Pausen zum Trinken zwischen den Runden einplanen.", "Schiri steht seitlich am Netz, nie unter dem Netz.", "Fairplay: Gegner nach dem Spiel abklatschen."],
    },
]

GAMES = {
    "kreis": {
        "name": "Ballkreis", "stunde": 1, "min": "8 Minuten", "wer": "ganzes Team (4)", "tag": "Aufwärmen", "svg": "kreis",
        "ziel": "Das Team hält den Ball so lange wie möglich in der Luft.",
        "aufbau": "Ein Team steht im Kreis, 2 Meter Abstand. Ein Ball.",
        "schritte": ["Einer wirft den Ball hoch. Der Nächste pritscht ihn weiter zum nächsten Spieler.", "Fällt der Ball, geht es von vorn los. Einer zählt die Pritschen laut mit.", "Rekord merken. Dann noch einmal, jetzt mit dem Ziel, den Rekord zu schlagen."],
        "punkte": "Ab 10 Pritschen: 1 Punkt. Ab 20: 2 Punkte. Ab 30: 3 Punkte.",
        "leichter": "Der Ball darf einmal aufspringen.", "schwerer": "Nach jedem Zuspiel einen Platz weiterlaufen.",
    },
    "wand": {
        "name": "Wand-Pritschen", "stunde": 1, "min": "6 Minuten", "wer": "jeder allein", "tag": "Technik", "svg": "wand",
        "ziel": "Allein das Pritschen üben, bis die Haltung sitzt.",
        "aufbau": "Jeder steht 2 Meter vor einer Wand. Klebeband in 2,5 Metern Höhe.",
        "schritte": ["Ball über der Stirn halten und mit beiden Händen gegen die Wand pritschen.", "Die Linie treffen, den Ball zurückkommen lassen und wieder pritschen.", "Wettlauf: Wer als Erster 10 Treffer in Folge schafft, ruft STOPP. Dann geht es von vorn los."],
        "punkte": "Wer STOPP ruft, holt 1 Punkt fürs Team (höchstens 2 Punkte).",
        "leichter": "Ball zwischendurch fangen.", "schwerer": "Mit Abstand 3 Meter.",
    },
    "pendel": {
        "name": "Partner-Pritschen", "stunde": 1, "min": "10 Minuten", "wer": "2 Spieler", "tag": "Technik", "svg": "partner",
        "ziel": "Zu zweit den Ball sauber hin und her pritschen.",
        "aufbau": "Zwei Spieler stehen 3 Meter auseinander. Ein Ball pro Paar.",
        "schritte": ["A wirft den Ball hoch über die Stirn von B.", "B pritscht zurück: Hände als Dreieck über der Stirn, Beine strecken.", "A fängt und wirft wieder. Nach 5 Mal tauschen. Wer schafft 10 saubere Pritschen?"],
        "punkte": "Jedes Paar mit 10 sauberen Pritschen bringt 1 Punkt fürs Team.",
        "leichter": "Abstand 2 Meter.", "schwerer": "Beide pritschen, ohne zu fangen.",
    },
    "fang": {
        "name": "Fang-Volleyball", "stunde": 1, "min": "35 Minuten", "wer": "3 gegen 3", "tag": "Spiel", "svg": "netz",
        "ziel": "Mini-Volleyball über das Netz. Der Ball darf gefangen werden.",
        "aufbau": "Feld 6 Meter breit, 5 Meter pro Seite, Netz auf 2,10 Meter. Zwei Teams, der vierte pfeift.",
        "schritte": ["Das Spiel beginnt mit einem Einwurf von unten über das Netz.", "Wer den Ball fängt, wirft ihn hoch zu einem Mitspieler.", "Der pritscht den Ball über das Netz. Landet er im Feld des Gegners, gibt es einen Punkt. Joker: Im Gegnerfeld steht ein Hütchen. Wer es trifft, bekommt 2 Punkte."],
        "punkte": "Sieg: 2 Punkte. Unentschieden: 1 Punkt. Gespielt wird 6 Minuten.",
        "leichter": "Zwischen den Pritschen darf der Ball aufspringen.", "schwerer": "Nach dem Fangen sofort pritschen, ohne zu werfen.",
    },
    "bagpendel": {
        "name": "Bagger-Pendel", "stunde": 2, "min": "10 Minuten", "wer": "2 Spieler", "tag": "Technik", "svg": "partner",
        "ziel": "Zu zweit den Ball sicher baggern.",
        "aufbau": "Zwei Spieler stehen 3 Meter auseinander. Ein Ball pro Paar.",
        "schritte": ["A wirft den Ball flach zu B, auf Hüfthöhe.", "B geht in die Knie, streckt die Arme wie ein Brett und baggert zurück. Der Schwung kommt aus den Beinen.", "A fängt. Nach 5 Mal tauschen. Ziel: 10 saubere Bagger."],
        "punkte": "Jedes Paar mit 10 sauberen Baggern bringt 1 Punkt fürs Team.",
        "leichter": "Abstand 2 Meter.", "schwerer": "Beide baggern, ohne zu fangen.",
    },
    "bagziel": {
        "name": "Bagger-Zielscheibe", "stunde": 2, "min": "15 Minuten", "wer": "2 Spieler", "tag": "Technik", "svg": "zonen",
        "ziel": "Den Ball in die richtige Zone baggern.",
        "aufbau": "Zwei Zonen (2 mal 2 Meter) mit je vier Hütchen, links und rechts. Der Bagger steht 4 Meter davor.",
        "schritte": ["Der Werfer ruft laut LINKS oder RECHTS und wirft den Ball sanft zum Bagger.", "Der Bagger dreht die Arme zur richtigen Seite und baggert den Ball in die Zone.", "5 Versuche, dann tauschen. Alle Treffer zählen."],
        "punkte": "Je 4 Treffer des Teams ergeben 1 Punkt, höchstens 3 Punkte.",
        "leichter": "Nur eine Zone, die vorher bekannt ist.", "schwerer": "Der Werfer ruft erst, wenn der Ball schon fliegt.",
    },
    "wechsel": {
        "name": "Wechsel-Duell 2 gegen 2", "stunde": 2, "min": "35 Minuten", "wer": "2 gegen 2", "tag": "Spiel", "svg": "netz2",
        "ziel": "Schnelles Spiel, in dem jeder oft den Ball bekommt.",
        "aufbau": "Zwei Teams mit je 4 Spielern. Auf dem Feld stehen je 2, die anderen 2 warten am Rand. Feld 4 Meter breit.",
        "schritte": ["Ein Spieler gibt von unten an. Der Ball darf gebaggert oder gepritscht werden und einmal aufspringen.", "Nach jedem Punkt wechseln die beiden Spieler im Feld mit den Wartenden.", "Gespielt wird bis 5 Punkte. Danach tauschen die Teams das Feld."],
        "punkte": "Sieg: 2 Punkte. Unentschieden: 1 Punkt.",
        "leichter": "Ball darf zweimal aufspringen.", "schwerer": "Ball darf nicht aufspringen.",
    },
    "rallye": {
        "name": "Netzrallye", "stunde": 2, "min": "12 Minuten", "wer": "2 Teams gemeinsam", "tag": "Aufwärmen", "svg": "rallye",
        "ziel": "Beide Teams spielen zusammen gegen die Uhr: Wie viele Bälle gehen am Stück über das Netz?",
        "aufbau": "Je ein Team steht in einer Schlange hinter der Grundlinie, auf jeder Netzseite. Ein Ball, Netz auf 2,10 Meter.",
        "schritte": ["Der Erste gibt von unten an. Der Ball geht über das Netz.", "Wer den Ball spielt (Bagger oder Pritsche), läuft danach unter dem Netz hindurch auf die andere Seite und stellt sich hinten an.", "Fällt der Ball, gibt es einen neuen Versuch. Alle zählen laut mit. Rekord der Stunde auf die Tafel schreiben."],
        "punkte": "Ab 6 Bällen: 1 Punkt für beide Teams. Ab 10: 2 Punkte. Ab 15: 3 Punkte.",
        "leichter": "Ball darf einmal aufspringen.", "schwerer": "Abwechselnd Bagger und Pritsche.",
    },
    "angabe": {
        "name": "Angabe-Zielscheibe", "stunde": 3, "min": "15 Minuten", "wer": "jeder allein", "tag": "Technik", "svg": "angabe",
        "ziel": "Die Angabe von unten üben und das Feld treffen.",
        "aufbau": "Der Angeber steht hinter der Grundlinie, 5 Meter vor dem Netz. Auf der anderen Seite liegen drei Zonen mit den Zahlen 1, 2, 3. Zone 3 ist ganz hinten.",
        "schritte": ["Stelle dich seitlich auf, Schlagarm hinten. Der Ball liegt auf der anderen Hand.", "Ball loslassen und mit der flachen Hand von unten über das Netz schlagen.", "Triff eine Zone. 5 Versuche pro Spieler, dann wechseln."],
        "punkte": "Zone 1 = 1 Punkt, Zone 2 = 2 Punkte, Zone 3 = 3 Punkte. Ab 15 Teampunkten gibt es 1 Ligapunkt, ab 25: 2, ab 35: 3.",
        "leichter": "Näher ans Netz (3 Meter).", "schwerer": "Nur Zone 2 und 3 zählen.",
    },
    "kette": {
        "name": "Dreierkette", "stunde": 3, "min": "20 Minuten", "wer": "3 Spieler + 1 Beobachter", "tag": "Technik", "svg": "dreieck",
        "ziel": "Angabe, Annahme, Zuspiel: so läuft später jedes Spiel.",
        "aufbau": "Drei Spieler stehen im Dreieck, 3 Meter Abstand. Der vierte im Team zählt und gibt Tipps.",
        "schritte": ["A wirft den Ball zu B (später: Angabe von unten).", "B baggert den Ball hoch zu C. Das ist die Annahme.", "C pritscht den Ball zurück zu A. Danach rotieren alle: A wird B, B wird C, C wird A."],
        "punkte": "Gelungene Ketten in 3 Minuten: ab 6 = 1 Punkt, ab 10 = 2 Punkte, ab 14 = 3 Punkte.",
        "leichter": "Ball darf einmal aufspringen.", "schwerer": "Der Ball geht über ein Seil oder eine Leine.",
    },
    "drei": {
        "name": "Drei Kontakte Pflicht", "stunde": 3, "min": "35 Minuten", "wer": "3 gegen 3", "tag": "Spiel", "svg": "netz",
        "ziel": "Echtes Volleyball: Annahme, Zuspiel, dann über das Netz.",
        "aufbau": "Feld 6 Meter breit, 5 Meter pro Seite, Netz auf 2,10 Meter. Zwei Teams, der vierte pfeift.",
        "schritte": ["Angabe von unten hinter der Grundlinie.", "Pflicht: Annahme (Bagger), Zuspiel (Pritsche), dann erst über das Netz. Der Ball geht zuerst zum Mitspieler, dann zum Gegner.", "Punkt, wenn der Ball im Gegnerfeld landet oder der Gegner einen Fehler macht. Nach dem Punkt rotiert das Team im Uhrzeigersinn."],
        "punkte": "Sieg: 2 Punkte. Unentschieden: 1 Punkt. Gespielt wird 8 Minuten.",
        "leichter": "Ball darf einmal aufspringen.", "schwerer": "Dritter Kontakt muss ein Pritschen sein.",
        "tipp": "Rufen hilft: Wer den Ball annimmt, ruft vorher laut MEINER.",
    },
    "turnier": {
        "name": "Spieltag-Turnier", "stunde": 4, "min": "45 Minuten", "wer": "4 Teams, 3 gegen 3", "tag": "Spiel", "svg": "turnier",
        "ziel": "Jedes Team spielt gegen jedes andere. Am Ende gibt es ein Finale.",
        "aufbau": "Zwei Felder quer, drei Runden. In jeder Runde spielen alle vier Teams.",
        "schritte": ["Drei Spieler pro Team spielen, der vierte pfeift und zählt.", "Nach jeder Runde wechselt der Schiri. Wer noch nie dran war, kommt zuerst.", "Jede Runde dauert 10 Minuten, dann gibt es 5 Minuten für Wechsel und Trinken."],
        "punkte": "Sieg: 3 Punkte. Unentschieden: 1 Punkt. Niederlage: 0 Punkte.",
        "leichter": "Ball darf einmal aufspringen.", "schwerer": "Alle drei Kontakte sind Pflicht.",
        "extra": "plan",
    },
}

TECHNIK = [
    {
        "key": "pritschen", "name": "Pritschen", "sub": "oberes Zuspiel", "svg": "pritsch", "farbe": "blau",
        "merk": ["Hände über die Stirn. Finger und Daumen bilden ein Dreieck.", "Beine beugen und unter den Ball gehen.", "Arme und Beine strecken, der Ball fliegt hoch."],
        "fehler": [("Der Ball geht gegen die Brust.", "Zu tief gestanden. Näher an den Ball gehen."), ("Die Hände sind steif.", "Finger locker, Hände wie eine Schale."), ("Der Ball fliegt nur flach.", "Mehr Streckung aus den Beinen.")],
        "pruefung": "Ein Partner wirft 5 Mal aus 4 Metern zu. Der Schüler pritscht den Ball in eine Zone (2 mal 2 Meter) neben dem Werfer.",
        "kriterien": [("Dreieck", "Hände bilden ein Dreieck über der Stirn"), ("Beine", "Knie beugen, dann strecken"), ("Treffpunkt", "Ball wird über der Stirn getroffen"), ("Flug", "Ball steigt hoch und gerade"), ("Blick", "Blick zum Ball und zum Ziel")],
    },
    {
        "key": "baggern", "name": "Baggern", "sub": "unteres Zuspiel", "svg": "bagger", "farbe": "gelb",
        "merk": ["Hände fest zusammen. Arme gestreckt wie ein Brett.", "Knie beugen. Der Ball kommt vor dem Körper.", "Schwung aus den Beinen, die Arme nicht hochreißen."],
        "fehler": [("Der Ball fliegt nach hinten.", "Arme schwingen zu hoch. Beine nutzen."), ("Der Ball trifft die Hände.", "Ball mit der Mitte der Unterarme treffen."), ("Die Arme sind gebeugt.", "Ellbogen strecken, Daumen nebeneinander.")],
        "pruefung": "Ein Partner wirft 5 Mal aus 4 Metern zu. Der Schüler baggert den Ball in eine Zone (2 mal 2 Meter) neben dem Werfer.",
        "kriterien": [("Arme", "Hände zusammen, Arme gestreckt"), ("Beine", "Knie gebeugt, Schwung aus den Beinen"), ("Treffpunkt", "Ball trifft die Unterarme vor dem Körper"), ("Flug", "Ball steigt kontrolliert hoch"), ("Blick", "Blick zum Ball und zum Ziel")],
    },
]

SPIEL_KRITERIEN = [
    ("Annahme und Zuspiel", "3 = fast immer sauber, 0 = der Ball geht oft verloren"),
    ("Absprache und Stellung", "3 = ruft Meiner und steht richtig, 0 = bleibt stehen"),
    ("Fairness und Regeln", "3 = fair und akzeptiert Entscheidungen, 0 = stört"),
    ("Einsatz und Teamgeist", "3 = immer dabei und motiviert andere, 0 = wenig Einsatz"),
]

# Bewertung: zwei Noten
MAXE = {"pritschen": 10, "baggern": 10, "spiel": 12}
TECHNIK_MAX = 20


def schluessel(maximum):
    """Mindestpunkte fuer Note 1 bis 5 nach Fabis Standard (90/80/60/40/20 Prozent)."""
    return [math.ceil(round(p * maximum, 6)) for p in (0.9, 0.8, 0.6, 0.4, 0.2)]


# ---------------------------------------------------------------- Helfer

def esc(text):
    return html.escape(text, quote=True)


def rich(text):
    """Escaped Text, **fett** wird zu <b>."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc(text))


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#fff8ee">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
</head>
<body>
"""


def nav(current):
    items = [("stunde-%d.html" % l["n"], "Stunde %d" % l["n"], "stunde-%d" % l["n"]) for l in LESSONS]
    items += [("spiele.html", "Spiele", "spiele"), ("technik.html", "Technik", "technik"),
              ("timer.html", "Timer", "timer"), ("liga.html", "Liga", "liga"), ("bewertung.html", "Bewertung", "bewertung")]
    links = []
    for href, label, key in items:
        cur = ' aria-current="page"' if key == current else ""
        links.append(f'<li><a class="link" href="{href}"{cur}>{label}</a></li>')
    return f"""<header class="nav"><div class="wrap">
<a class="brand" href="index.html"><img src="icon.svg" alt="" width="30" height="30">Volleyball <b>Liga</b></a>
<nav aria-label="Hauptnavigation"><ul>{''.join(links)}</ul></nav>
</div></header>
"""


def foot():
    return """<footer class="foot"><div class="wrap">
<span>Sport, Klasse 8, Mittelschule. Material für den Unterricht.</span>
<span>Lehrplan: LehrplanPLUS Bayern, Sport Jgst. 8</span>
</div></footer>
<script src="app.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------- Grafiken (SVG)

def svg(w, h, inner, label):
    return (f'<svg class="gfx" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0L10 5L0 10z" fill="{TINTE}"/></marker></defs>{inner}</svg>')


def dot(x, y, color, text="", r=13, op=1):
    t = f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">{text}</text>' if text else ""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" opacity="{op}" stroke="#fff" stroke-width="2.5"/>{t}'


def ball(x, y):
    return (f'<circle cx="{x}" cy="{y}" r="9" fill="#fff" stroke="{TINTE}" stroke-width="2"/>'
            f'<path d="M{x - 9} {y}Q{x} {y - 5} {x + 9} {y}M{x} {y - 9}Q{x - 5} {y} {x} {y + 9}" fill="none" stroke="{TINTE}" stroke-width="1.4"/>')


def arrow(x1, y1, x2, y2, bend=0, dash=False):
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2 - bend
    d = ' stroke-dasharray="6 5"' if dash else ""
    return f'<path d="M{x1} {y1}Q{cx} {cy} {x2} {y2}" fill="none" stroke="{TINTE}" stroke-width="2.4" stroke-linecap="round"{d} marker-end="url(#ah)"/>'


def text(x, y, s, size=13, anchor="middle", weight=600, color=TINTE):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}">{esc(s)}</text>'


def court(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fdebc0" stroke="#fff" stroke-width="4"/>')


def net_line(x, y1, y2):
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{TINTE}" stroke-width="5" stroke-linecap="round"/>'
            f'<circle cx="{x}" cy="{y1}" r="5" fill="{TINTE}"/><circle cx="{x}" cy="{y2}" r="5" fill="{TINTE}"/>')


def g_kreis():
    cx, cy, rr = 160, 105, 66
    cols = [BLAU, GELB, GRUEN, KORALL]
    pts = [(cx + rr * math.cos(math.radians(a)), cy + rr * math.sin(math.radians(a))) for a in (-90, 0, 90, 180)]
    out = f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="#fff" stroke-width="10"/>'
    out = f'<rect width="320" height="210" rx="14" fill="#fdebc0"/>' + out
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        out += arrow(round(a[0] + (b[0] - a[0]) * .25), round(a[1] + (b[1] - a[1]) * .25), round(a[0] + (b[0] - a[0]) * .75), round(a[1] + (b[1] - a[1]) * .75), bend=0)
    for i, (x, y) in enumerate(pts):
        out += dot(round(x), round(y), cols[i], str(i + 1), 16)
    out += ball(cx, cy - 12) + text(cx, cy + 20, "Ball oben", 12)
    return svg(320, 210, out, "Vier Spieler stehen im Kreis und spielen sich den Ball zu")


def g_partner():
    out = '<rect width="320" height="190" rx="14" fill="#fdebc0"/>'
    out += dot(60, 120, BLAU, "A", 17) + dot(260, 120, GELB, "B", 17)
    out += arrow(80, 108, 240, 108, bend=90)
    out += ball(160, 62)
    out += f'<line x1="60" y1="160" x2="260" y2="160" stroke="{TINTE}" stroke-width="2" marker-start="url(#ah)" marker-end="url(#ah)"/>'
    out += text(160, 180, "3 Meter", 13)
    return svg(320, 190, out, "Zwei Spieler stehen drei Meter auseinander und spielen sich den Ball zu")


def g_wand():
    out = '<rect width="320" height="190" rx="14" fill="#fdebc0"/>'
    out += f'<rect x="268" y="10" width="40" height="150" rx="6" fill="#cfd9e8"/>'
    out += f'<line x1="268" y1="48" x2="308" y2="48" stroke="{KORALL}" stroke-width="5"/>'
    out += text(16, 30, "Linie in 2,5 m Höhe", 13, "start")
    out += dot(110, 130, BLAU, "", 18)
    out += arrow(126, 112, 262, 60, bend=55) + ball(150, 62)
    out += f'<line x1="110" y1="170" x2="268" y2="170" stroke="{TINTE}" stroke-width="2" marker-start="url(#ah)" marker-end="url(#ah)"/>' + text(190, 187, "2 Meter", 12)
    return svg(320, 190, out, "Ein Spieler pritscht den Ball gegen eine Wand und trifft eine Linie")


def _team(xs, ys, color, n, op=1):
    return "".join(dot(x, y, color, "", 13, op) for x, y in list(zip(xs, ys))[:n])


def g_netz(n=3, bench=0):
    out = '<rect width="340" height="230" rx="14" fill="#cde7ff"/>' + court(18, 18, 304, 168) + net_line(170, 14, 190)
    ys_all = [52, 102, 152]
    lx = [100, 60, 100] if n == 3 else [90, 90]
    ly = ys_all if n == 3 else [70, 134]
    out += _team(lx, ly, BLAU, n)
    rx = [240, 280, 240] if n == 3 else [250, 250]
    out += _team(rx, ly, KORALL, n)
    out += arrow(116, ly[0], 232, ly[0], bend=36, dash=True) + ball(170, ly[0] - 42)
    out += text(170, 10, "Netz", 11)
    if bench:
        out += text(70, 205, "warten", 11) + text(270, 205, "warten", 11)
        for x in (50, 90):
            out += dot(x, 218, BLAU, "", 8, .55)
        for x in (250, 290):
            out += dot(x, 218, KORALL, "", 8, .55)
    return svg(340, 230, out, "Zwei Teams spielen über das Netz")


def g_zonen():
    out = '<rect width="320" height="200" rx="14" fill="#fdebc0"/>'
    out += dot(40, 100, BLAU, "W", 16) + dot(130, 100, GELB, "B", 16)
    out += arrow(58, 100, 110, 100, bend=14) + ball(84, 76)
    out += f'<rect x="220" y="14" width="86" height="76" rx="10" fill="{GRUEN}" opacity=".85"/><rect x="220" y="110" width="86" height="76" rx="10" fill="{KORALL}" opacity=".85"/>'
    out += text(263, 58, "LINKS", 16, color="#fff") + text(263, 154, "RECHTS", 16, color="#fff")
    out += arrow(146, 92, 214, 54, bend=18, dash=True) + arrow(146, 110, 214, 148, bend=-18, dash=True)
    out += text(40, 132, "Werfer", 12) + text(130, 132, "Bagger", 12)
    return svg(320, 200, out, "Ein Werfer ruft links oder rechts, der Bagger spielt in die Zone")


def g_angabe():
    out = '<rect width="340" height="200" rx="14" fill="#cde7ff"/>' + court(14, 14, 312, 172) + net_line(150, 10, 190)
    out += dot(44, 100, BLAU, "", 15)
    for i, (x, c, n) in enumerate([(176, "#ffe08a", "1"), (232, "#9be3c1", "2"), (288, "#ffb3b5", "3")]):
        out += f'<rect x="{x - 24}" y="30" width="48" height="140" rx="8" fill="{c}" stroke="#fff" stroke-width="3"/>' + text(x, 108, n, 26, weight=800)
    out += arrow(60, 90, 248, 68, bend=60) + ball(120, 44)
    out += text(150, 8, "Netz", 11) + text(44, 134, "Angeber", 12)
    return svg(340, 200, out, "Der Angeber schlägt von unten über das Netz in eine von drei Zonen")


def g_dreieck():
    out = '<rect width="320" height="210" rx="14" fill="#fdebc0"/>'
    A, B, C = (160, 44), (58, 156), (262, 156)
    out += arrow(138, 62, 78, 134, bend=14) + arrow(84, 156, 236, 156, bend=30) + arrow(250, 134, 180, 62, bend=14)
    out += dot(*A, BLAU, "A", 17) + dot(*B, GELB, "B", 17) + dot(*C, GRUEN, "C", 17)
    out += text(78, 82, "1 Wurf", 12, "end") + text(160, 188, "2 Bagger", 12) + text(250, 82, "3 Pritsche", 12, "start")
    return svg(320, 210, out, "Dreierkette: A wirft zu B, B baggert zu C, C pritscht zu A")


def g_turnier():
    out = ""
    for ox, label in ((0, "Feld A"), (190, "Feld B")):
        out += f'<rect x="{ox + 6}" y="26" width="168" height="130" rx="10" fill="#fdebc0" stroke="#fff" stroke-width="3"/>' + net_line(ox + 90, 22, 160)
        out += _team([ox + 48, ox + 30, ox + 48], [58, 92, 126], BLAU if ox == 0 else GRUEN, 3)
        out += _team([ox + 132, ox + 150, ox + 132], [58, 92, 126], GELB if ox == 0 else KORALL, 3)
        out += text(ox + 90, 16, label, 13)
    out += text(180, 184, "Zwei Felder, vier Teams, drei Runden", 13)
    return svg(380, 196, out, "Zwei Spielfelder nebeneinander für das Turnier")


def g_rallye():
    out = '<rect width="340" height="220" rx="14" fill="#cde7ff"/>' + court(18, 18, 304, 170) + net_line(170, 14, 192)
    for i, y in enumerate((50, 85, 120, 155)):
        out += dot(52, y, BLAU, str(i + 1), 13) + dot(288, y, KORALL, str(i + 1), 13)
    out += arrow(70, 50, 270, 50, bend=44) + ball(170, 24)
    out += arrow(300, 172, 190, 205, bend=-6, dash=True) + arrow(150, 205, 40, 172, bend=-6, dash=True)
    out += text(170, 214, "Wer gespielt hat, läuft auf die andere Seite", 11)
    return svg(340, 220, out, "Zwei Teams stehen in Schlangen auf beiden Seiten des Netzes und spielen sich den Ball zu")


def g_pritsch():
    s = f'stroke="{TINTE}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    out = '<rect width="470" height="270" rx="14" fill="#e4ecff"/>'
    out += f'<line x1="20" y1="248" x2="450" y2="248" stroke="#fff" stroke-width="6"/>'
    out += f'<circle cx="110" cy="74" r="18" fill="#ffd9b8" stroke="{TINTE}" stroke-width="4"/>'
    out += f'<path d="M110 94L106 158" {s} stroke="{BLAU}"/>'
    out += f'<path d="M106 158L90 204L96 246M106 158L128 204L136 246" {s}/>'
    out += f'<path d="M108 106L78 78L96 38M108 106L142 78L124 38" {s} stroke="{BLAU}" stroke-width="8"/>'
    out += f'<path d="M96 38L110 30L124 38" fill="none" stroke="{KORALL}" stroke-width="5" stroke-dasharray="3 5"/>'
    out += ball(110, 8)
    for y, t, ty in ((40, "1  Hände: Dreieck über der Stirn", 44), (160, "2  Beine gebeugt, unter den Ball", 164), (224, "3  Dann Beine und Arme strecken", 228)):
        out += f'<line x1="160" y1="{y}" x2="190" y2="{y}" stroke="{TINTE}" stroke-width="2"/>' + text(198, ty, t, 14, "start")
    return svg(470, 270, out, "Pritschen: Hände als Dreieck über der Stirn, Knie gebeugt")


def g_bagger():
    s = f'stroke="{TINTE}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    out = '<rect width="470" height="270" rx="14" fill="#fff2cc"/>'
    out += f'<line x1="20" y1="248" x2="450" y2="248" stroke="#fff" stroke-width="6"/>'
    out += f'<circle cx="112" cy="84" r="18" fill="#ffd9b8" stroke="{TINTE}" stroke-width="4"/>'
    out += f'<path d="M110 104L92 164" {s} stroke="{GELB}"/>'
    out += f'<path d="M92 164L124 204L108 246M92 164L148 200L140 246" {s}/>'
    out += f'<path d="M108 116L168 176" {s} stroke="{GELB}" stroke-width="10"/><path d="M104 120L164 180" {s} stroke="{KORALL}" stroke-width="3" opacity=".0"/>'
    out += ball(172, 148) + arrow(172, 134, 172, 96, bend=0)
    for y, t, ty in ((60, "1  Arme gestreckt wie ein Brett", 64), (160, "2  Knie gebeugt, Ball vor dem Körper", 164), (224, "3  Schwung aus den Beinen", 228)):
        out += f'<line x1="190" y1="{y}" x2="214" y2="{y}" stroke="{TINTE}" stroke-width="2"/>' + text(222, ty, t, 14, "start")
    return svg(470, 270, out, "Baggern: Arme gestreckt, Knie gebeugt, Ball trifft die Unterarme")


SVGS = {"kreis": g_kreis, "partner": g_partner, "wand": g_wand, "netz": g_netz, "netz2": lambda: g_netz(2, 1), "rallye": g_rallye,
        "zonen": g_zonen, "angabe": g_angabe, "dreieck": g_dreieck, "turnier": g_turnier,
        "pritsch": g_pritsch, "bagger": g_bagger}

ICON = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="#fff" stroke="{TINTE}" stroke-width="3"/>
<path d="M32 2C24 14 24 26 32 32C40 38 52 38 62 32" fill="none" stroke="{BLAU}" stroke-width="5"/>
<path d="M4 20C16 22 24 28 32 32C40 36 44 48 42 62" fill="none" stroke="{GELB}" stroke-width="5"/>
<path d="M10 50C18 40 28 38 32 32C36 26 44 14 54 12" fill="none" stroke="{KORALL}" stroke-width="5"/></svg>"""


# ---------------------------------------------------------------- Bausteine

def spielplan():
    rows = [("Runde 1", (0, 1), (2, 3)), ("Runde 2", (0, 2), (1, 3)), ("Runde 3", (0, 3), (1, 2))]
    out = '<table class="plan"><tr><th></th><th>Feld A</th><th>Feld B</th></tr>'
    for name, a, b in rows:
        def chip(t):
            n, c = TEAMS[t]
            return f'<span class="dotlbl"><i style="background:{c}"></i>{n}</span>'
        out += f"<tr><td>{name}</td><td>{chip(a[0])} gegen {chip(a[1])}</td><td>{chip(b[0])} gegen {chip(b[1])}</td></tr>"
    return out + "</table>"


def game_card(gid, farbe_cls=None):
    g = GAMES[gid]
    lesson = LESSONS[g["stunde"] - 1]
    pfeil = "".join(f"<li>{esc(s)}</li>" for s in g["schritte"])
    tipp = f'<p class="tl-note">{esc(g["tipp"])}</p>' if g.get("tipp") else ""
    extra = spielplan() if g.get("extra") == "plan" else ""
    return f"""<details class="game {lesson['farbe']}" id="g-{gid}" data-stunde="{g['stunde']}" open>
<summary class="game-head"><span class="badge">Stunde {g['stunde']}</span><h3>{esc(g['name'])}</h3>
<div class="tags"><span class="tag">{esc(g['min'])}</span><span class="tag">{esc(g['wer'])}</span><span class="tag">{esc(g['tag'])}</span></div></summary>
<div class="game-body">
<div class="game-fig">{SVGS[g['svg']]()}</div>
<div class="game-text">
<p class="ziel"><b>Ziel:</b> {esc(g['ziel'])}</p>
<p><b>Aufbau:</b> {esc(g['aufbau'])}</p>
<h4>So geht es</h4><ol class="steps">{pfeil}</ol>
<div class="pts"><b>Punkte fürs Team</b>{esc(g['punkte'])}</div>
<p class="var"><span>Leichter</span> {esc(g['leichter'])}<br><span>Schwerer</span> {esc(g['schwerer'])}</p>
{tipp}
</div></div>{extra}</details>"""


# ---------------------------------------------------------------- Seiten

def page_index():
    stairs = []
    for i, l in enumerate(LESSONS):
        stairs.append(
            f'<a class="step-block {l["farbe"]}" style="--i:{i}" href="stunde-{l["n"]}.html">'
            f'<span class="num">{l["n"]}</span>'
            f'<span><span class="t">{esc(l["short"])}</span><span class="s">{esc(l["highlight"])}</span></span></a>')

    rows = []
    for l in LESSONS:
        rows.append(f"""<a class="lesson-row {l['farbe']} reveal" href="stunde-{l['n']}.html">
<span class="n">{l['n']}</span>
<span><h3>{esc(l['title'])}</h3><p class="goal">{esc(l['goal'])}</p></span>
<span class="meta"><b>Highlight</b>{esc(l['highlight'])}<b style="margin-top:6px">Technik</b>{esc(l['short'])}</span>
<span class="arr" aria-hidden="true">&rarr;</span>
</a>""")

    teams = "".join(f'<span class="team-pill" style="--c:{c}"><i></i>Team {n}</span>' for n, c in TEAMS)

    body = head("Volleyball Liga, Klasse 8", "Vier Termine Volleyball für die 8. Klasse: Liga mit Teams, Stundenverläufe, Spielkarten und Bewertung.") + nav("index")
    body += f"""<main>
<section class="hero"><div class="wrap">
<div>
<h1>Volleyball <em>Liga</em> in vier Terminen</h1>
<p class="lead">Vier Teams, eine Tabelle, ein Spieltag. Vom ersten Pritschen bis zum Finale.</p>
<div class="teams">{teams}</div>
<div class="actions"><a class="btn btn-primary" href="stunde-1.html">Stunde 1 öffnen</a><a class="btn btn-ghost" href="spiele.html">Alle Spiele ansehen</a></div>
</div>
<div class="stairs" aria-label="Der Weg in vier Schritten">{''.join(stairs)}</div>
</div></section>

<section class="block" id="stunden"><div class="wrap">
<h2 class="title reveal">Vier Termine, ein Weg</h2>
<p class="sub reveal">Jede Stunde hat den gleichen Ablauf: einspielen, Technik, Spielform, Liga-Runde. So wissen die Jungs sofort, was kommt.</p>
<div class="lessons">{''.join(rows)}</div>
</div></section>

<section class="block" id="liga"><div class="wrap">
<h2 class="title reveal">So funktioniert die Liga</h2>
<div class="three">
<div class="step-card blau reveal"><span class="big">1</span><h3>Vier Teams</h3><p>16 Schüler, vier Teams zu je vier. Die Teams wählen eigene Namen. Auf dem Feld spielen drei, der vierte pfeift.</p></div>
<div class="step-card gelb reveal"><span class="big">2</span><h3>Punkte sammeln</h3><p>Jedes Spiel bringt Teampunkte. Sie stehen auf der Spielkarte. Du trägst sie in die Ligatabelle ein.</p></div>
<div class="step-card korall reveal"><span class="big">3</span><h3>Spieltag</h3><p>In Stunde 4 spielt jedes Team gegen jedes andere. Dann kommt das Finale und die Siegerehrung.</p></div>
</div>
<div class="page-actions"><a class="btn btn-primary" href="liga.html">Zur Ligatabelle</a></div>
</div></section>

<section class="block" id="bewertung"><div class="wrap">
<h2 class="title reveal">Zwei Noten für Volleyball</h2>
<p class="sub reveal">Die Noten hängen nicht an der Liga. So bleibt es fair, auch wenn ein Team verliert. Der Schlüssel folgt deinem Standard: ab 90, 80, 60, 40 und 20 Prozent gibt es die Noten 1 bis 5.</p>
<div class="score-grid">
<div class="tile blau reveal"><span class="big">20<small>Punkte</small></span><h3>Note Technik</h3><p>Pritschen (10) und Baggern (10). Die Probe läuft in Stunde 3 mit je fünf Zuwürfen.</p></div>
<div class="tile korall reveal"><span class="big">12<small>Punkte</small></span><h3>Note Spiel</h3><p>Vier Kriterien im Turnier, je 0 bis 3 Punkte. Du beobachtest in Stunde 3 und 4.</p></div>
</div>
<div class="page-actions"><a class="btn btn-primary" href="bewertung.html">Notenrechner und Bogen</a></div>
</div></section>

<section class="block" id="material"><div class="wrap">
<h2 class="title reveal">Material und Lehrplan</h2>
<div class="two">
<div class="reveal"><h3>Das brauchst du</h3><ul class="plain">
<li>Volleybälle, am besten einer pro Paar (mindestens 8)</li>
<li>Netz auf 2,10 m, quer geteilt für zwei Felder</li>
<li>Hütchen, Leibchen in vier Farben, Pfeife, Stoppuhr</li>
<li>Klebeband für die Wand, ausgedruckter Bewertungsbogen und Ligatabelle</li>
</ul></div>
<div class="reveal"><h3>Lehrplanbezug (Sport Jgst. 8)</h3><ul class="plain">
<li>4.3 Spielen: oberes und unteres Zuspiel, Angabe von unten</li>
<li>Annahme des aufgeschlagenen Balls, Stellen eines zugespielten Balls</li>
<li>Kleinfeldspiele bis 3:3, Regeln, Fairness, Schiedsrichter</li>
</ul></div>
</div>
</div></section>
</main>
""" + foot()
    return body


def page_lesson(l):
    steps = []
    for zeit, titel, bullets, gid, note in l["steps"]:
        lis = "".join(f"<li>{rich(b)}</li>" for b in bullets)
        note_html = f'<p class="tl-note">{esc(note)}</p>' if note else ""
        link = f'<a class="gamelink" href="#g-{gid}">Spielkarte: {esc(GAMES[gid]["name"])} &darr;</a>' if gid else ""
        steps.append(f"""<div class="tl-step reveal"><div class="tl-time">{esc(zeit)}<span>Minuten</span></div>
<div class="tl-body"><h3>{esc(titel)}</h3><ul>{lis}</ul>{note_html}{link}</div></div>""")

    mat = "".join(f"<li>{esc(m)}</li>" for m in l["material"])
    saf = "".join(f"<li>{esc(s)}</li>" for s in l["safety"])

    gids = []
    for s in l["steps"]:
        if s[3] and s[3] not in gids:
            gids.append(s[3])
    cards = "".join(game_card(g) for g in gids)

    prev_l = LESSONS[l["n"] - 2] if l["n"] > 1 else None
    next_l = LESSONS[l["n"]] if l["n"] < len(LESSONS) else None
    pager = ""
    if prev_l:
        pager += f'<a class="prev" href="stunde-{prev_l["n"]}.html"><small>Zurück</small><strong>Stunde {prev_l["n"]}: {esc(prev_l["short"])}</strong></a>'
    if next_l:
        pager += f'<a class="next" href="stunde-{next_l["n"]}.html"><small>Weiter</small><strong>Stunde {next_l["n"]}: {esc(next_l["short"])}</strong></a>'
    else:
        pager += '<a class="next" href="bewertung.html"><small>Weiter</small><strong>Bewertung und Notenrechner</strong></a>'

    body = head(f"Volleyball Stunde {l['n']}: {l['title']}", l["goal"]) + nav("stunde-%d" % l["n"])
    body += f"""<main class="{l['farbe']}"><div class="wrap">
<div class="page-head">
<div class="crumb"><a href="index.html">Volleyball Liga</a> &nbsp;/&nbsp; Stunde {l['n']} von {len(LESSONS)}</div>
<h1>{esc(l['title'])}</h1>
<p class="goal">{esc(l['goal'])}</p>
<div class="facts"><span class="tag">90 Minuten</span><span class="tag">16 Schüler, 4 Teams</span><span class="tag">Halle: {esc(l['halle'])}</span><span class="tag">Highlight: {esc(l['highlight'])}</span></div>
<div class="page-actions no-print"><button class="btn btn-primary" onclick="window.print()">Als PDF herunterladen</button><a class="btn btn-ghost" href="spiele.html">Alle Spiele</a><a class="btn btn-ghost" href="liga.html">Ligatabelle</a></div>
</div>
<div class="jump no-print"><a href="#ablauf">Ablauf</a><a href="#spiele-stunde">Spiele</a><a href="#material">Material</a></div>
<div class="timeline" id="ablauf">{''.join(steps)}</div>
<div class="aside-grid">
<div class="panel" id="material"><h3>Material</h3><ul class="plain">{mat}</ul></div>
<div class="panel warn"><h3>Sicherheit</h3><ul class="plain">{saf}</ul></div>
</div>
<p class="sub" style="margin-top:20px">{esc(l['lehrplan'])}</p>
<h2 class="title games-title" id="spiele-stunde">Die Spiele dieser Stunde</h2>
<p class="sub">Jede Spielkarte erklärt Ziel, Aufbau und Ablauf in drei Schritten. Zum Vorlesen oder Zeigen.</p>
<div class="games">{cards}</div>
<div class="pager">{pager}</div>
</div></main>
""" + foot()
    return body


def page_spiele():
    chips = ['<button class="chip" data-filter="alle" aria-pressed="true">Alle</button>']
    for l in LESSONS:
        chips.append(f'<button class="chip {l["farbe"]}" data-filter="{l["n"]}" aria-pressed="false">Stunde {l["n"]}: {esc(l["short"])}</button>')
    cards = "".join(game_card(g) for g in GAMES)
    body = head("Volleyball Spiele", "Alle Spielkarten der Volleyball-Liga, einfach erklärt.") + nav("spiele")
    body += f"""<main><div class="wrap">
<div class="page-head">
<div class="crumb"><a href="index.html">Volleyball Liga</a> &nbsp;/&nbsp; Spiele</div>
<h1>Alle Spiele auf einen Blick</h1>
<p class="goal">Zwölf Spiele, jedes mit Ziel, Aufbau und drei Schritten. Filtere nach Stunde.</p>
</div>
<div class="chips" role="group" aria-label="Nach Stunde filtern">{''.join(chips)}</div>
<div class="games" id="game-list">{cards}</div>
</div></main>
""" + foot()
    return body


def page_technik():
    blocks = []
    for t in TECHNIK:
        merk = "".join(f"<li>{esc(m)}</li>" for m in t["merk"])
        fehler = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in t["fehler"])
        kr = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in t["kriterien"])
        blocks.append(f"""<article class="tech {t['farbe']}">
<div class="tech-fig">{SVGS[t['svg']]()}</div>
<div class="tech-text">
<span class="badge">{esc(t['sub'])}</span><h2>{esc(t['name'])}</h2>
<h4>Drei Merkpunkte</h4><ol class="steps">{merk}</ol>
<div class="panel"><h3>Typische Fehler</h3><table><tr><th>Fehler</th><th>Tipp</th></tr>{fehler}</table></div>
<div class="panel"><h3>Technikprobe: {esc(t['name'])}</h3><p>{esc(t['pruefung'])}</p>
<table><tr><th>Merkmal (je 1 Punkt)</th><th>Maßstab</th></tr>{kr}</table></div>
</div></article>""")
    body = head("Volleyball Technik", "Pritschen und Baggern: Merkpunkte, typische Fehler und Kriterien für die Technikprobe.") + nav("technik")
    body += f"""<main><div class="wrap">
<div class="page-head">
<div class="crumb"><a href="index.html">Volleyball Liga</a> &nbsp;/&nbsp; Technik</div>
<h1>Pritschen und Baggern</h1>
<p class="goal">Je drei Merkpunkte zum Vorzeigen, dazu typische Fehler und die Kriterien der Technikprobe.</p>
<div class="page-actions no-print"><button class="btn btn-primary" onclick="window.print()">Als PDF herunterladen</button></div>
</div>
{''.join(blocks)}
</div></main>
""" + foot()
    return body


def page_liga():
    def row(i, name, c):
        cols = "".join(f'<td data-label="{n}"><input class="pt" type="text" inputmode="numeric" autocomplete="off" aria-label="{n} Punkte {name}" data-team="{i}" data-col="{k}"></td>'
                       for k, n in enumerate(["Stunde 1", "Stunde 2", "Stunde 3", "Spieltag"]))
        return (f'<tr data-team="{i}" style="--tc:{c}"><td class="tname"><i style="background:{c}"></i>'
                f'<input class="nm" type="text" value="Team {name}" maxlength="24" aria-label="Teamname {name}" data-name="{i}"></td>{cols}'
                f'<td class="sum" data-label="Summe" data-sum="{i}">0</td><td class="rank" data-label="Rang" data-rank="{i}">-</td></tr>')
    rows = "".join(row(i, n, c) for i, (n, c) in enumerate(TEAMS))
    body = head("Volleyball Ligatabelle", "Teampunkte eintragen, Summe und Rang werden automatisch berechnet.") + nav("liga")
    body += f"""<main><div class="wrap">
<div class="page-head">
<div class="crumb"><a href="index.html">Volleyball Liga</a> &nbsp;/&nbsp; Liga</div>
<h1>Die Ligatabelle</h1>
<p class="goal">Teamnamen und Punkte eintragen. Summe und Rang rechnet die Seite selbst. Alles bleibt auf diesem Gerät gespeichert.</p>
</div>
<div class="sheet-wrap"><table class="liga" aria-label="Ligatabelle">
<tr><th>Team</th><th>Stunde 1</th><th>Stunde 2</th><th>Stunde 3</th><th>Spieltag</th><th>Summe</th><th>Rang</th></tr>{rows}</table></div>
<div class="page-actions no-print"><button class="btn btn-primary" onclick="window.print()">Als PDF herunterladen</button><button class="btn btn-ghost" id="liga-reset" type="button">Tabelle leeren</button></div>

<h2 class="title" style="margin-top:56px">So kommen die Punkte zusammen</h2>
<div class="scales">
<div class="panel"><h3>Spiele</h3><table><tr><th>Ergebnis</th><th>Punkte</th></tr><tr><td>Sieg (Stunde 1 bis 3)</td><td>2</td></tr><tr><td>Unentschieden</td><td>1</td></tr><tr><td>Sieg am Spieltag</td><td>3</td></tr></table></div>
<div class="panel"><h3>Übungen</h3><p>Rekord im Ballkreis, gelungene Paare und Treffer in den Zielzonen bringen 1 bis 3 Punkte. Die genaue Regel steht auf jeder Spielkarte.</p></div>
</div>
</div></main>
""" + foot()
    return body


def page_timer():
    presets = "".join(f'<button class="chip" type="button" data-min="{m}">{m} Min</button>' for m in (3, 5, 6, 8, 10, 12, 15))
    body = head("Volleyball Timer", "Stoppuhr für Spielzeiten, mit Signalton und Bildschirm-an.") + nav("timer")
    body += f"""<main><div class="wrap">
<div class="page-head">
<div class="crumb"><a href="index.html">Volleyball Liga</a> &nbsp;/&nbsp; Timer</div>
<h1>Timer</h1>
<p class="goal">Zeit wählen, Start drücken. Am Ende kommt ein Signalton und das Handy vibriert. Der Bildschirm bleibt an.</p>
</div>
<div class="timer" id="timer">
<div class="chips" role="group" aria-label="Zeit wählen">{presets}</div>
<div class="clock" id="clock" role="timer" aria-live="off">06:00</div>
<div class="timer-btns"><button class="btn btn-primary" id="t-start" type="button">Start</button><button class="btn btn-ghost" id="t-reset" type="button">Zurück</button></div>
<p class="sub" id="t-info">Tipp: Zum Spielen eine Runde 6 bis 10 Minuten, dann Wechsel.</p>
</div>
</div></main>
""" + foot()
    return body


def page_bewertung():
    sk = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in SPIEL_KRITERIEN)
    kr_p = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in TECHNIK[0]["kriterien"])
    kr_b = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in TECHNIK[1]["kriterien"])

    ff = ""
    for k, n, m in (("pritschen", "Pritschen", 10), ("baggern", "Baggern", 10), ("spiel", "Spiel", 12)):
        ff += (f'<div class="field"><label for="f-{k}">Punkte {n}</label>'
               f'<input id="f-{k}" name="{k}" type="text" inputmode="decimal" autocomplete="off">'
               f'<span class="hint">0 bis {m} Punkte</span><span class="err" id="e-{k}" role="alert"></span></div>')

    res = ('<div class="res-col"><div class="lbl">Note Technik</div><div class="note" id="r-technik" aria-live="polite">-</div><div class="lbl" id="p-technik"></div></div>'
           '<div class="res-col"><div class="lbl">Note Spiel</div><div class="note" id="r-spiel" aria-live="polite">-</div><div class="lbl" id="p-spiel"></div></div>')

    st, ss = schluessel(TECHNIK_MAX), schluessel(12)
    sch_rows = "".join(f"<tr><td>Note {i + 1}</td><td>ab {st[i]}</td><td>ab {ss[i]}</td></tr>" for i in range(5))
    sch_rows += "<tr><td>Note 6</td><td>darunter</td><td>darunter</td></tr>"

    rows = "".join(f'<tr><td class="n">{i}</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 17))

    body = head("Volleyball Bewertung", "Notenrechner, Punkte-Richtwerte und Bewertungsbogen für die Volleyball-Liga.") + nav("bewertung")
    body += f"""<main><div class="wrap">
<div class="page-head">
<div class="crumb"><a href="index.html">Volleyball Liga</a> &nbsp;/&nbsp; Bewertung</div>
<h1>Zwei Noten für Volleyball</h1>
<p class="goal">Technik (Pritschen und Baggern, zusammen 20 Punkte) und Spiel (12 Punkte). Jede Note wird einzeln berechnet.</p>
</div>

<div class="calc no-print">
<form id="rechner" novalidate aria-label="Notenrechner">{ff}</form>
<div class="result">{res}</div>
</div>

<div class="scales">
<div class="panel"><h3>Technik Pritschen, 10 Punkte</h3><p>5 Zuwürfe aus 4 Metern, jeder Treffer in der Zone gibt 1 Punkt. Dazu 5 Technikpunkte:</p><table><tr><th>Merkmal</th><th>Maßstab</th></tr>{kr_p}</table></div>
<div class="panel"><h3>Technik Baggern, 10 Punkte</h3><p>5 Zuwürfe aus 4 Metern, jeder Treffer in der Zone gibt 1 Punkt. Dazu 5 Technikpunkte:</p><table><tr><th>Merkmal</th><th>Maßstab</th></tr>{kr_b}</table></div>
<div class="panel"><h3>Spiel, 12 Punkte</h3><p>Vier Kriterien, je 0 bis 3 Punkte, beobachtet im 3-gegen-3.</p><table><tr><th>Kriterium</th><th>Maßstab</th></tr>{sk}</table></div>
<div class="panel"><h3>Notenschlüssel (90, 80, 60, 40, 20 Prozent)</h3>
<table><tr><th>Note</th><th>Technik /20</th><th>Spiel /12</th></tr>{sch_rows}</table></div>
</div>
<p class="sub">Die Richtwerte sind ein Vorschlag, keine amtliche Tabelle. Nach dem ersten Durchlauf mit der Klasse justieren, falls fast alle am selben Ende landen.</p>

<div class="bogen-section">
<h2 class="title" style="margin-top:56px">Bewertungsbogen zum Ausdrucken</h2>
<div class="page-actions no-print"><button class="btn btn-primary" onclick="window.print()">Als PDF herunterladen</button></div>
<div class="sheet-wrap"><table class="bogen" aria-label="Bewertungsbogen">
<tr><th>#</th><th>Name</th><th>Team</th><th>Pritschen /10</th><th>Baggern /10</th><th>Note Technik</th><th>Spiel /12</th><th>Note Spiel</th></tr>{rows}</table></div>
</div>
</div></main>
""" + foot()
    return body


def main():
    files = {"index.html": page_index(), "spiele.html": page_spiele(), "technik.html": page_technik(),
             "liga.html": page_liga(), "timer.html": page_timer(), "bewertung.html": page_bewertung()}
    for l in LESSONS:
        files["stunde-%d.html" % l["n"]] = page_lesson(l)
    for name, content in files.items():
        bad = [c for c in ("—", "–") if c in content]
        assert not bad, f"Gedankenstrich in {name}"
        (ROOT / name).write_text(content, encoding="utf-8")
    (ROOT / "icon.svg").write_text(ICON, encoding="utf-8")
    print("Gebaut:", ", ".join(files))


if __name__ == "__main__":
    main()

# Volleyball Liga Klasse 8 (Sequenz-Homepage)

Stand: 09.10.2026, lokal gebaut und geprüft, noch nicht veröffentlicht, noch nicht im Unterricht getestet.

Vier Termine (je 90 Min, 16 Schüler, 4 Teams zu je 4) vom Pritschen bis zum Turnier mit Finale. Eine Liga über alle Termine, dazu zwei Noten (Technik 20 P aus Pritschen und Baggern, Spiel 12 P). Lehrplanbezug: LehrplanPLUS Mittelschule Sport Jgst. 8, 4.3 Spielen (oberes und unteres Zuspiel, Angabe von unten, Kleinfeldspiele bis 3:3).

Gedacht für die Nutzung auf dem Handy in der Halle: Spielkarten klappen auf dem Handy zu, Timer mit Signalton, Ligatabelle als Karten.

## Dateien

| Datei | Zweck |
|---|---|
| `index.html` | Startseite: Weg, Stunden, Liga-Erklärung, Noten, Material |
| `stunde-1.html` bis `stunde-4.html` | Zeitleiste, Material, Sicherheit und die Spielkarten der Stunde |
| `spiele.html` | Alle 12 Spielkarten, filterbar nach Stunde |
| `technik.html` | Pritschen und Baggern: Merkpunkte, Fehler, Kriterien der Technikprobe |
| `liga.html` | Ligatabelle, speichert im Browser (localStorage), Summe und Rang automatisch |
| `timer.html` | Countdown mit Signalton, Vibration, Bildschirm bleibt an |
| `bewertung.html` | Notenrechner, Punkte-Richtwerte, Bewertungsbogen für 16 Schüler |
| `style.css`, `app.js`, `fonts/`, `icon.svg` | Gestaltung, Verhalten, Schrift Geist (lokal), Icon |
| `quellen/build.py` | Baut alle Seiten neu. Inhalte, Spiele und Grafiken (SVG) stehen im Skript |

Änderungen: in `quellen/build.py` ändern, dann `python3 quellen/build.py`.

## Design

Vorlage: 21st.dev "Forma Pilates Studio" (wie Basketball), hier mit vier Teamfarben (Blau, Gelb, Grün, Korall) auf warmem Creme. Jede Stunde hat eine feste Farbe. Alle Grafiken sind selbst gezeichnete Vektorgrafiken, keine Bildgenerierung (kostenlos).

## Druck

PDF über den Button auf der Seite. Seitenzahlen: Stunde 1 = 6, Stunde 2 = 6, Stunde 3 = 5, Stunde 4 = 3, Technik = 5, Bewertung = 3, Liga = 1.

## Offene Punkte

- Veröffentlichen: eigenes Repo `Fhe86/volleyball` und GitHub Pages anlegen (wartet auf Fabis Ja).
- Annahmen prüfen: Doppelstunden (90 Min), Netz auf 2,10 m quer teilbar für zwei Felder, 16 Schüler.
- Punkte-Richtwerte (Ballkreis-Rekorde, Ketten pro 3 Minuten, Angabe-Zonen) nach dem ersten Durchlauf anpassen.
- Spielnote: Beobachtungsplan steht in Stunde 4 (Runde 1 Feld A, Runde 2 und 3 Feld B).

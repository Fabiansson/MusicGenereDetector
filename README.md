
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Fabiansson/MusicGenreDetector">
    <img src="https://i.postimg.cc/L6YDTjSQ/logo.png" width="800" />
  </a>
</p>

# Projektbeschreibung
Das vorliegende Projekt hat es sich zur Aufgabe gemacht, einen Musik-Classifier zu erstellen. Dieses Neuronale Netzwerk wurde im Rahmen des Moduls "Deep Learning" erstellt. Es sollte in der Lage sein, ein Musikstück, einem Genre zu zuweisen. Für das Testing wurde das FMA Dataset verwendet (https://github.com/mdeff/fma). Das Set umfasst 8000 Songs in MP3-Format aus 8 ausbalancierten Parent-Genres von jeweils einer Länge von 30 Sekunden.
Die Aufgaben bestanden hauptsächlich im Extrahieren der Features, dem Aufbereiten der Daten und der Erstellung des neuralen Netzwerks.

Link zum Trello-Board mit den Aufgaben:

https://trello.com/invite/b/IzMeQyMZ/efc49880889c33077999f696bb65d48f/musifier

# Technische Beschreibung
Das Projekt wurde mit Python geschrieben und lässt sich grundsätzlich in vier Teile unterteilen.
## data_processor.py
Im File data_processor.py findet hauptsächlich die Feature-Extraktion bei den mp3-Dateien aus dem Datensatz statt. Dazu wird ein trackgenremapping.xlsx eingelsen wobei dieses jedem Song ein bestimmtes Label zuweist. Danach wird mittels Librosa die Featureextraktion gemacht und so ein CSV erstellt (features_with_var_parentlabels.csv). Dabei erhalten wir eine Liste aller Songs und deren Features. Ausserdem werden die Anzahl Labels auf die 8 Parent-Genres reduziert.
## trainer.py
Im File trainer.py können die ausgelsenene Songs inkl. Features wieder eingelesen werden und das eigentliche Erstellen und Trainieren des Netzes beginnt hier. Es wird ein LabelEncoder verwendet, der die Lables aus der letzten Spalte einliest und darauf folgend, werden alle Feature-Values normiert mit Hilfe eines StandartScalers. Danach wird das Datenset aufgeteilt in Trainings- und Testdaten in einem Verhältnis von 70% zu 30%.

Für das Netz verwenden wir ein sequentielles Neurales Netz, welches wie folgt aufgebaut ist: 512-256-128-64-8. Als Aktivierungsfunktion wird jeweils "RELU" verwendet und zum Schluss ein Soft-Max Layer, um die Klassifikation auf 8 Genres vorzunehmen. Dazwischen verwenden wir jeweils Dropout-Layers, wobei pro Durchlauf immer 20% der Gewichte nicht verändert werden, um Overfitting an die Trainingsdaten zu verhindern.
Zum Schluss wird das Netz mit 100 Epochen trainiert und das Model abgespeichert.

## predicter.py
Im File predicter.py wird das trainierte Netzt verwendet, um andere Songs nach dem Genre zu klassifizieren. Dabei gehen wir ähnlich vor wie im data_processor, wobei wir einen bestimmten Song einlesen und wieder mit Librosa eine Feature-Extraktion machen. Wichtig hierbei ist, da wir das Netz mit Songs von der Länge von 30 Sekunden trainiert haben, dass unser Input-Song auch diese Länge aufweist. Dies ist natürlich nicht immer gegeben. Um diesem Problem aus dem Weg zu gehen, spliten wir den Song in mehrere Teile, welche jeweils 30 Sekunden lang sind und lesen die Features aus diesen Teilen aus. Die Trainingsdaten werden erneut eingelesen und die zu klassifizierenden Song-Teile am Schluss angehängt. Dies ist nötig um die Feature-Values in Zusammmenhang zu den Trainings-Values zu bringen und eine Normalisation zu machen. Im Anschluss wird das trainierte Model geladen und eine Prediction für alle Parts ausgeführt. Dabei erhalten wir für jeden Part ein Genre. Die Genres werden aufsummiert und die höchste Summe entspricht dem Genre des ganzen Songs.
## cli.py
Das CLI dient zur einfachen Bedienung des Programms. Man kann ein Filepath oder eine YouTube-URL eingeben. Im Anschluss wird der Song gegebenenfalls von YouTube heruntergelesen und klassifiziert.

<p float="left">
  <img src="https://i.postimg.cc/q7nWZ9dY/1.png" width="800" />
</p>

# Benutzung
Um den MusicGenreDetector zu nutzen, müssen alle Dependencies installiert werden:

`pip install -r requirements.txt`

Das Modell muss nicht mehr traniert werden, da es bereits im Repository vorhanden ist.
Danach kann das CLI ganz einfach mit beispielsweise einem YouTube-Link ausgeführt werden:

`python cli.py https://www.youtube.com/watch?v=pRpeEdMmmQ0`

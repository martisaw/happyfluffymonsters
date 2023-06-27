import os
import openai
from dotenv import load_dotenv

# Load all variables from .env file
load_dotenv('./hfm.env')

# openai.organization = "personal"
openai.api_key = os.getenv('API_KEY')

# Idee: ChatGPT generiert uns ein Szenario
# verb something + location
# verbliste, ortliste, gegenstandsliste

verben = ["lachen", "lächeln", "jubeln", "strahlen", "blühen", "wachsen", "lieben", "umarmen", "unterstützen", "loben", "bewundern", "danken", "helfen", "teilen", "genießen", "inspirieren", "motivieren", "ermutigen", "erfreuen", "sich freuen", "sich begeistern", "feiern", "tanzen", "singen", "schaffen", "entdecken", "erkunden", "staunen", "bewundern", "schätzen", "belohnen", "träumen", "hoffen", "optimistisch sein", "erneuern", "vertrauen", "aufbauen", "erholen", "entspannen", "strahlen", "glänzen", "begeistern", "beflügeln", "aufblühen", "strahlen", "aufleben", "mitfühlen", "anerkennen", "zufrieden sein", "umsetzen", "erfüllen", "erreichen", "inspirieren", "motivieren", "anspornen", "begeistern", "ermutigen", "bewegen", "bezaubern", "faszinieren", "beeindrucken", "überwinden", "sich entwickeln", "weiterkommen", "wachsen", "aufsteigen", "Fortschritte machen", "erfolgreich sein", "gewinnen", "stärken", "unterstützen", "fördern", "bereichern", "erweitern", "erleben", "bereichern", "positiv denken", "lächeln", "optimistisch sein", "positiv kommunizieren", "strahlend sein", "freudig sein", "optimistisch sein", "sich verbessern", "glücklich sein", "das Leben genießen"]
orte = ["Strand", "Berggipfel", "Wald", "Wasserfall", "Nationalpark", "See", "Insel", "Wiese", "Blumenfeld", "Botanischer Garten", "Wüste", "Klippe", "Flussufer", "Schlucht", "Höhle", "Küste", "Schloss", "Ruinen", "Kirche", "Tempel", "Museum", "Theater", "Konzertsaal", "Bibliothek", "Opernhaus", "Stadion", "Marktplatz", "Schwimmbad", "Zoo", "Aquarium", "Freizeitpark", "Einkaufszentrum", "Kaffeehaus", "Restaurant", "Café", "Weinberg", "Bauernhof", "Weingut", "Brauerei", "Botanischer Garten", "Picknickplatz", "Yachthafen", "Segelhafen", "Skigebiet", "Campingplatz", "Thermen", "Kurort", "Wellness-Spa", "Strandpromenade", "Fahrradweg", "Wanderweg", "Pilgerstätte", "Schrein", "Rastplatz", "Aussichtspunkt", "Observatorium", "Leuchtturm", "Hochseilgarten", "Meditationszentrum", "Klettergarten", "Schwimmbad", "Freibad", "Wasserpark", "Strandclub", "Tanzstudio", "Sportplatz", "Skatepark", "Minigolfplatz", "Golfplatz", "Tennisplatz", "Basketballplatz", "Park", "Botanischer Garten", "Vogelschutzgebiet", "Naturreservat", "Wildtierbeobachtungsstelle", "Hafen", "Fischereihafen", "Flughafen", "Bahnhof", "Busbahnhof", "Autobahnraststätte", "Tankstelle", "Supermarkt", "Boutique", "Kunstgalerie", "Kino", "Bücherei", "Schule", "Universität"]
gegenstand = ["Laptop", "Buch", "Stift", "Telefon", "Kamera", "Brille", "Schlüssel", "Uhr", "Tasche", "Schuhe", "Kleidung", "Geldbörse", "Sonnenbrille", "Regenschirm", "Rucksack", "Kaffeetasse", "Teller", "Besteck", "Schere", "Bürste", "Fernbedienung", "Handtuch", "Kissen", "Decke", "Blumentopf", "Vase", "Kerze", "Taschenlampe", "Notizbuch", "Klebeband", "Schraubenzieher", "Hammer", "Schrauben", "Nähmaschine", "Bügeleisen", "Kochtopf", "Pfanne", "Backform", "Kaffeemaschine", "Toaster", "Mixer", "Staubsauger", "Fön", "Badezimmerwaage", "Gartenwerkzeuge", "Mülltonne", "Fahrrad", "Auto", "Motorrad", "Helm", "Tisch", "Stuhl", "Sofa", "Bett", "Kommode", "Spiegel", "Kleiderschrank", "Fernseher", "Radio", "Lautsprecher", "Kühlschrank", "Mikrowelle", "Waschmaschine", "Trockner", "Ventilator", "Klimaanlage", "Heizung", "Bücherregal", "Schreibtisch", "Drucker", "Scanner", "Projektor", "Bastelschere", "Farbstifte", "Leinwand", "Easel", "Gitarre", "Klavier", "Keyboard", "Mikrofon", "Trommel", "Ballettschuhe", "Fußball", "Basketball", "Schachbrett", "Puzzle", "Kartenspiel", "Kuscheltier", "Puppenhaus", "Bauklötze", "Lego", "Puzzle", "Modellflugzeug"]

# Anzahl Monster
# Kombiniere aus jedem 1 (mit und ohne ort) -> Chat GPT soll einen Satz erstellen
# Happy fluffy monster

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are an image creator with endless creativity."},
    # {"role": "user", "content": "Hello! What is a happy fluffy monster doing today? Answer in one sentence!"}
    {"role": "user", "content": "Hello! What is a happy fluffy monster doing today? Answer in one short sentence! Start with 'A happy fluffy monster'"}
  ],
  temperature=1.2
)

input_dalle = completion.choices[0].message.content.replace(".", ", digital art.")

print(input_dalle)

res = openai.Image.create(
  prompt=input_dalle,
  n=2,
  size="256x256"
)

print(res)
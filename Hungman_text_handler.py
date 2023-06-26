import pickle
STRINGS_FILE = "strings.db"

polish_key_words = [
    ["Zwierzęta hodowlane", "pies", "kot", "owca", "byk", "kura", "świnia", "baran", "gęś", "królik", "indyk", "kaczka"],
    ["Warzywa", "marchew", "ogórek", "dynia", "groch", "cebula", "ziemniak", "sałata", "kapusta", "kalafior", "brokuł", "papryka", "pomidor"],
    ["Miasto w Polsce", "warszawa", "poznań", "gdańsk", "łódź", "opole", "katowice", "szczecin", "białystok", "kraków", "wrocław", "szczecin"],
    ["Kolory", "czerwony", "zielony", "niebieski", "żółty", "fioletowy", "różowy", "pomarańczowy", "czarny", "biały", "brązowy", "szary", "beżowy"],
    ["Owoce", "jabłko", "banan", "truskawka", "gruszka", "wiśnia", "malina", "arbuz", "ananas", "śliwka", "mango", "winogrono", "brzoskwinia"],
    ["Kraje", "polska", "niemcy", "francja", "włochy", "hiszpania", "japonia", "rosja", "brazylia", "chiny", "indie", "anglia", "usa"],
    ["Przedmioty szkolne", "matematyka", "fizyka", "chemia", "historia", "biologia", "język polski", "geografia", "informatyka", "muzyka", "plastyka", "w-f", "religia"],
    ["Zawody", "lekarz", "nauczyciel", "prawnik", "programista", "inżynier", "architekt", "dziennikarz", "kucharz", "fryzjer", "piekarz", "kelner", "listonosz"],
    ["Sporty", "koszykówka", "siatkówka", "tenis", "pływanie", "boks", "łyżwiarstwo", "kolarstwo", "golf", "narciarstwo", "judo", "wspinaczka"],
    ["Instrumenty muzyczne", "gitara", "pianino", "skrzypce", "perkusja", "trąbka", "saksofon", "flet", "harmonijka", "wiolonczela", "akordeon", "klarnet", "keyboard"],
    ["Kwiaty", "róża", "tulipan", "narcyz", "storczyk", "słonecznik", "konwalia", "fiołek", "lilia", "irys", "magnolia", "stokrotka", "orchidea"],
    ["Części ciała", "głowa", "ręka", "noga", "usta", "oko", "nos", "usta", "szyja", "kolano", "ramię", "brzuch", "plecy"],
    ["Samochody", "audi", "bmw", "ford", "toyota", "honda", "volkswagen", "mercedes", "opel", "fiat", "renault", "peugeot", "nissan"],
    ["Państwa", "usa", "kanada", "meksyk", "brazylia", "japonia", "rosja", "chiny", "indie", "niemcy", "francja", "włochy", "hiszpania"],
    ["Przedmioty gospodarstwa domowego", "lodówka", "kuchenka", "pralka", "telewizor", "mikrofalówka", "zmywarka", "suszarka", "mikserek", "odkurzacz", "żelazko", "czajnik"],
    ["Języki obce", "angielski", "francuski", "hiszpański", "niemiecki", "włoski", "rosyjski", "japoński", "chiński", "portugalski", "arabski", "holenderski", "szwedzki"],
    ["Przedmioty codziennego użytku", "telefon", "klucze", "portfel", "okulary", "długopis", "notes", "pudełko", "zegarek", "torebka", "aparat"],
    ["Góry", "tatry", "alpy", "himalaje", "karakorum", "andy", "rockies", "ural", "pireneje", "ande", "australia"],
    ["Przybory kuchenne", "nóż", "patelnia", "garnek", "talerz", "widelec", "łyżka", "sito", "nożyczki", "deska", "wałek", "termometr"],
    ["Przedmioty podróżne", "walizka", "plecak", "paszport", "bagaż", "bilet", "torba", "kompas", "mapa", "wiza", "przewodnik"],
    ["Zwierzęta dzikie", "lew", "tygrys", "niedźwiedź", "słoń", "girafa", "hipopotam", "żyrafa", "krokodyl", "tygrys", "lampart", "pantera"],
    ["Części samochodowe", "silnik", "kierownica", "hamulce", "opona", "szyba", "szyberdach", "akumulator", "filtr", "amortyzator", "rozrusznik"],
    ["Słynne zabytki", "koloseum", "piramidy", "wielka murawa", "tadź mahal", "pałac kultury", "machu picchu", "pałac wersalski", "akropol", "petra", "wieża eiffla"],
    ["Przedmioty w kuchni", "garnek", "patelnia", "nóż", "talerz", "łyżka", "widelec", "kubek", "szklanka", "miska", "deska", "czajnik"],
    ["Sporty zespołowe", "piłka nożna", "koszykówka", "siatkówka", "hokej", "rugby", "piłka ręczna", "baseball", "hurling", "krykiet", "netball"],
    ["Literatura klasyczna", "pan tadeusz", "w pustyni i w puszczy", "zbrodnia i kara", "lalka", "przedwiośnie", "quo vadis", "odyssey", "duma i uprzedzenie", "mały książę", "hamlet"],
    ["Przybory do malowania", "pędzel", "farba", "paleta", "papier", "farbki", "gwasze", "penseta", "easel", "pasty", "akwarele"],
    ["Słynne wynalazki", "telefon", "samolot", "telewizja", "komputer", "samochód", "lampka", "odkurzacz", "maszyna do pisania", "drukarka", "aparat fotograficzny"],
    ["Gatunki filmowe", "komedia", "dramat", "thriller", "science-fiction", "horror", "akcja", "romantyczny", "animowany", "przygodowy", "fantasy"],
    ["Przybory do ogrodu", "grabie", "szpadel", "sekator", "wózek", "kosiarka", "nożyczki", "sadzonka", "worki", "kaczka", "rękawice"],
    ["Zawody sportowe", "lekkoatleta", "piłkarz", "pływak", "kolarz", "biegacz", "skoczek", "tenisista", "siatkarz", "gimnastyk", "zapaśnik"],
    ["Przedmioty piśmiennicze", "długopis", "ołówek", "zeszyt", "notes", "gumka", "temperówka", "linijka", "flamastry", "marker", "klej"],
    ["Czasowniki", "biec", "skakać", "pisać", "czytać", "śpiewać", "tańczyć", "mówić", "gotować", "myć", "budować"],
    ["Przedmioty domowe", "kanapa", "stół", "krzesło", "szafa", "łóżko", "komoda", "lustro", "toaleta", "zlew", "kominek"],
    ["Państwa afrykańskie", "egipt", "kenia", "maroko", "nigeria", "południowa afryka", "tunezja", "algieria", "etiopia", "sudan", "senegal"],
    ["Słynne postacie literackie", "sherlock holmes", "harry potter", "hamlet", "don kichot", "robinson crusoe", "frankenstein", "oliver twist", "alice in wonderland", "huckleberry finn", "pippi longstocking"]
]


english_key_words = [
    ["Farm Animals", "dog", "cat", "cow", "sheep", "bull", "hen", "pig", "ram", "goose", "rabbit"],
    ["Vegetables", "carrot", "cucumber", "pumpkin", "pea", "onion", "potato", "lettuce", "cabbage", "cauliflower", "broccoli"],
    ["City", "Warsaw", "Berlin", "Paris", "Beijing", "Moscov", "New York", "Rome", "Cairo", "Mexico City"],
    ["Colors", "red", "green", "blue", "yellow", "purple", "pink", "orange", "black", "white", "brown"],
    ["Fruits", "apple", "banana", "strawberry", "pear", "cherry", "raspberry", "watermelon", "pineapple", "plum", "mango"],
    ["Countries", "Poland", "Germany", "France", "Italy", "Spain", "Japan", "Russia", "Brazil", "China", "India"],
    ["Professions", "doctor", "teacher", "lawyer", "programmer", "engineer", "architect", "journalist", "chef", "hairdresser", "baker"],
    ["Sports", "basketball", "volleyball", "tennis", "swimming", "boxing", "figure skating", "cycling", "golf", "skiing"],
    ["Musical Instruments", "guitar", "piano", "violin", "drums", "trumpet", "saxophone", "flute", "harmonica", "cello", "accordion"],
    ["Flowers", "rose", "tulip", "daffodil", "orchid", "sunflower", "lily of the valley", "violet", "lily", "iris", "magnolia"],
    ["Body Parts", "head", "hand", "leg", "mouth", "eye", "nose", "mouth", "neck", "knee", "arm"],
    ["Cars", "Audi", "BMW", "Ford", "Toyota", "Honda", "Volkswagen", "Mercedes", "Opel", "Fiat", "Renault", "Peugeot", "Nissan"],
    ["Countries", "USA", "Canada", "Mexico", "Brazil", "Japan", "Russia", "China", "India", "Germany", "France", "Italy", "Spain"],
    ["Household Items", "refrigerator", "stove", "washing machine", "television", "microwave", "dishwasher", "dryer", "mixer", "vacuum cleaner", "iron", "kettle"],
    ["Foreign Languages", "English", "French", "Spanish", "German", "Italian", "Russian", "Japanese", "Chinese", "Portuguese", "Arabic", "Dutch", "Swedish"],
    ["Everyday Items", "phone", "keys", "wallet", "glasses", "pen", "notebook", "box", "watch", "bag", "camera"],
    ["Mountains", "Tatra", "Alps", "Himalayas", "Andes", "Rockies", "Kilimanjaro", "Everest", "Fuji", "Matterhorn"],
    ["Seas", "Atlantic Ocean", "Pacific Ocean", "Indian Ocean", "Arctic Ocean", "Mediterranean Sea", "Caribbean Sea", "Red Sea", "Baltic Sea"],
    ["Planets", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
]



polish_strings = [
    "Gra polega na zgadywaniu haseł po przez pojedyńcze litery",
    "Gra automatycznie wstawia polskie znaki.",
    "POWRÓT",
    "ZAPISZ",
    "GRATULACJE, TWÓJ WYNIK TO:",
    "PODAJ SWOJĘ IMIĘ, ABY ZAPISAĆ WYNIK",
    "SUKCES",
    "PORAŻKA",
    "NOWA GRA",
    "OPCJE",
    "NAJLESPZE WYNIKI",
    "WYJŚCIE",
    "RESET",
    "PEŁNY EKRAN",
    "OKNO",
    "MUZYKA",
    "DŹWIĘK",
    "POLSKI",
    "ANGIELSKI", 
    "ROZDZIELCZOŚĆ", 
    "JĘZYK",
    "WYŁ.",
    "KATEGORIA:",
    "PUNKTY:",
    "KONIEC GRY"]

english_strings = [
    "The game involves guessing passwords letter by letter.",
    "",
    "BACK",
    "SAVE",
    "CONGRATULATIONS, YOUR SCORE IS:",
    "ENTER YOUR NAME TO SAVE THE SCORE",
    "SUCCESS",
    "FAILURE",
    "NEW GAME",
    "OPTIONS",
    "TOP SCORES",
    "EXIT",
    "RESET",
    "FULL SCREEN",
    "WINDOW",
    "MUSIC",
    "SOUND",
    "POLISH",
    "ENGLISH",
    "RESOLUTION",
    "LANGUAGE",
    "OFF",
    "CATEGORY:",
    "SCORE:",
    "GAME OVER"]

polish_localisation = [polish_strings, polish_key_words]
english_localisation = [english_strings, english_key_words]

content = [polish_localisation, english_localisation]

with open (STRINGS_FILE,"wb") as stream:
    pickle.dump(content, stream)
# DistSys - Prvi mini projekt

### Prvi mikroservis
Fake E-ucenje API microservis (M0). Sastoji se od DB i jedne rute koja vraca github linkove na zadace. Prilikom pokretanja servisa, provjerava se postoje li podaci u DB. Ukoliko ne postoje, pokrece se funkcija koja popunjava DB s testnim podacima (10000). Kad microservis zaprimi zahtjev za dohvacanje linkova, uzima maksimalno 100 redataka podataka iz DB-a.

### Drugi mikroservis
Microservis asinkrono poziva e-ucenje API (M1), te prosljeđuje podatke kao dictionary Worker tokenizer (WT) microservisu.

### Treći mikroservis
WT microservis uzima dictionary. Uzima samo redove gdje username pocinje na w. Prosljeđuje kod 4. microservisu.

### Četvrti mikroservis
WT microservis uzima dictionary. Uzima samo redove gdje username pocinje na d. Prosljeđuje kod 4. microservisu.

### Peti mikroservis
Microservis sastoji od rute (/gatherData) sprema se Python kod u listu. Ako ima više od 10 elemenata unutar liste asinkrono se kreiraju svi file-ovi iz liste.

# Distributed Systems - First mini project

### First microservice
"Fake E-ucenje API" microservice (M0). It includes a DB and a route that returns my GitHub homework repo link. When run it checks if there is any data in the DB. If the DB is empty, a method is used that fills the DB with test data (the first 10_000 lines). When the microservice receives the data gathering request, it takes a maximum of 100 lines od data from the DB.

### Second microservice
This microservice asynchronously calls the "Fake E-ucenje API" microservice and it sends the data as a dictionary to the Worker tokenizer (WT) microservice

### Third microservice
The worker tokenizer microservice receives the dictionary. It takes only the lines where the "username" starts with "w". It sends its code to the fourth microservice.

### Fourth microservice
The worker tokenizer microservice receives the dictionary. It takes only the lines where the "username" starts with "d". It sends its code to the fourth microservice.


### Fifth microservice
This microservice inludes a /gatherData route which saves the Python code to a list. If the lists has more than 10 elements, all the files in the list are asynchronously created.

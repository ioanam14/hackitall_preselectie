# HackITall Preselectie

## Desrierea problemei

Consideram un tren care circula intre Brasov si Bucuresti si opreste in 6 statii. Din fiecare statie se pot urca intre 30 si 60 de persoane.
Acestia calatoresc in grupuri care pot avea intre 1 si 5 persoane. Trenul are in componenta lui 5 vagoane, fiecare vagon are 10 compartimente a cate 8 locuri.
Programul aloca bilete intr-un mod cat mai optim astfel incat calatorii sa fie distribuiti uniform in compartimente, iar grupurile
sa fie repartizate pe cat posibil in acelasi compartiment. Se asigura astfel ca compartimentele vor fi ocupate in aproximativ aceeasi
masura, iar calatorii nu vor fi inghesuiti in anumite compartimente, iar altele vor fi libere.

Input: 
* un numar intre 1 si 5 reprezentand numarul de persoane din grup
* statia de plecare
* statia de sosire

Output:
* numarul vagonului si numarul locului pentru fiecare bilet din grup

## Descrierea situatiilor care pot sa apara

Analizand datele problemei putem observa ca daca sunt 6 statii si se urca intre 30 si 60 de persoane in fiecare statie, atunci vom avea
maxim 6 * 60 = 360 de calatori pe tot parcursul calatoriei. Pe de alta parte, in tren sunt 400 de locuri si nu toti calatorii vor merge toate
cele 6 statii. In concluzie, vor fi locuri suficiente pentru toti calaltorii.

Situatii speciale si exceptiii tratate:

* Nu mai exista suficiente locuri disponibile pentru un grup de mai mult de o persoana astfel incat locurile repartizate sa se afle in acelasi
compartiment. In acest caz vom incerca sa impartim grupul in subgrupuri. Ca prima optiune incercam sa impartim grupul in doua jumatati
cat se poate de egale astfel incat sa nu ramana o singura persoana separata de restul grupului. Vom aplica acest procedeu pana cand se 
pot repartiza locuri fiecarei persoane din grup. 
* Numarul de persoane care formeaza un grup poate fi doar intre 1 si 5
* Nu se poate cumpara bilet intre o statie de plecare care se afla dupa statia de sosire sau statia de plecare si statia de sosire identice


## Descrierea algoritmului folosit

Trenul va fi reprezentat ca o lista de vagoane. Fiecare vagon va avea o lista de compartimente si fiecare compartiment o lista de locuri. 
Pentru fiecare loc se memoreaza intervalele (statie_plecare, statie_sosire) pentru care el este ocupat. 
Atunci cand se doreste  eliberarea unor noi bilete se primesc datele de intrare precizate mai sus si se parcurg urmatorii pasi:
* se obtine o lista cu toate compartimentele
* se parcurge aceasta lista si se verifica daca sunt suficiente locuri disponibile in respectivul compartiment pentru intreg grupul
* daca se gaseste un compartiment care sa verifice conditiile de mai sus, se va verifica daca el are numarul minim de locuri ocupate
* dupa ce s-au parcurs toate compartimentele, daca s-au putut atribui locuri, ele s-au rezervat in compartimentul cel mai putin ocupat
* daca nu s-au putut atribui locuri inseamna ca nu mai exista locuri suficiente astfel incat tot grupul sa stea in acelasi compartiment,
deci incercam sa ii separam in subgrupuri si sa repetam procesul de mai sus pentru fiecare subgrup
* in final se afiseaza vagonul si locurile atribuite


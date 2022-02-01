# Pràctica 2: Cerca Voraç / Optimització

## El problema

Una companyia de distribució de benzina ens demana que l’ajudem a optimitzar la distribució d’aquest 
preuat combustible entre les seves benzineres situades en una àrea delimitada. 

La companyia té #n# centres de distribució de combustible repartits geogràficament dins d’aquesta àrea. En 
cadascun hi ha un únic camió cisterna que permet portar el combustible a la benzinera que ho necessiti. Les
benzineres tenen varis dipòsits a on emmagatzemen el combustible que van servint al seus clients. Assumirem
que les benzineres serveixen el combustible d’un dipòsit fins que es buida i llavors passen a buidar el següent.  

Els camions cisterna que s’usen per l’abastiment tenen el doble de capacitat d’emmagatzemament que els
dipòsits de les benzineres. És a dir, un camió podria omplir dos dipòsits completament. Cada matí, a una
cisterna li ha d’arribar un conjunt de peticions i aquesta les ha de servir fent uns viatges específics. Tot això
és el que determinarem nosaltres usant els algorismes de cerca. 

Un camió cisterna en cada viatges que fa, primer s’omple completament, serveix les benzineres que té assignades
en aquest viatge (dos com a màxim) i torna al centre de distribució. Aquest procés es repeteix fins que s’esgoten
les peticions que ha rebut. El normal seria que, en un viatge, una cisterna omplis un diposit en dues benzineres,
però res li impedeix que una cisterna pugui en un viatge omplir dos dipòsits d’una benzinera (si aquesta té
dues peticions), o solament omplir un diposit d’una benzinera.  

Tenim la restricció de que una cisterna no pot recórrer més de #k# kilòmetres diaris i tampoc pot fer més de #v# 
viatges diaris. A més ens interessa minimitzar la distància que recorrem per abastir les benzineres.

Les peticions les genera cada benzinera a l’avisar a la companyia de distribució quan un dels seus dipòsits es 
buida. D’aquesta forma, cada dia es disposa d’un llistat de peticions de benzineres que han anat arribant i encara
no s’han pogut servir. Assumirem que poden haver-hi vàries peticions per atendre de la mateixa benzinera, una
per cada diposit que se li ha buidat. Algunes peticions poden dur varis dies sense haver estat ateses. 

Depenen del nombre de dies que porti la petició pendent, la companyia rebaixa el preu que cobra pel combustible.
Si el nombre de dies que porta una petició pendent és 0 (s’acaba de buidar el diposit) la companyia cobra un
102% del preu, a partir d’aquí el percentatge de preu que es cobra segueix la fórmula: %preu = (100 - 2*dies)%

Obviament a la companyia no li interessa deixar esperar molt les peticions. Per resoldre el problema suposarem
que l’àrea geogràfica és una quadrícula de 100x100 km<sup>2</sup> i disposem de les coordenades en les
que estan situats els centres de distribució i les benzineres (les coordenades són valors sencers). Per calcular
la distància entre els centres de distribució i les benzineres utilitzarem la següent funció:
d(D,G) = |Dx - Gx| + |Dy - Gy|
èssen Dx i Dy les coordenades x i y del centre de distribució, Gx i Gy les coordenades x i y de la benzinera.

Les dades del problema són el nombre de benzineres a abastir, les seves coordenades, les peticions que hem
de servir per cada benzinera y els dies que porten pendents, el nombre de centres de distribució i les seves
coordenades, el nombre de kilòmetres que pot recórrer en un dia i quants viatges pot fer en un dia.

L’objectiu es tribar, per cada dia, una assignació de peticions a cisternes i com aquestes es serviran, de manera
que permeti mantenir el major benefici, però minimitzant el que perdrem amb els peticions no ateses (assumint
que les atendrem el dia següent) i fent que la distància total recorreguda per les cisternes sigui la menor 
possible.

## Criteris de la solució

Per obtenir i avaluar la solució usarem els següents criteris i restriccions:
1. Les cisternes viatgen a 80Km/h i treballen durant 8h, així que podran recórrer un màxim de 640Km diaris
(assumirem que els temps de càrrega i descàrrega són instantanis).
2. Una cisterna no pot fer més de 5 viatges
3. Hem de maximitzar el benefici que obtindrem tenint en compte la pèrdua que suposa no atendre una petició
el dia actual, assumint que les peticions no ateses es podran atendre el dia següent. Assumirem que el valor
d’un diposit és de 1000
4. Hem de minimitzar també la distància que recorren assumint que hi ha un cost fix per kilòmetre recorregut.
Assumirem que el cost per kilòmetre és 2

## Generació d’escenaris

Haureu de programar unes funcions/classes per generar alelatòriament els escenaris. Com sabreu el Python té mètodes de generació de nombres aleatòris. Per tal de poder reproduïr els mateixs escenaris totes les funcions tindran coma a paràmetre la llavor (seed) per inicialitar el generador aleatori.

Concretament heu d'implementar:
* Una funció o classe que generi els centres de producció. Per cada centre de prosucció s'ha de negerar les coordenades x i y dins de l'àrea 100 x 100. La funció com a **paràmetres** té la llavor (seed) i el nobre de centres a generar

* Una funció o classe que generi les benzineres. Per cada benzinera s'ha de generar les coordenades x i y dins de l'àrea 100 x 100. La funció com a **paràmetres** té la llavor (seed) i el nobre de benzineres a generar. A més per cada benzinera s'han de generar les peticions

* Una funció o classe (que serà cridada per l'anterior) que generi les peticions. Una benzinera tindrà una única petició amb probabilitat 5%, dues amb probabilitat 65% i tres amb probabiliat 30%. Per cada petició s'ha d'establir quants dies fa que s'ha realitzat amb les següents probabilitats: 0 dies 60%, 1 dia 20%, 2 dies 15% i 3 dies 5%. Usarà la mateixa llavor (seed) que la funció de generar benzineres

## Tasques a realitzar
El desenvolupament de la pràctica implica realitzar les següents tasques:

1. Implementar la generació aleatòria d’escenaris on els paràmetres són el nombre de centres de distribució,
el nombre de benzineres i la llavor (seed) de la generació de nombres aleatoris.
2. Definir i implementar la representació de l’estat del problema per poder ser resolt usant les classes de l’AIMA.
Heu de pensar bé la representació per tal que sigui eficient en espai i temps
3. Definir i implementar un mínim de dues estratègies per generar l’estat inicial
4. Definir i implementar la funció generadora d’estats successors. Això implica decidir el conjunt d’operadors per
explorar l’espai de cerca. Heu de pensar i avaluar diferents alternatives de conjunts d’operadors. Podria ser
que fossin diferents depenent de l’estratègia de l’estat inicial
5. Definir i implementar una funció de benefici que tingui en compte els criteris de l’apartat 2. 

## Coses a lliurar

1. Implementació de les classes pertinents per poder executar el problema usant l’algorisme de cerca Hill-Climbing
2. **Experiment 1**: Experimentar amb les dues estratègies d’inicialització i també els dos conjunts d’operadors per generar
els estats successors. Escriu en l’apartat de Resultats les conclusions i si trobes alguna explicació pel que observes
3. **Experiment 2**: Hem assumit que el cost fix de 2 per Kilòmetre recorregut. Usa l’algorisme de Hill-Climbing per estudiar
com afecta al nombre de peticions servides al l’augmentar el cost per Kilòmetre. Ves doblant el cost fins que
puguis veure la tendència. Té algun efecte en la proporció de peticions servides segons el temps que porten
pendents? Escriu les conclusions d’aquest experiments a l’apartat de Resultats

## Resultats
Al fer el plantejament del problema i replantejar-lo al llarg de diversos dies vam arribar a certes conclusions que ajudaven a la implementació del problema:
- La reducció de benefici en base als dies pendents és proporcional, així que servir una petició més nova sempre donarà més benefici.
- Degut a les mides del taulell, fer una acció sempre serà millor que no fer-ne cap: en el pitjor dels casos un camió haurà de recorrer 400 km (d'una punta a l'altre del taulell, anar i tornar i servir una petició de fa 3 dies). Això vol dir que guanyaria 960 i perdria 800 en el viatge, obtenint sempre un benefici.
De totes maneres, l'algoritme té en compte el cas de que una acció no aproti més valor, que succeiria en el cas d'un taulell més gran, reduir el benefici per dipòsit servit o aumentant el cost de cada km realitzat.
- A l'hora de calcular la llista d'accions legals, hem hagut de generar totes les possibles combinacions d'anar a una benzinera i servir 1, anar a una benzinera i servir 2 i anar a dues benzineres. Però quan generem una acció comprovem si és legal. Una acció és legal si compleix totes les restriccions del problema (km restants, viatges restants) i algunes restriccions implícites (la benzinera té peticions pendents, el camió té km restants per anar però també per tornar)

La implementació del components del problema en forma de llistes (i llistes de llistes), ens va donar un problema del que no erem conscients. Al fer una copia d'una llista, si aquesta té una altra llista dins, copia la referència i no realitza una copia de la llista interna. Quan vam veure el problema, vam descobrir l'existència de la funció deepcopy(), que copia la llista i les llistes internes de forma recursiva.


### Resultats experiment 1
Després de programar-ho tot i debugar, hem arribat a una solució bastant bona. Compleix tots els requeriments i hem testejat tots els casos que se'ns han acodit: benzineres es queden amb peticions pendents perquè les distribuidores es queden sense km o viatges (taulell molt gran o moltes benzineres i poques distribuidores), distribuidores no es mouen perquè s'han servit totes les peticions (moltes distribuidores, poques benzineres), casos ràpids de poques distribuidores i poques benzineres i casos lents de moltes distribuidores i moltes benzineres.

El resultat obtingut és un dels millors, si no el millor que hi ha. Això és degut a com és aquest problema concret i al fet de començar de 0 (0 valor i cap acció realitzada). Per la forma en la que hem plantejat el problema i com l'hem implementat, els casos en els que el Hill-Climbing no dona la millor solució són molt extranys, ja que són combinacions de posicionaments de distribuidores, benzineres, distàncies i km/viatges restants molt específics.

Cal destacar, que al incrementar el nombre de distribuidores o benzineres, el temps que triga en pendre cada decisió s'incrementa considerablement, ja que ha de calcular totes les combinacions i per cadascuna d'aquestes comprovar si és legal. Per exemple, 10 distribuidores i 10 benzineres s'executen en menys de 2 segons, mentre que 20 i 20 triguen uns 30 segons.


### Resultats experiment 2
En aquest experiment, hem canviat l'implementació de manera que es dona preferència a les peticions més antigues (més dies pendents).

En contra del que pensàvem (que donar preferència a les més noves dona sempre millor resultat), hem comprovat que amb aquesta nova implementació, en alguns casos, s'obté un major benefici. Segons la situació: l'exercici 1 dona millors resultats, l'exercici 2 dona millors resultats o ambdós exercicis obtenen el mateix.
Per exemple, amb seeds 0 per distribuidores i 0 per benzineres:
- 5 benzineres i 5 distribuidores, l'exercici 1 obté un millor resultat.
- 7 benzineres i 7 distribuidores, els dos exercicis obtenen el mateix resultat.
- 10 benzineres i 10 distribuidores, l'exercici 2 obté un millor resultat.

Després d'analitzar les accions realitzades en cada cas, hem arribat a la conclusió de que, tot i que la primera implementació obté un major benefici en cada acció, a la última (o últimes) accions es veu obligat a fer una acció que li dona menys benefici que la última acció de la segona implementació. Per exemple, la última acció del exercici 1 és una petició de fa 2 dies i que està bastant lluny, mentre que la última de l'exercici 2 és una acció de fa 0 dies (perquè al principi ha donat preferència a les més antigues) i que li queda més a prop, per tant obté més benefici pel dipòstit i fa menys km.
Aquesta diferència a la última acció ve donada perquè al donar prefèrencia a l'oposat, les accions agafades són diferents, i aquesta combinació tan diferent deriva en un resultat o un altre depenent del taulell inicial.


![alt text](/Solucions.JPG)

Com podem veure en aquest cas (seeds 0 i 0 respectivament, 7 distribuidores i 8 benzineres), la primera acció que agafen és exactament la mateixa, però l'exercici 1 obté més benefici perquè ha servit dos peticions de fa 0 dies, mentre que l'exericici 2 n'ha servit una de fa 1 dia i una de fa 0 dies.

Això es repeteix durant 3 accions més, i a partir d'aquí començen a escollir accions diferents. Durant totes les accions l'exercici 1 obté millors beneficis, però a l'última acció l'exercici dos remunta i acaba obtenint un millor benefici total:

- Com podem comprovar, l'última acció del cas 1 [[38, 61, 1, 68], [17, 36, [1]], [78, 81, [3]]], ha de fer un camí molt llarg per servir una petició de fa 1 dia i una de fa 2 dies.
- Per contra, l'última acció del cas 2 [[45, 74, 1, 80], [78, 81, [0]], [42, 31, [0]]], fa un camí més curt i serveix dues peticions de fa 0 dies, així que acaba amb un increment dels beneficis suficient com per superar el benefici final del seu oposat.

## Crèdits
Exercici extret de la col·lecció d'exercicis publicats a la UPC amb la licència Creative Commons


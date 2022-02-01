# Pràctica 1: Cerca - Evitar obstacles 

## El problema
Hem de trobar el camí més curt entre dos punts en un pla que té obstacles representats per poligons convexos (sense concavitats).
De fet això és una simplificació del problema que té un robot per anar d'un punt a un altre en un entorn amb obstacles.

1. Suposem que l'espai d'estats consisteix en totes les posicions (x, y) en el pla. Quants estats hi ha en el pla? Quants 
camins hi ha entre l'orígen i el destí?
2. Pregunta pista: explica breument per què el camí més curt entre el vèrtex d'un polígon a qualsevol altre punt de l'escena
consistirà en una seqüència de segments rectes que uneixen diferents vèrtex dels polígons. En aquest cas, quin és l'espai
d'estats?
3. Defineix les funcions necessàries per implementar el problema de cerca. Pensa que les accions tindràn com a paràmetre
el punt (probablement un vèrtex) de partida, és a dir, l'estat actual.
4. Pensa en quina pot ser una bona funció heurística, h()
5. Aplica els algorismes de cerca vists a classe i compara'ls en termes de rendiment
Respon a les preguntes anteriors en aquest mateix fitxer a l'apartat de respostes

## Exemple:
* Orígen: (1,1)
* Destí: (18,13)
* Poligons: {((0.62, 2)(2,1.5)(2.3,3.2)) ((4,4)(4,2)(12,2)(12,4)) ((2.5,6.75)(2.5,4.5)(5,6.6)) ((6,8)(6,5)(9,5)(9,8))
((10,12)(10,5)(12,5)(12,12)) ((13,1)(16,6)(19,1)) ((13,9)(15,6)(16,9)) ((14,12)(14,11)(20,11)(20,12)}

![alt text](https://github.com/TecniquesIntelligenciaArtificial17-18/Practica1_1819/images/escena.png "Exemple escena")


# Respostes

Representació gràfica de la solució del problema (camí més curt trobat amb algoritme A* i Uniform Cost-Dijkstra):
![Alt text](/images/solution_astar.jpg?raw=true "shortest_path")

Representació gràfica del camí que passa per menys nodes (trobat amb algoritme BFS):
![Alt text](/images/solution_bfs.jpg?raw=true "less_nodes_path")

Representació gràfica d'un camí aleatori (trobat amb algoritme DFS):
![Alt text](/images/solution_dfs.jpg?raw=true "random_path")


1. El pla va de (-infinit, -infinit) a (+infinit, +infinit), passant per tots els nombres reals. Per tant, com l'estat ve definit per la posició, hi ha diferents estats.
	Hi ha infinits camins possibles ja que al tractar-se d'un pla infinit i no discret hi ha infinites permutacions possibles per arribar d'un punt A un punt B.
	
    >En aquest cas, l'espai d'estats vindrà donat pel producte de les dimensions del pla menys l'àrea dels polígons que obstaculitzen.   
	>És a dir *〈 Espai d'estats = x * y - ÀreaPolígons 〉*

   Després de pensar com reduir les infinites opcions, ens adonem que els possibles camins passaràn obligatòriament pels vèrtex dels poligons, mai per un punt qualsevol del pla.
   Amb aquesta conclusió, les respostes passen a ser: 
   
    >nEstats = n + 2 . On n és el nombre de nodes i el +2 és degut a l'estat de la posició inicial i la posició final, que no són vèrtex dels polígons.  
	>nCamins = (n-1)! - {# camins prohibits}. On n és el nombre de nodes i un camí prohibit és un camí que inclou un moviment entre nodes que no estàn directament connectats. Aquesta resta és deguda a que (n-1)! no és exacte, ja que considera que tots els nodes estàn connectats amb la resta de nodes. I sabem que no és així, ja que els polígons han fet que hi hagi nodes sense una connecxió directa entre ells.
	El nombre de camins prohibits depen de la disposició dels polígons, i per tant, del problema. La única manera de saber exactament el nombre de camins és amb algoritmes de cerca, com el backtracking entre d'altres. Per aquest motiu, en problemes amb molts nodes, calcular el nombre de camins amb aquest mètode és enormement costós en temps i memòria.  
   
   Exemple (Origen: node 1, Destí: node 4):
   
   ![Alt text](/images/exemple1.jpg?raw=true "exemple1")
   
   En aquest cas, com tots els nodes estàn connectats entre ells, (n-1)! ja dona el nombre exacte. # camins = (4-1)! - 0 = 6
   
   ![Alt text](/images/exemple2.jpg?raw=true "exemple2")
   
   En aquest altre cas, veiem clarament que només hi ha 2 camins possibles (sense passar 2 cops pel mateix node). Per tant: # camins = (4-1)! - 4 = 2. Perquè dels 6 camins, 4 d'ells inclouen un salt entre 1 i 4 o 2 i 3.
   
   ![Alt text](/images/exemple3.jpg?raw=true "exemple3")
   
   En aquest últim cas, hem portat l'exemple al extrem, on no hi ha cap solució. Si consideressim només (n-1)! el resultat s'allunya molt de la realitat, així que al fer la resta quedaria: # camins = (4-1)! - 6 = 0. Ja que tots els camins inclouen algun moviment entre un node i el node 4, que no està connectat a cap.
	


   
2. Donat que el camí més curt entre 2 punts és una línea recta, si un polígon convex intersecta amb aquesta línea, el camí més curt per rodejar-lo serà seguir el seu perímetre.
   A més, gràcies al teaorema de pitàgores, sabem que la hipotenusa d'un triangle rectangle sempre és més curta que la suma dels seus catets. Per aquest motiu, per anar d'un polígon a un altre, el camí més curt sempre serà anar de vèrtex a vèrtex, passant per la hipotenusa d'un triangle imaginari, mai serà anar fins al punt intermig d'una arista i d'aquí anar fins al vèrtex.
	


3. **INIT()**: Especifiquem el l'estat d'inicial i l'estat final. En el nostre cas es tracta del node origen (1, 1) i el node destí (18, 13).  
   **ACTIONS(state)**: En aquest cas, l'estat que ens arriba per paràmetre és el node on ens trobem, i per tant les accions possibles son tots els nodes adjacents a ell.  
   **RESULT(state, action)**: Comparem l'estat actual, que és un node, amb l'estat final que hem definit al inici que també és un node.  	**H(node)**: La funció heurística que utilitzem per l'algoritme A*: consisteix en la distància vectorial, és a dir el mòdul, entre el node que ens arriba per paràmetre i el node destí.  
   **PATH_COST(c, state1, action, state2)**: funció que retorna el cost real d'arribar des de l'estat inicial fins el node en el que es troba, aquest cost és la suma del cost d'arribar al node anterior (paràmetre c) + el cost d'arribar des d'aquest últim node fins el node actual (distància lineal entre els paràmetres state1 i state2). Al sumar aquest cost amb la funció heurística, obtenim el valor amb el que l'algoritme A* ordena la seva llista de prioritat.  

4. h(n) = D(n, destí). On n és el node actual (inici, destí o vèrtex) i D(n, destí) és la distància lineal entre el node i el punt destí. Aquesta sería una bona funció heurística, perquè sempre serà igual o més petita que el cost real. La distància real per arribar al destí mai serà més petita que la distància lineal entre el node i el destí.

5. El rendiment dels algoritmes utilitzats és:  
![Alt text](/images/rendiment.jpg?raw=true "rendiment")  
Per fer la comparació ignorarem la eficiencia dels algoritmes Depth First Search i Breadth First Search, ja que DFS i BFS no busquen el mateix que els altres dos algoritmes, sino que cerquen un camí aleatori i el camí que passa per menys nodes, respectivament.  
Com podem comprovar, tot i que els algoritmes A* i Uniform Cost cerquen el camí més curt, l'A* expandeix, evalua i visita pràcticament un 50% menys de nodes. Això és degut a que al utilitzar l'heurístic a l'hora de calcular els costos, l'algoritme evita anar en la direcció oposada al objectiu tot i que els costos immediats d'anar cap aquells nodes siguin més petits.
Per aquest motiu podem afirmar que l'algoritme A* és molt més eficient que l'algoritme Uniform Cost-Dijkstra.
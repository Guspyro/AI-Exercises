import random
import search
import copy


# estructures no OOP
#  - benzinera      = [ pos_y, pos_x, peticions ]
#  - peticions      = [ dia, dia, ... ]
#  - distribuidor   = [ pos_y, pos_x, num_viatges_realitzats, km_realitzats ]


# dades problema
grid_x = 100
grid_y = 100
grid = [[-1 for i in range(grid_x)] for j in range(grid_y)]
llista_peticions = list()
llista_benzineres = list()
llista_distribuidors = list()


# restriccions problema
MAX_KMH = 80                            # (usat)
MAX_HORES = 8                           # (usat)
MAX_KM_PER_DIA = MAX_HORES * MAX_KMH    # (usat)
MAX_VIATGES_CAMIO = 5                   # (usat)
MAX_DIPOSITS_CAMIO = 2                  # (usat en implementació)
COST_KM = 2                             # (usat)
VALOR_DIPOSIT = 1000                    # (usat)
#MAX_DIPOSITS_BENZINERA = 2             (no cal usar)


#  d(D,G) = |Dx - Gx| + |Dy - Gy|
def distance (distribuidor, benzinera):
    return abs(distribuidor[0] - benzinera[0]) + abs(distribuidor[1] - benzinera[1])


# funcio que generi distribuidors
def gen_distribuidors (seed, num_centres):
    random.seed(seed)
    for i in range(0, num_centres):
        distrib_added = False
        while not distrib_added:
            rand_x = random.randint(0, grid_x - 1)
            rand_y = random.randint(0, grid_y - 1)
            if (grid[rand_x][rand_y] == -1):
                # afegeix distrib a grid
                grid[rand_x][rand_y] = [rand_x, rand_y, 0, 0]
                # afegeix distrib a llista
                llista_distribuidors.append([rand_x, rand_y, 0, 0])
                distrib_added = True


# funcio que generi peticions cridada per gen_benzineres
def gen_peticions():
    peticions = list()
    prob_num_peticions = random.uniform(0.0, 1.0)
    if prob_num_peticions < 0.05:
        num_peticions = 1
    elif 0.05 <= prob_num_peticions < 0.7:
        num_peticions = 2
    else:
        num_peticions = 3

    dies_pendents = 0
    for i in range(0, num_peticions):
        prob_dies_pendents = random.uniform(0.0, 1.0)
        if prob_dies_pendents < 0.6:
            dies_pendents = 0
        elif 0.6 <= prob_dies_pendents < 0.8:
            dies_pendents = 1
        elif 0.8 <= prob_dies_pendents < 0.95:
            dies_pendents = 2
        else:
            dies_pendents = 3
        peticions.append(dies_pendents) # afegeix petició
    return peticions


# funcio que generi benzineres on per cada benzinera cal generar peticions
def gen_benzineres (seed, num_benzineres):
    random.seed(seed)
    for i in range(0, num_benzineres):
        benz_added = False
        while not benz_added:
            rand_x = random.randint(0, grid_x - 1)
            rand_y = random.randint(0, grid_y - 1)
            if (grid[rand_x][rand_y] == -1):
                peticions = gen_peticions()
                # afegeix benzinera i genera peticions a grid
                benzinera = list()
                benzinera.append(rand_x)
                benzinera.append(rand_y)
                benzinera.append(peticions)
                grid[rand_x][rand_y] = benzinera
                # afegeix benzinera i genera peticions a llista
                llista_benzineres.append(benzinera)
                benz_added = True


# grid generation
gen_distribuidors(0, 5)
gen_benzineres(0, 5)




# EXPERIMENT 1 of 2
class ExerciseProblem1(search.Problem):

        def __init__(self):
            # our custom attributes
            #self.actionsPossibles = self.get_possible_initial_actions()
            #self.actionsToPrune = set()

            self.initial = self.get_initial_state()
            search.Problem.__init__(self, self.initial)
            print("Benefici després de cada acció: ", end = '')

        def actions(self, state):
            print(str(state["value"]) + ", ", end = '')
            return self.get_legal_actions(state)

        def result(self, state, action):
            return self.get_next_state( state, action)

        def value(self, state):
            return self.compute_value(state)



        def get_initial_state(self):
            state = dict()
            state["accions_realitzades"] = list()
            state["distribuidores"] = llista_distribuidors.copy()
            state["benzineres"] = llista_benzineres.copy()
            state["value"] = 0
            state["value_calculat"] = False #Paràmetre per distingir si es tracta del calcul i assignació real del valor (get_next_state) o és l'algoritme fent una comprovació de valor.
                                      #Si no fem aquesta distinció, al fer la comprovació, torna a afegir el valor de l'acció tot i que ja estava afegit

            return state

        def get_next_state(self, state, action):
            # returns a new SUPPOSED state based on the current state and the new action performed
            new_state = copy.deepcopy(state) # non destructive
            new_state["value_calculat"] = False
            new_state["accions_realitzades"].append(action)
            #possible_actions = new_state[1]
            for d in new_state["distribuidores"]:
                if d == action [0]:
                    d[2] += 1  # sumem un viatge a la distribuidora
                    if (action[2] == 1) or (action[2] == 2): #restem la distància del viatge
                        d[3] +=  distance(action[0], action[1]) * 2
                    else:
                        d[3] += (distance(action[0], action[1]) + distance(action[1], action[2]) + distance(action[2], action[0]))


            for b in new_state["benzineres"]:
                if action[2] == 1 and b == action[1]:
                    b[2].remove(self.get_peticio_mes_nova(b[2]))

                elif action[2] == 2 and b == action[1]:
                    b[2].remove(self.get_peticio_mes_nova(b[2]))
                    b[2].remove(self.get_peticio_mes_nova(b[2]))

                elif b == action[1] or b == action[2]:
                    b[2].remove(self.get_peticio_mes_nova(b[2]))


            new_state["value"] = self.compute_value(new_state)
            new_state["value_calculat"] = True
            return new_state

        # estimar el cost d'un estat per poder estriar de manera voraç
        def compute_value(self, state):

            value = state["value"]
            if state["value_calculat"]:
                return value


            if len(state["accions_realitzades"]) == 0:
                return value
            action = state["accions_realitzades"][-1] #La última acció serà la que hem afegit al nou state i sobre la que hem de calcular el value
            if action[2] == 1:
                value -= distance(action[0], action[1]) * 2 * COST_KM

                peticions = action[1][2]

                benefici_diposit = self.compute_pct_cost_devaluation(self.get_peticio_mes_nova(peticions))

                value += benefici_diposit

            elif action[2] == 2:
                value -= distance(action[0], action[1]) * 2 * COST_KM

                peticions = action[1][2]

                benefici_diposit_1 = self.compute_pct_cost_devaluation(self.get_peticio_mes_nova(peticions))
                value+= benefici_diposit_1

                benefici_diposit_2 = self.compute_pct_cost_devaluation(self.get_segona_peticio_mes_nova(peticions))
                value+=benefici_diposit_2

            else:
                value -= (distance(action[0], action[1]) + distance(action[1], action[2]) + distance(action[2], action[0])) * COST_KM

                peticions_benz_1 = action[1][2]
                benefici_diposit_benz_1 = self.compute_pct_cost_devaluation(self.get_peticio_mes_nova(peticions_benz_1))
                value+=benefici_diposit_benz_1


                peticions_benz_2 = action[2][2]
                benefici_diposit_benz_2 = self.compute_pct_cost_devaluation(self.get_peticio_mes_nova(peticions_benz_2))
                value+=benefici_diposit_benz_2
            return value


        # calcul el percentatge en el que un bidó (1000) es devalua amb els dies pendents que porta la petició
        def compute_pct_cost_devaluation(self, dies):
            if dies == 0:
                return 1.02 * VALOR_DIPOSIT
            else:
                return VALOR_DIPOSIT * ((100 - 2 * dies) / 100)


        def get_peticio_mes_nova(self, peticions): #donar preferència a les peticions més noves ens donarà més benefici aquest dia que servir una d'un dia anterior
            return min(peticions)

        def get_segona_peticio_mes_nova(self, peticions): #serveix per calcular el benefici quan servim dues peticions, com al calcular no borrem de la llista, no podem agafar la més antiga dos cops
            peticionscopy = peticions.copy()
            peticionscopy.remove(self.get_peticio_mes_nova(peticionscopy))

            return min(peticionscopy)

        # # returns all possible initial actions
        # def get_possible_initial_actions(self):
        #     # accio servir = [ from_distrib, to_benz ]
        #     actions = list()
        #     for distribuidor in llista_distribuidors:
        #         for benzinera1 in llista_benzineres:
        #             actions.append([distribuidor, benzinera1, 1])
        #             actions.append([distribuidor, benzinera1, 2])
        #             for benzinera2 in llista_benzineres:
        #                 if benzinera1 == not benzinera2:
        #                     actions.append([distribuidor, benzinera1, benzinera2])
        #     return actions


        # def pruneCamio(self, camio):
        #     for a in self.actionsPossibles:
        #         if a[0] == camio:
        #             self.actionsToPrune.add(a)
        #
        # def pruneBenzinera(self, benzinera):
        #     for a in self.actionsPossibles:
        #         if (a[1] == benzinera) or (a[2] == benzinera):
        #             self.actionsToPrune.add(a)

        def legal(self, action):
            # An action == legal if:
            # - camió no supera kms
            # - camió té kms per tornar a casa
            # - camió no supera n viatges
            # - benzinera destí té peticions pendents (sinó considero il.legal fer un viatge absurd)

            camio = action[0]
            benzinera1 = action[1]
            benzinera2  = action[2]

            is_legal = False
            if (camio[3] < MAX_KM_PER_DIA  # camió no supera kms
            and camio[2] < MAX_VIATGES_CAMIO):  # camió no supera n viatges

                if len(benzinera1[2]) <= 0:  # benzinera destí no té peticions pendents
                    #self.pruneBenzinera(benzinera1)
                    return False
                if benzinera2 == 1 or benzinera2 == 2:

                    if distance(camio, benzinera1)*2 <= (MAX_KM_PER_DIA - camio[3]): # camió té km per tornar a casa
                        is_legal = True
                    if len(benzinera1[2]) == 1 and benzinera2 == 2:
                        return False
                else:
                    if len(benzinera2[2]) <= 0:  # benzinera destí té peticions pendents
                        #self.pruneBenzinera(benzinera2)
                        return False
                    if distance(camio, benzinera1) + distance(benzinera1, benzinera2) + distance(benzinera2,camio) <= (MAX_KM_PER_DIA - camio[3]): # camió té km per tornar a casa
                        is_legal = True

            else:
                #self.pruneCamio(camio)
                return False

            return is_legal


        def get_legal_actions(self, state):

            actions = list()
            for distribuidor in state["distribuidores"]:
                for benzinera1 in state["benzineres"]:
                    action1 = [distribuidor, benzinera1, 1]
                    if self.legal(action1):
                        actions.append(action1)


                    action2 = [distribuidor, benzinera1, 2]
                    if self.legal(action2):
                        actions.append(action2)


                    for benzinera2 in state["benzineres"]:
                        if benzinera1 != benzinera2:
                            action3 = [distribuidor, benzinera1, benzinera2]
                            if self.legal(action3):
                                actions.append(action3)
            return actions


            # copiaActionsPossibles = self.actionsPossibles.copy()
            # for action in copiaActionsPossibles:
            #     if not self.legal(action):
            #         self.actionsPossibles.remove(action)
            #
            # self.actionsPossibles - self.actionsToPrune
            # self.actionsToPrune = set()



print("Llista de distribuidors inicial:")
print(llista_distribuidors)

print("Llista de benzineres inicial:")
print(llista_benzineres)


print("\nSolució Exercici1 -----")
sol = search.hill_climbing(ExerciseProblem1())
print("\nAccions realitzades: " + str(sol["accions_realitzades"]))
print("Llista de distribuidors final: " + str(sol["distribuidores"]))
print("Llista de benzineres final: " + str(sol["benzineres"]))
print("Benefici aconseguit: " + str(sol["value"]))



# EXPERIMENT 2 of 2
class ExerciseProblem2(search.Problem):

    def __init__(self):
        # our custom attributes
        # self.actionsPossibles = self.get_possible_initial_actions()
        # self.actionsToPrune = set()

        self.initial = self.get_initial_state()
        search.Problem.__init__(self, self.initial)
        print("Benefici després de cada acció: ", end='')

    def actions(self, state):
        print(str(state["value"]) + ", ", end='')
        return self.get_legal_actions(state)

    def result(self, state, action):
        return self.get_next_state(state, action)

    def value(self, state):
        return self.compute_value(state)

    def get_initial_state(self):
        state = dict()
        state["accions_realitzades"] = list()
        state["distribuidores"] = llista_distribuidors.copy()
        state["benzineres"] = llista_benzineres.copy()
        state["value"] = 0
        state["value_calculat"] = False  # Paràmetre per distingir si es tracta del calcul i assignació real del valor (get_next_state) o és l'algoritme fent una comprovació de valor.
                                         # Si no fem aquesta distinció, al fer la comprovació, torna a afegir el valor de l'acció tot i que ja estava afegit

        return state

    def get_next_state(self, state, action):
        # returns a new SUPPOSED state based on the current state and the new action performed
        new_state = copy.deepcopy(state)  # non destructive
        new_state["value_calculat"] = False
        new_state["accions_realitzades"].append(action)
        # possible_actions = new_state[1]
        for d in new_state["distribuidores"]:
            if d == action[0]:
                d[2] += 1  # sumem un viatge a la distribuidora
                if (action[2] == 1) or (action[2] == 2):  # restem la distància del viatge
                    d[3] += distance(action[0], action[1]) * 2
                else:
                    d[3] += (distance(action[0], action[1]) + distance(action[1], action[2]) + distance(action[2],
                                                                                                        action[0]))

        for b in new_state["benzineres"]:
            if action[2] == 1 and b == action[1]:
                b[2].remove(self.get_peticio_mes_antiga(b[2]))

            elif action[2] == 2 and b == action[1]:
                b[2].remove(self.get_peticio_mes_antiga(b[2]))
                b[2].remove(self.get_peticio_mes_antiga(b[2]))

            elif b == action[1] or b == action[2]:
                b[2].remove(self.get_peticio_mes_antiga(b[2]))

        new_state["value"] = self.compute_value(new_state)
        new_state["value_calculat"] = True
        return new_state

    # estimar el cost d'un estat per poder estriar de manera voraç
    def compute_value(self, state):

        value = state["value"]
        if state["value_calculat"]:
            return value

        if len(state["accions_realitzades"]) == 0:
            return value
        action = state["accions_realitzades"][
            -1]  # La última acció serà la que hem afegit al nou state i sobre la que hem de calcular el value
        if action[2] == 1:
            value -= distance(action[0], action[1]) * 2 * COST_KM

            peticions = action[1][2]

            benefici_diposit = self.compute_pct_cost_devaluation(self.get_peticio_mes_antiga(peticions))

            value += benefici_diposit

        elif action[2] == 2:
            value -= distance(action[0], action[1]) * 2 * COST_KM

            peticions = action[1][2]

            benefici_diposit_1 = self.compute_pct_cost_devaluation(self.get_peticio_mes_antiga(peticions))
            value += benefici_diposit_1

            benefici_diposit_2 = self.compute_pct_cost_devaluation(self.get_segona_peticio_mes_antiga(peticions))
            value += benefici_diposit_2

        else:
            value -= (distance(action[0], action[1]) + distance(action[1], action[2]) + distance(action[2],
                                                                                                 action[0])) * COST_KM

            peticions_benz_1 = action[1][2]
            benefici_diposit_benz_1 = self.compute_pct_cost_devaluation(self.get_peticio_mes_antiga(peticions_benz_1))
            value += benefici_diposit_benz_1

            peticions_benz_2 = action[2][2]
            benefici_diposit_benz_2 = self.compute_pct_cost_devaluation(self.get_peticio_mes_antiga(peticions_benz_2))
            value += benefici_diposit_benz_2
        return value

    # calcul el percentatge en el que un bidó (1000) es devalua amb els dies pendents que porta la petició
    def compute_pct_cost_devaluation(self, dies):
        if dies == 0:
            return 1.02 * VALOR_DIPOSIT
        else:
            return VALOR_DIPOSIT * ((100 - 2 * dies) / 100)

    def get_peticio_mes_antiga(self,
                             peticions):  # donar preferència a les peticions més noves ens donarà més benefici aquest dia que servir una d'un dia anterior
        return max(peticions)

    def get_segona_peticio_mes_antiga(self,
                                    peticions):  # serveix per calcular el benefici quan servim dues peticions, com al calcular no borrem de la llista, no podem agafar la més antiga dos cops
        peticionscopy = peticions.copy()
        peticionscopy.remove(self.get_peticio_mes_antiga(peticionscopy))

        return max(peticionscopy)


    def legal(self, action):
        # An action == legal if:
        # - camió no supera kms
        # - camió té kms per tornar a casa
        # - camió no supera n viatges
        # - benzinera destí té peticions pendents (sinó considero il.legal fer un viatge absurd)

        camio = action[0]
        benzinera1 = action[1]
        benzinera2 = action[2]

        is_legal = False
        if (camio[3] < MAX_KM_PER_DIA  # camió no supera kms
                and camio[2] < MAX_VIATGES_CAMIO):  # camió no supera n viatges

            if len(benzinera1[2]) <= 0:  # benzinera destí no té peticions pendents
                # self.pruneBenzinera(benzinera1)
                return False
            if benzinera2 == 1 or benzinera2 == 2:

                if distance(camio, benzinera1) * 2 <= (MAX_KM_PER_DIA - camio[3]):  # camió té km per tornar a casa
                    is_legal = True
                if len(benzinera1[2]) == 1 and benzinera2 == 2:
                    return False
            else:
                if len(benzinera2[2]) <= 0:  # benzinera destí té peticions pendents
                    # self.pruneBenzinera(benzinera2)
                    return False
                if distance(camio, benzinera1) + distance(benzinera1, benzinera2) + distance(benzinera2, camio) <= (
                        MAX_KM_PER_DIA - camio[3]):  # camió té km per tornar a casa
                    is_legal = True

        else:
            # self.pruneCamio(camio)
            return False

        return is_legal

    def get_legal_actions(self, state):

        actions = list()
        for distribuidor in state["distribuidores"]:
            for benzinera1 in state["benzineres"]:
                action1 = [distribuidor, benzinera1, 1]
                if self.legal(action1):
                    actions.append(action1)

                action2 = [distribuidor, benzinera1, 2]
                if self.legal(action2):
                    actions.append(action2)

                for benzinera2 in state["benzineres"]:
                    if benzinera1 != benzinera2:
                        action3 = [distribuidor, benzinera1, benzinera2]
                        if self.legal(action3):
                            actions.append(action3)
        return actions



print("\nSolució Exercici2 -----")
sol = search.hill_climbing(ExerciseProblem2())
print("\nAccions realitzades: " + str(sol["accions_realitzades"]))
print("Llista de distribuidors final: " + str(sol["distribuidores"]))
print("Llista de benzineres final: " + str(sol["benzineres"]))
print("Benefici aconseguit: " + str(sol["value"]))



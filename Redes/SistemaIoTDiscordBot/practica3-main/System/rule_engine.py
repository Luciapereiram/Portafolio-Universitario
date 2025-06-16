import re
import datetime

class RuleEngine:
    """ Clase RuleEngine, quien se encarga del manejo de reglas. """

    def __init__(self):
        """ Constructor de la clase RuleEngine. """

        # Para llevar un control de los dispositivos del sistema
        self.devices = {}


    def add_device(self, device, state):
        """ Funcion que agrega un nuevo dispositivo al sistema. """

        if device in self.devices.keys():
            return False

        self.devices[device] = state

        return True


    def remove_device(self, device):
        """ Funcion que elimina un determinado dispositivo del sistema. """

        if device not in self.devices.keys():
            return False

        self.devices.pop(device)

        return True


    def list_devices(self):
        """ Funcion que lista todos los dispositivos del sistema. """

        devices_list = "List of system devices:\n"

        for device, state in self.devices.items():
            devices_list += f'{device} state: {state}\n'

        return devices_list


    def set_device_state(self, device, state):
        """Funcion que establece el valor del estado de un dispositivo. """

        if device not in self.devices.keys():
            return False

        self.devices[device] = state
        return True


    def add_rule(self, rule):
        """Funcion que agrega una regla al sistema. """

        with open('System/system_rules.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if rule == line[0:len(line)-1]:
                    return False 
        
        with open('System/system_rules.txt', 'a') as file:
            file.write(f'{rule}\n')
        
        return True


    def remove_rule(self, rule):
        """Funcion que elimina una regla del sistema. """

        found = False

        with open('System/system_rules.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if rule+"\n" == line:
                    found = True
                    break
        
        if found == False:
            return False

        # Sobreescribir fichero
        with open('System/system_rules.txt', 'w') as file:
            for rule in lines:
                if rule != line:
                    file.write(line)

        return True
    

    def list_rules(self):
        """ Funcion que lista todas las reglas. """

        rules_list = "List of system rules:\n"

        with open('System/system_rules.txt', 'r') as file:
            for num, line in enumerate(file.readlines()):
                rules_list += f'{num}) {line}'

        return rules_list


    def match_rule(self):
        """ Funcion que comprueba si alguna regla se activa al cambiar 
        el estado de un dispositivo determinado, y retorna las acciones a realizar
        si esto ocurre. """

        with open('System/system_rules.txt', 'r') as file:
            actions = []

            # Por cada regla
            for line in file.readlines():
                if line == "\n":
                    pass

                # Recoger condiciones y accion a realizar
                rule = line.split('then')

                # Se quita el if y los espacios del principio y del final
                conditions = rule[0].strip()[3:]
                then = rule[1].strip()
                
                # print(f'CONDICIONES:\nCondicion->{conditions} Accion->{then}')

                # Por si hubiera mas de una condicion
                each_condition = re.split(r' (and|or) ', conditions)

                operands = []
                conditions_results = []

                # Mas de una condicion
                if len(each_condition) > 1:
                
                    # print(f'Lista condiciones->{each_condition}')

                    for c in each_condition:
                        if c == 'and' or c == 'or':
                            operands.append(c)
                        else:
                            # Recoger dispositivo, comparador y valor
                            device, comparator, value = re.split(r' (==|!=|>|<|>=|<=|=>|=<) ', c)
                            # print(f'\nDevice: {device}  Comparador: {comparator}  Valor: {value}\n')

                            # Comprobar si el dispositivo aun esta en el sistema
                            if device in self.devices.keys():
                                # Agregar el resultado de la comparacion
                                conditions_results.append(self.auto_comparator(device[:-1], self.devices[device], comparator, value))
                                
                            else:
                                # Damos por hecho que no se cumple la regla
                                conditions_results.append(False)

                    print("- Operandos: ", operands)
                    print("- Resultados: ", conditions_results)

                    i = 0
                    result = conditions_results[0]

                    for o in operands:
                        if o == 'and':
                            result = result and conditions_results[i+1]

                        elif o == 'or':
                            result = result or conditions_results[i+1]

                        i += 1

                    print("Resultado final: ",result)

                    if result is True:
                        new_action = then.split(' ')
                        if self.devices[new_action[0]] != new_action[2]:
                            actions.append(then)

                # Una unica condicion
                else:
                    # Recoger dispositivo, comparador y valor
                    device, comparator, value = re.split(r' (==|!=|>|<|>=|<=|=>|=<) ', conditions)
                    # print(f'\nDevice: {device}  Comparador: {comparator}  Valor: {value}\n')

                    # Comprobar si el dispositivo aun esta en el sistema
                    if device in self.devices.keys():
                        # Recoger el resultado de la comparacion
                        comparacion = self.auto_comparator(device[:-1], self.devices[device], comparator, value)

                    else:
                        # Damos por hecho que no se cumple la regla
                        comparacion = False

                    if comparacion == True:
                        new_action = then.split(' ')
                        if new_action[0] in self.devices.keys() and self.devices[new_action[0]] != new_action[2]:
                            actions.append(then)

            return actions


    def auto_comparator(self, device, value1, comparator, value2):
        """ Funcion que dado un comparador en formato String, realiza la comparacion correspondiente. """
        
        if device == "sensor":
            v1 = int(value1)
            v2 = int(value2)
        elif device == "clock":
            v1 = datetime.datetime.strptime(value1, '%H:%M:%S')
            v2 = datetime.datetime.strptime(value2, '%H:%M:%S')

        if comparator == '==':
            if v1 == v2:
                return True
        elif comparator == '!=':
            if v1 != v2:
                return True
        elif comparator == '>':
            if v1 > v2:
                return True
        elif comparator == '<':
            if v1 < v2:
                return True
        elif comparator == '>=' or comparator == '=>':
            if v1 >= v2:
                return True
        elif comparator == '<=' or comparator == '=<':
            if v1 <= v2:
                return True
                
        

        return False
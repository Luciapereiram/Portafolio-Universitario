import ast

class MaliciousCodeChecker(ast.NodeVisitor):
    """
    Recorre el árbol de sintaxis abstracta para verificar si se usan términos maliciosos.
    """
    def __init__(self, blacklist):
        """
        Inicializa el detector con una lista de términos maliciosos.

        :param blacklist: Lista de nombres a considerar maliciosos.
        """
        self.blacklist = blacklist
        self.found_malicious = []

    def visit_Import(self, node):
        # Detecta importaciones del tipo: import module_name
        for alias in node.names:
            if alias.name in self.blacklist:
                self.found_malicious.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        # Detecta importaciones del tipo: from module_name import ...
        if node.module in self.blacklist:
            self.found_malicious.append(node.module)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Detecta atributos como: module_name.some_method()
        if isinstance(node.value, ast.Name) and node.value.id in self.blacklist:
            self.found_malicious.append(node.value.id)
        self.generic_visit(node)

    def visit_Call(self, node):
        # Detecta llamadas a funciones como eval() o exec()
        if isinstance(node.func, ast.Name) and node.func.id in self.blacklist:
            self.found_malicious.append(node.func.id)
        self.generic_visit(node)

def validate_code(code, blacklist):
    """
    Valida que el código proporcionado no utilice términos maliciosos de la lista.

    :param code: Código Python como cadena.
    :param blacklist: Lista de términos maliciosos a buscar.
    :return: Tupla (bool, mensaje).
    """
    try:
        # Convierte el código en un árbol AST
        tree = ast.parse(code)
        checker = MaliciousCodeChecker(blacklist)
        checker.visit(tree)
        if checker.found_malicious:
            return False, f"Código contiene elementos maliciosos: {', '.join(set(checker.found_malicious))}."
        return True, "El código es seguro."
    except SyntaxError as e:
        return False, f"Error de sintaxis en el código: {e}"


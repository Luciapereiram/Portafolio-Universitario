from django.test import TestCase
from simulator.code_validator import validate_code

# -----------------------------------------
#           TESTS PARA validate_code
# -----------------------------------------

class CodeValidatorTests(TestCase):

    def setUp(self):
        self.blacklist = ["sys", "os", "subprocess", "eval", "exec"]

    def test_valid_code(self):
        code = "from qiskit import QuantumCircuit\nqc = QuantumCircuit(2)"
        valid, msg = validate_code(code, self.blacklist)
        self.assertTrue(valid)
        self.assertEqual(msg, "El código es seguro.")

    def test_valid_import(self):
        code = "import math\nprint(math.sqrt(16))"
        valid, msg = validate_code(code, self.blacklist)
        self.assertTrue(valid)
        self.assertEqual(msg, "El código es seguro.")

    def test_import_blacklisted_module(self):
        code = "import os\nqc = QuantumCircuit(2)"
        valid, msg = validate_code(code, self.blacklist)
        self.assertFalse(valid)

    def test_use_blacklisted_function(self):
        code = "eval('2+2')"
        valid, msg = validate_code(code, self.blacklist)
        self.assertFalse(valid)

    def test_use_blacklisted_attribute(self):
        code = "subprocess.Popen(['ls'])"
        valid, msg = validate_code(code, self.blacklist)
        self.assertFalse(valid)

    def test_use_blacklisted_partial(self):
        code = "from subprocess import Popen"
        valid, msg = validate_code(code, self.blacklist)
        self.assertFalse(valid)

    def test_use_blacklisted_combine(self):
        code = "import sys\nimport os\nos.system('rm -rf /')"
        valid, msg = validate_code(code, self.blacklist)
        self.assertFalse(valid)

    def test_use_blacklisted_complex(self):
        code = """
                def safe_function():
                    print("This is safe code.")
                safe_function()
            
            import sys
            from os import system as s
            import subprocess

            def run_command(cmd):
                s(cmd)

            eval("print('Malicious Code')")

            class Exploit:
                def __init__(self):
                    self.process = subprocess.Popen(['ls'], stdout=subprocess.PIPE)
                    exec("print('Still Malicious')")

            run_command('echo Exploit triggered')
        """

        valid, msg = validate_code(code, self.blacklist)
        self.assertFalse(valid)


    def test_syntax_error(self):
        code = "def f(:\n pass"
        valid, msg = validate_code(code, self.blacklist)
        self.assertFalse(valid)




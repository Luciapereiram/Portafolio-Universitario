import curses
import time
from enum import Enum

class CursesUi:
    """ Clase que proporciona una interfaz basada en `curses` para interactuar
    con la terminal de manera eficiente. """

    class TextStyle(Enum):
        NORMAL = curses.A_NORMAL
        BOLD = curses.A_BOLD
        UNDERLINE = curses.A_UNDERLINE
        REVERSE = curses.A_REVERSE

    def __init__(self, stdscr):
        self.stdscr = stdscr
        # Permite detectar teclas especiales (BACKSPACE por ejemplo)
        self.stdscr.keypad(True)
        curses.curs_set(0)        # Oculta el cursor para mejor apariencia

    def clear_screen(self):
        """ Limpia la pantalla y refresca. """

        self.stdscr.clear()
        self.stdscr.refresh()

    def clear_line(self, y):
        """ Limpia la línea en la posición 'y'. """

        self.stdscr.move(y, 0)
        self.stdscr.clrtoeol()  # Borra hasta el final de la línea
        self.stdscr.refresh()

    def show_message(self, message, y, format=TextStyle.NORMAL):
        """ Muestra un mensaje en la línea 'y'. """

        self.stdscr.addstr(y, 0, message, format.value)
        self.stdscr.refresh()

    def show_temporal_message(self, message, y, delay=2, format=TextStyle.NORMAL):
        """ Muestra un mensaje en la línea 'y' y lo borra después de 'delay' segundos. """

        self.stdscr.addstr(y, 0, message, format.value)
        self.stdscr.refresh()
        time.sleep(delay)
        self.clear_line(y)

    def get_message(self, y):
        """ Recoge la entrada del usuario en la línea 'y'. """
        
        curses.echo()
        return self.stdscr.getstr(y, 0).decode('utf-8')

    def pause_screen(self, ms=3000):
        """ Pausa la pantalla durante unos segundos determinados. """
        curses.napms(ms)

    def password_input(self, y):
        # Capturar la contraseña sin mostrarla en la pantalla
        password = ""

        curses.noecho()
    
        while True:
            key = self.stdscr.getch()

            if key == 10:  # Enter (contraseña completa)
                break

            elif key == 27:  # Escape (para salir)
                return False

            elif key == curses.KEY_BACKSPACE:  # Backspace (para borrar)
                # Limpiar la línea
                self.stdscr.addstr(y, 0, f"Contraseña: {' ' * len(password)}")
                self.stdscr.refresh()

                password = password[:-1]

                # Mostrar la contraseña en asteriscos
                self.stdscr.addstr(y, 0, f"Contraseña: {'*' * len(password)}")
                self.stdscr.refresh()

            else:
                password += chr(key)
                # Mostrar la contraseña en asteriscos
                self.stdscr.addstr(y, 0, f"Contraseña: {'*' * len(password)}")
                self.stdscr.refresh()

        return password

    def menu(self, options, y_start):
        """ Muestra un menu interactivo y devuelve la opción seleccionada. """

        selected = 0

        while True:
            self.stdscr.clear()
            self.stdscr.addstr(y_start, 0, "Menu Principal")
            for idx, option in enumerate(options):
                if idx == selected:
                    # Resaltar opción seleccionada
                    self.stdscr.addstr(idx + 2, 0, option, curses.A_REVERSE)
                else:
                    self.stdscr.addstr(idx + 2, 0, option)

            self.stdscr.refresh()

            key = self.stdscr.getch()  # Obtener tecla presionada

            if key == curses.KEY_DOWN:
                # Mover hacia abajo en el menu
                selected = (selected + 1) % len(options)

            elif key == curses.KEY_UP:
                # Mover hacia arriba en el menu
                selected = (selected - 1) % len(options)

            elif key == 10:  # Enter
                return selected
            
            elif key == 27: # Esc (para salir)
                return -1

package fonoteca;

import tiempo.Tiempo;
import valoraciones.*;

import excepciones.*;
import prettyPrint.*;

/**
 * Esta es la clase abstracta ElementoMusical 
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public abstract class ElementoMusical implements ITree, IRecomendable {
    private String titulo;
    private Tiempo duracion = new Tiempo(0, 0);

    /**
     * Constructor de ElementoMusical
     * 
     * @param titulo titulo del elemento
     * @param duracion duracion del elemento
     */
    public ElementoMusical(String titulo, Tiempo duracion) {
        this.titulo = titulo;
        this.duracion.sumarTiempo(duracion);
    }

    /**
     * @return el titulo del elemento
     */
    public String getTitulo() {
        return this.titulo;
    }

    /**
     * @return la duracion del elemento
     */
    public Tiempo getDuracion() {
        return this.duracion;
    }

    /**
     * @param duracion duracion a establecer
     */
    public void setDuracion(Tiempo duracion) {
		this.duracion = duracion;
	}

	/**
     * Metodo abstracto que comprueba si un elemento musical contiene otro. En caso de contenerlo, 
     * lanza una excepcion.
     * 
     * @param elemento elemento musical a comprobar
     * @param except booleano para señalizar que se quiere lanzar excepcion
     * 
     * @return false en caso de no contenerlo
     * 
     * @throws ExcepcionCancionRepetida excepcion de que una cancion se repite
     */
    public abstract boolean contieneMusica(ElementoMusical elemento, boolean except) throws  ExcepcionCancionRepetida;
    
    /**
     * Metodo para comprobar si un elemento musical contiene otro pero sin lanzar excepciones. 
     * 
     * @param elemento elemento musical a comprobar
     * 
     * @return true si lo contiene, false en caso contrario
     */
    public boolean contieneMusica(ElementoMusical elemento) {
		try {
			if (this.contieneMusica(elemento, true)) {
				return true;
			}
		} catch (ExcepcionCancionRepetida e) {
			return true;
		}
		
        return false;
    }
}

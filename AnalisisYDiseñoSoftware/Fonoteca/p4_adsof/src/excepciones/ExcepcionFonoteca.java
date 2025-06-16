package excepciones;

import fonoteca.ElementoMusical;

/**
 * Esta es la clase ExcepcionFonoteca, que hereda de Exception 
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class ExcepcionFonoteca extends Exception {
	private static final long serialVersionUID = 1L;
	private ElementoMusical elemento;
	
	/**
	 * Constructor de ExcepcionFonoteca 
	 * 
	 * @param elemento el elemento que genera la excepcion
	 */
	public ExcepcionFonoteca(ElementoMusical elemento) {
		this.elemento = elemento;
	}

	/**
	 * @return el elemento que genera la excepcion
	 */
	public ElementoMusical getElemento() {
		return elemento;
	}
}
package fonoteca;

import java.util.*;
import tiempo.Tiempo;
import excepciones.*;
import prettyPrint.*;

/**
 * Esta es la clase ListaMusica 
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class ListaMusica extends ElementoMusical {
	private List<ElementoMusical> elementos;

	/**
	 * Constructor de ListaMusica. Solo accesible desde el paquete fonoteca
	 * 
	 * @param titulo titulo de la lista
	 */
	protected ListaMusica(String titulo) {
		super(titulo, new Tiempo(0, 0));
		this.elementos = new ArrayList<ElementoMusical>();
	}

	/**
	 * @return los elementos musicales de la lista
	 */
	public List<ElementoMusical> getElementos() {
		return this.elementos;
	}

	/**
	 * Metodo para agregar un elemento musical a la lista
	 * 
	 * @param elem elemento musical a agregar
	 * 
	 * @return la lista con los cambios realizados (si los hubiera)
	 */
	protected ListaMusica addMusica(ElementoMusical elem) {
		if (elem == null) return this;
		
		this.elementos.add(elem);
		this.getDuracion().sumarTiempo(elem.getDuracion());
		return this;
	}

	/**
     * Metodo para comprobar si una lista contiene un elemento musical dado. En caso de contenerlo, lanza
     * la excepcion correspondiente.
     * 
     * @param elemento elemento musical a comprobar
     * @param except booleano para señalizar que se quiere lanzar excepcion
     * 
     * @return false en caso de no contenerlo
     * 
     * @throws ExcepcionCancionRepetida excepcion de que una cancion se repite
     */
	@Override
	public boolean contieneMusica(ElementoMusical elemento, boolean except) throws ExcepcionCancionRepetida {
		if (elemento == null) {
			return false;
		}

		if (this.getTitulo() == elemento.getTitulo() && this.getDuracion() == elemento.getDuracion()) {
			return true;
		}

		for (ElementoMusical elem : this.elementos) {
			try {
				if (elem.contieneMusica(elemento, except)) {
					return true;
				}
			} catch (ExcepcionCancionRepetida e) {
				throw e;
			}
		}

		return false;
	}

	/**
	 * Override de toString
	 */
	@Override
	public String toString() {
		return PrettyPrinter.print(this, "", 0);
	}

	/**
     * Metodo auxiliar para PrettyPrinter
     */
	@Override
	public String getNombre() {
		return "LISTA: " + this.getTitulo() + ", " + "DURACION: " + this.getDuracion() + "\n";
	}

	/**
	 * Metodo auxiliar para PrettyPrinter, obteniendo los hijos de la lista (albumes y canciones)
	 */
	@Override
	public List<ITree> getChildren() {
		return new ArrayList<ITree>(this.elementos);
	}

	/**
	 * Metodo de la interfaz IRecomendable
	 */
	@Override
	public String getDescripcion() {
		return this.getNombre();
	}
}

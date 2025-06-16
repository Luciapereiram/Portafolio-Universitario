package fonoteca;

import java.util.Collections;
import java.util.List;

import excepciones.ExcepcionCancionRepetida;
import tiempo.Tiempo;
import prettyPrint.*;

/**
 * Esta es la clase Cancion
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class Cancion extends ElementoMusical {

	/**
	 * Constructor de Cancion
	 * 
	 * @param titulo   titulo de la cancion
	 * @param minutos  minutos que dura
	 * @param segundos segundos que dura
	 */
	public Cancion(String titulo, int minutos, int segundos) {
		super(titulo, new Tiempo(minutos, segundos));
	}

	/**
	 * Metodo para comprobar si una cancion contiene un elemento musical dado. En
	 * caso de contenerlo, lanza la excepcion correspondiente. En este caso, se
	 * comprueba si una cancion es igual a si misma.
	 * 
	 * @param elemento elemento musical a comprobar
	 * @param except   booleano para señalizar que se quiere lanzar excepcion
	 * 
	 * @return false en caso de no contenerlo
	 * 
	 * @throws ExcepcionCancionRepetida excepcion de que una cancion se repite
	 */
	public boolean contieneMusica(ElementoMusical elemento, boolean except) throws ExcepcionCancionRepetida {
		if (elemento == null) {
			return false;
		}

		if (this.equals(elemento)) {
			throw new ExcepcionCancionRepetida(this);
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
		return this.getTitulo() + " (" + this.getDuracion() + ")";
	}

	/**
	 * Metodo auxiliar para PrettyPrinter, obteniendo los hijos de la cancion
	 * (conjunto vacio)
	 */
	@Override
	public List<ITree> getChildren() {
		return Collections.emptyList();
	}

	/**
	 * Metodo de la interfaz IRecomendable
	 */
	@Override
	public String getDescripcion() {
		return "CANCION: " + this.getTitulo();
	}

	/**
	 * Override del metodo equals
	 */
	@Override
	public boolean equals(Object object) {
		if (!(object instanceof Cancion))
			return false;

		if (this == object)
			return true;

		Cancion cancion = (Cancion) object;

		return ((super.getTitulo() == cancion.getTitulo()) && (this.hashCode() == object.hashCode())
				&& (super.getDuracion().mismoTiempo(cancion.getDuracion())));
	}

	/**
	 * Override del metodo hashCode
	 */
	@Override
	public int hashCode() {
		int hash = 2;
		hash = 3 * hash * super.getTitulo().hashCode();
		hash = 3 * hash * super.getDuracion().getMinutos();
		hash = 3 * hash * super.getDuracion().getSegundos();
		return hash;
	}

}

package fonoteca;

import java.util.*;

import excepciones.*;
import tiempo.Tiempo;
import prettyPrint.*;

/**
 * Esta es la clase Album
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class Album extends ElementoMusical {
	private String artista;
	private List<Cancion> canciones;
	private EstiloMusical estilo;

	/**
	 * Constructor de Album. Solo accesible desde el paquete fonoteca
	 * 
	 * @param titulo    titulo del album
	 * @param duracion  duracion del album
	 * @param artista   artista del album
	 * @param estilo    estilo musical
	 * @param canciones lista de canciones del album
	 */
	protected Album(String titulo, Tiempo duracion, String artista, EstiloMusical estilo, List<Cancion> canciones) {

		super(titulo, duracion);
		this.artista = artista;
		this.estilo = estilo;
		this.canciones = canciones;
	}

	/**
	 * Metodo para comprobar si un album contiene un elemento musical dado. En caso
	 * de contenerlo, lanza la excepcion correspondiente.
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
			return true;
		}

		for (Cancion c : this.canciones) {
			try {
				c.contieneMusica(elemento, except);
			} catch (ExcepcionCancionRepetida e) {
				throw e;
			}
		}

		return false;
	}

	/**
	 * @return el artista del album
	 */
	public String getArtista() {
		return artista;
	}

	/**
	 * @param artista el artista a establecer
	 */
	public void setArtista(String artista) {
		this.artista = artista;
	}

	/**
	 * @return la lista de canciones
	 */
	public List<Cancion> getCanciones() {
		return canciones;
	}

	/**
	 * @param canciones la lista de canciones a establecer
	 */
	public void setCanciones(List<Cancion> canciones) {
		this.canciones = canciones;
	}

	/**
	 * @return el estilo musical
	 */
	public EstiloMusical getEstilo() {
		return estilo;
	}

	/**
	 * @param estilo el estilo a establecer
	 */
	public void setEstilo(EstiloMusical estilo) {
		this.estilo = estilo;
	}

	/**
	 * Override de toString
	 */
	@Override
	public String toString() {
		return PrettyPrinter.print(this, "    ", 0);
	}

	/**
	 * Metodo auxiliar para PrettyPrinter
	 */
	@Override
	public String getNombre() {
		return "ALBUM: " + this.getTitulo() + ", " + "ARTISTA: " + this.artista + ", " + "DURACION: "
				+ this.getDuracion().getMinutos() + ":" + this.getDuracion().getSegundos() + ", " + "ESTILO: "
				+ this.estilo;
	}

	/**
	 * Metodo auxiliar para PrettyPrinter, obteniendo los hijos del album (las
	 * canciones)
	 */
	@Override
	public List<ITree> getChildren() {
		return new ArrayList<ITree>(this.canciones);
	}

	/**
	 * Metodo de la interfaz IRecomendable
	 */
	@Override
	public String getDescripcion() {
		return this.getNombre();
	}

	/**
	 * Override del metodo equals
	 */
	@Override
	public boolean equals(Object object) {
		if (!(object instanceof Album)) {
			return false;
		}

		if (this == object){
			return true;
		}

		Album album = (Album) object;

		for (Cancion c : this.canciones) {
			try {
				if (!album.contieneMusica(c, false)) {
					return false;
				}
			} catch (ExcepcionFonoteca e) {
				return false;
			}
		}

		return ((super.getTitulo() == album.getTitulo()) && (this.hashCode() == album.hashCode())
				&& (super.getDuracion().mismoTiempo(album.getDuracion())) && this.artista.equals(album.artista)
				&& this.estilo == album.estilo);
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
		hash = 3 * hash * this.artista.hashCode();
		hash = 3 * hash * this.estilo.hashCode();

		for (Cancion c : this.canciones) {
			hash = 3 * hash * c.hashCode();
		}

		return hash;
	}

}

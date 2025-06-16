package fonoteca;

import java.util.*;

import excepciones.*;
import tiempo.Tiempo;
import valoraciones.*;
import recomendaciones.*;

/**
 * Esta es la clase Fonoteca
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class Fonoteca {
	private Map<String, ElementoMusical> elementos;
	private Map<String, Usuario> usuarios;
	private IRecomendador recomendador;

	/**
	 * Constructor de Fonoteca
	 */
	public Fonoteca() {
		this.elementos = new LinkedHashMap<String, ElementoMusical>();
		this.recomendador = new RecomendadorPopularidad(0.5);
		this.usuarios = new HashMap<String, Usuario>();
	}

	/**
	 * Constructor de Fonoteca especificando el corte
	 * 
	 * @param corte corte de confianza
	 */
	public Fonoteca(double corte) {
		this.elementos = new LinkedHashMap<String, ElementoMusical>();
		this.recomendador = new RecomendadorPopularidad(corte);
		this.usuarios = new HashMap<String, Usuario>();
	}

	/**
	 * Constructor de Fonoteca especificando el recomendador
	 * 
	 * @param recomendador recomendador que se quiere establecer
	 */
	public Fonoteca(IRecomendador recomendador) {
		this.elementos = new LinkedHashMap<String, ElementoMusical>();
		this.recomendador = recomendador;
		this.usuarios = new HashMap<String, Usuario>();
	}

	/**
	 * @return los elementos musicales de la fonoteca
	 */
	public Map<String, ElementoMusical> getElementos() {
		return elementos;
	}

	/**
	 * @return los usuarios registrados en la fonoteca
	 */
	public Map<String, Usuario> getUsuarios() {
		return usuarios;
	}

	/**
	 * Metodo para crear un album de canciones sin estar repetidas entre si
	 * 
	 * @param titulo    titulo del album
	 * @param artista   artista del album
	 * @param estilo    el estilo musical
	 * @param canciones canciones a agregar
	 * 
	 * @return el nuevo album creado
	 * 
	 * @throws ExcepcionCancionRepetida excepcion si se quiere agregar una cancion
	 *                                  repetida
	 */
	public Album crearAlbum(String titulo, String artista, EstiloMusical estilo, Cancion... canciones)
			throws ExcepcionCancionRepetida {
		Tiempo duracionAlbum = new Tiempo(0, 0);
		List<Cancion> cancionesAlbum = new ArrayList<Cancion>();
		int i, j;

		if (titulo == null || artista == null || canciones == null || canciones.length == 0) {
			return null;
		}

		// Comprobar que en el propio album no se estan agregando canciones repetidas
		for (i = 0; i < canciones.length; i++) {
			for (j = i + 1; j < canciones.length; j++) {
				try {
					canciones[i].contieneMusica(canciones[j], true);
				} catch (ExcepcionCancionRepetida e) {
					throw e;
				}
			}

			duracionAlbum.sumarTiempo(canciones[i].getDuracion());
			cancionesAlbum.add(canciones[i]);
		}

		Album a = new Album(titulo, duracionAlbum, artista, estilo, cancionesAlbum);
		this.elementos.put(a.getTitulo(), a);

		return a;
	}

	/**
	 * Metodo para crear un album de canciones sin estar repetidas entre si pero sin
	 * estilo musical
	 * 
	 * @param titulo    titulo del album
	 * @param artista   artista del album
	 * @param canciones canciones a agregar
	 * 
	 * @return el nuevo album creado
	 * 
	 * @throws ExcepcionCancionRepetida excepcion si se quiere agregar una cancion
	 *                                  repetida
	 */
	public Album crearAlbum(String titulo, String artista, Cancion... canciones) throws ExcepcionCancionRepetida {
		return crearAlbum(titulo, artista, EstiloMusical.SINESTILO, canciones);
	}

	/**
	 * Metodo para crear una lista musical inicialmente vacia
	 * 
	 * @param titulo titulo de la lista
	 * 
	 * @return la nueva lista creada
	 */
	public ListaMusica crearListaMusica(String titulo) {
		ListaMusica l = new ListaMusica(titulo);
		this.elementos.put(l.getTitulo(), l);
		return l;
	}

	/**
	 * Metodo para agregar musica a una lista de la fonoteca. El elemento a agregar
	 * debe existir en la fonoteca, y no puede estar repetido en la propia lista.
	 * 
	 * @param lista lista donde agregar musica
	 * @param elem  elemento a agregar
	 * 
	 * @return la propia fonoteca con los cambios realizados (si hubiera)
	 * 
	 * @throws ExcepcionMusicaNoExistente excepcion de que el elemento no se
	 *                                    encuentra en la fonoteca
	 * @throws ExcepcionCancionRepetida   excepcion de que una cancion esta repetida
	 */
	public Fonoteca aniadirMusicaALista(ListaMusica lista, ElementoMusical elem)
			throws ExcepcionMusicaNoExistente, ExcepcionCancionRepetida {
		if (lista == null || elem == null || !this.elementos.containsValue(lista)) {
			return this;
		}

		boolean ret = false;

		// Si la fonoteca no contiene el elemento que se quiere agregar, entonces no se
		// agrega a la lista
		for (ElementoMusical e : this.elementos.values()) {
			if (e.contieneMusica(elem) == true) {
				ret = true;
			}
		}

		if (!ret) {
			throw new ExcepcionMusicaNoExistente(elem);
		}

		// Comprobar que no esta el elemento en la lista ya
		try {
			lista.contieneMusica(elem, true);
		} catch (ExcepcionCancionRepetida e) {
			throw e;
		}

		// Si esta en la fonoteca y no se repite en la lista, se agrega
		lista.addMusica(elem);
		return this;
	}

	/**
	 * Metodo para registrar usuarios que puedan valorar elementos musicales
	 * 
	 * @param nombre nombre del usuario
	 * @param nick   nickname unico del usuario
	 * 
	 * @return el nuevo usuario
	 */
	public Usuario registrarUsuario(String nombre, String nick) {
		if (nombre == null || nick == null || this.usuarios.keySet().contains(nick)) {
			return null;
		}

		Usuario usuarioNuevo = new Usuario(nombre, nick);
		this.usuarios.put(nick, usuarioNuevo);

		this.recomendador.addUsuario(usuarioNuevo);

		return usuarioNuevo;
	}

	/**
	 * Metodo privado para valorar un elemento musical, limitado a ser un album o
	 * una cancion.
	 * 
	 * @param u          el usuario que valora
	 * @param elem       el elemento a valorar
	 * @param valoracion la valoracion
	 * 
	 * @return la propia fonoteca con los cambios realizados (si hubiera)
	 */
	private Fonoteca valorarElemento(Usuario u, ElementoMusical elem, Valoracion valoracion) {
		if (u == null || !this.usuarios.containsValue(u) || elem == null || valoracion == null) {
			return this;
		}

		if (recomendador.haValorado(u, elem)) {
			return this;
		}

		boolean ret = false;

		// Se comprueba si existe el elemento en la fonoteca
		for (ElementoMusical e : this.elementos.values()) {
			if (e.contieneMusica(elem)) {
				ret = true;
				break;
			}
		}

		// Si existe se realiza la valoracion de dicho elemento, en caso contrario no se
		// puede valorar ya que no pertenece a la fonoteca
		if (ret) {
			this.recomendador.addUsuario(u);
			this.recomendador.addRecomendable(elem);
			this.recomendador.addValoracion(u, elem, valoracion);
		}

		return this;
	}

	/**
	 * Metodo publico para valorar un album, y por lo tanto sus canciones en caso de
	 * no estar valoradas ya
	 * 
	 * @param u          el usuario que valora
	 * @param elem       el elemento a valorar
	 * @param valoracion la valoracion
	 * 
	 * @return la propia fonoteca con los cambios realizados (si hubiera)
	 */
	public Fonoteca valorar(Usuario u, Album elem, Valoracion valoracion) {
		if (elem == null) {
			return this;
		}

		this.valorarElemento(u, elem, valoracion);

		for (Cancion c : elem.getCanciones()) {
			this.valorarElemento(u, c, valoracion);
		}

		return this;
	}

	/**
	 * Metodo publico para valorar una cancion
	 * 
	 * @param u          el usuario que valora
	 * @param elem       el elemento a valorar
	 * @param valoracion la valoracion
	 * 
	 * @return la propia fonoteca con los cambios realizados (si hubiera)
	 */
	public Fonoteca valorar(Usuario u, Cancion elem, Valoracion valoracion) {

		return this.valorarElemento(u, elem, valoracion);
	}

	/**
	 * Metodo para mostrar por pantalla los elementos de la fonoteca
	 */
	public void mostrar() {
		for (ElementoMusical elem : this.elementos.values()) {
			System.out.println(elem + "--------------");
		}
	}

	/**
	 * Metodo para mostrar las valoraciones de los usuarios de la fonoteca
	 * 
	 * @param usuario el usuario del que se quiere mostrar sus valoraciones
	 */
	public void mostrarValoraciones(Usuario usuario) {
		if (usuario == null) {
			throw new NullPointerException("usuario no puede ser null");
		}
		System.out.println("Valoracion de " + usuario.getNickname());

		for (IRecomendable elem : this.recomendador.elementosValorados(usuario)) {
			System.out.println(elem.getDescripcion() + " [" + this.recomendador.valoracion(usuario, elem) + "]");
		}
	}

	/**
	 * Metodo para mostrar recomendaciones a usuarios
	 * 
	 * @param usuario el usuario al que se quiere mostrar recomendaciones
	 */
	public void mostrarRecomendaciones(Usuario usuario) {
		Collection<Recomendacion> recomendaciones;
		if (usuario == null) {
			throw new NullPointerException("usuario no puede ser null");
		}

		System.out.println("RECOMENDACIONES PARA: " + usuario.getNickname());

		recomendaciones = recomendador.getRecomendaciones(usuario);

		for (Recomendacion r : recomendaciones) {
			System.out.println(r.getElemento().getDescripcion() + " [" + r.getConfianza() + "]");
		}
	}
}

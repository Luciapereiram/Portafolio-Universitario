package valoraciones;

import java.util.*;

/**
 * Esta es la clase AlmacenValoraciones
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class AlmacenValoraciones implements IAlmacenValoraciones {
	private Map<String, IUsuario> usuarios;
	private List<IRecomendable> elementos;
	private Map<IUsuario, Map<IRecomendable, Valoracion>> valoraciones;

	/**
	 * Constructor de AlmacenValoraciones
	 */
	public AlmacenValoraciones() {
		this.usuarios = new HashMap<String, IUsuario>();
		this.elementos = new ArrayList<IRecomendable>();
		this.valoraciones = new HashMap<IUsuario, Map<IRecomendable, Valoracion>>();
	}

	/**
	 * @return los usuarios que han realizado alguna valoracion
	 */
	public Map<String, IUsuario> getUsuarios() {
		return usuarios;
	}

	/**
	 * @return los elementos recomendables
	 */
	public List<IRecomendable> getElementos() {
		return elementos;
	}

	/**
	 * @return las valoraciones totales
	 */
	public Map<IUsuario, Map<IRecomendable, Valoracion>> getValoraciones() {
		return valoraciones;
	}

	/**
	 * Metodo de la interfaz IAlmacenValoraciones
	 * Agrega un usuario al almacen
	 */
	@Override
	public boolean addUsuario(IUsuario usuario) {
		if (usuario == null || this.usuarios.containsKey(usuario.getId())) {
			return false;
		}

		this.usuarios.put(usuario.getId(), usuario);
		return true;
	}

	/**
	 * Metodo de la interfaz IAlmacenValoraciones
	 * Agrega un elemento recomendable al almacen
	 */
	@Override
	public boolean addRecomendable(IRecomendable elemento) {
		if (elemento == null || this.elementos.contains(elemento)) {
			return false;
		}

		return this.elementos.add(elemento);
	}

	/**
	 * Metodo de la interfaz IAlmacenValoraciones
	 * Agrega una valoracion de un usuario a un elemento en el almacen
	 */
	@Override
	public void addValoracion(IUsuario usuario, IRecomendable elemento, Valoracion valoracion) {
		if (usuario == null || !this.usuarios.containsValue(usuario) || elemento == null ||
				!this.elementos.contains(elemento) || valoracion == null) {
			return;
		}

		if (this.valoraciones.containsKey(usuario)) {
			this.valoraciones.get(usuario).put(elemento, valoracion);
		} else {
			Map<IRecomendable, Valoracion> elementoValorado = new LinkedHashMap<IRecomendable, Valoracion>();
			elementoValorado.put(elemento, valoracion);
			this.valoraciones.put(usuario, elementoValorado);
		}
	}

	/**
	 * Metodo de la interfaz IAlmacenValoraciones
	 * Comprueba si un usuario ha valorado un elemento dado
	 */
	@Override
	public boolean haValorado(IUsuario usuario, IRecomendable elemento) {
		if (usuario == null || !this.usuarios.containsValue(usuario) ||
				elemento == null || !this.elementos.contains(elemento)) {
			return false;
		}
		if (this.elementosValorados(usuario) != null) {
			for (IRecomendable elem : this.elementosValorados(usuario)) {
				if (elem.equals(elemento))
					return true;
			}
		}

		return false;
	}

	/**
	 * Metodo de la interfaz IAlmacenValoraciones
	 * Devuelve el conjunto de elementos valorados por un determinado usuario
	 */
	@Override
	public Collection<IRecomendable> elementosValorados(IUsuario usuario) {
		if (usuario == null || !this.usuarios.containsValue(usuario) || !this.valoraciones.containsKey(usuario)) {
			return null;
		}

		return this.valoraciones.get(usuario).keySet();
	}

	/**
	 * Metodo de la interfaz IAlmacenValoraciones
	 * Devuelve la valoracion que un usuario ha dado a un elemento
	 */
	@Override
	public Valoracion valoracion(IUsuario usuario, IRecomendable elemento) {
		if (usuario == null || !this.usuarios.containsValue(usuario) ||
				elemento == null || !this.elementos.contains(elemento)) {
			return null;
		}

		if (this.haValorado(usuario, elemento)) {
			return this.valoraciones.get(usuario).get(elemento);
		}
		return null;
	}

}

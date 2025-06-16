package valoraciones;

import java.util.Collection;

/**
 * Esta es la interfaz IAlmacenValoraciones
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public interface IAlmacenValoraciones {
	/**
	 * @param usuario el usuario que se quiere agregar
	 * @return true si se agrega correctamente, false en caso contrario
	 */
	boolean addUsuario(IUsuario usuario);
	/**
	 * @param elemento el elemento que se quiere agregar
	 * @return true si se agrega correctamente, false en caso contrario
	 */
	boolean addRecomendable(IRecomendable elemento);
	/**
	 * @param usuario usuario que valora
	 * @param elemento elemento que se quiere valorar
	 * @param valoracion la valoracion
	 */
	void addValoracion(IUsuario usuario, IRecomendable elemento, Valoracion valoracion);
	/**
	 * @param usuario el usuario que se quiere comprobar si ha valorado
	 * @param elemento el elemento a comprobar 
	 * @return true si se agrega correctamente, false en caso contrario
	 */
	boolean haValorado(IUsuario usuario, IRecomendable elemento);
	/**
	 * @param usuario el usuario 
	 * @return conjunto de elementos valorados por dicho usuario
	 */
	Collection<IRecomendable> elementosValorados(IUsuario usuario);
	/**
	 * @param usuario el usuario
	 * @param elemento el elemento valorado
	 * @return la valoracion de dicho elemento por el usuario determinado
	 */
	Valoracion valoracion(IUsuario usuario, IRecomendable elemento);
}

package chatbots;

/**
 * Esta es la interfaz Builder
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 *
 * @param <E> tipo de objeto en el que se basa el builder
 */
public interface Builder<E> {
	/**
	 * @return devuelve el objeto creado
	 */
	public E build();
}

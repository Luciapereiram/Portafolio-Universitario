package prettyPrint;

import java.util.List;

/**
 * Esta es la interfaz ITree 
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public interface ITree {
	/**
	 * @return el nombre del arbol
	 */
	String getNombre();
	
	/**
	 * @return las hojas hijas del arbol
	 */
	List<ITree> getChildren();
}

package prettyPrint;

/**
 * Esta es la clase PrettyPrinter, para imprimir por pantalla de forma adecuada
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class PrettyPrinter {
	/** 
	 * Metodo estatico para imprimir
	 * 
	 * @param tree elemento que implementa la interfaz ITree
	 * @param indent el separador
	 * @param i el numero de elemento
	 * 
	 * @return una cadena de caracteres para imprimir
	 */
	public static String print(ITree tree, String indent, int i) {
		String returnValue = new String();
		
		if (i != 0) {
			returnValue += indent + i + ". " + tree;
		} else {
			returnValue += tree.getNombre() + "\n";
			i++;
			for (ITree t : tree.getChildren()) {
				returnValue += print(t, indent + "    ", i);
				i++;
			}
		}
		
		return returnValue;
	}
}

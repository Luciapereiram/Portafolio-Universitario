package excepciones;

import fonoteca.ElementoMusical;

/**
 * Esta es la clase ExcepcionCancionRepetida, que hereda de ExcepcionFonoteca
 * Es lanzada cuando una cancion esta repetida en un elemento musical 
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class ExcepcionCancionRepetida extends ExcepcionFonoteca {
	private static final long serialVersionUID = 1L;
	
    /**
     * Constructor de ExcepcionCancionRepetida
     * 
     * @param elemento la cancion repetida
     */
    public ExcepcionCancionRepetida(ElementoMusical elemento) {
        super(elemento);
    }

    /**
     * Override de toString
     */
    @Override
    public String toString() {
        return "music." + super.toString() + " La cancion " + this.getElemento().getTitulo() + " esta repetida";
    }
} 
package excepciones;

import fonoteca.ElementoMusical;

/**
 * Esta es la clase ExcepcionMusicaNoExistente, que hereda de ExcepcionFonoteca
 * Es lanzada cuando un elemento musical no existe en la fonoteca
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class ExcepcionMusicaNoExistente extends ExcepcionFonoteca {
    private static final long serialVersionUID = 1L;

    /**
     * Constructor de ExcepcionMusicaNoExistente
     * 
     * @param elemento elemento no existente
     */
    public ExcepcionMusicaNoExistente(ElementoMusical elemento) {
        super(elemento);
    }

    /**
     * Override de toString
     */
    @Override
    public String toString() {
        return "music." + super.toString() + " La cancion " + this.getElemento().getTitulo() + " no existe en la fonoteca";
    }
}
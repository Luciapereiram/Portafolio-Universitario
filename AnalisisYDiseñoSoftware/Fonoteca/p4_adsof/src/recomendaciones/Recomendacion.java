package recomendaciones;

import valoraciones.IRecomendable;

/**
 * Esta es la clase Recomendacion
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class Recomendacion implements Comparable<Recomendacion> {
    private IRecomendable elemento;
    private double confianza;

    /**
     * Constructor de Recomendacion
     * 
     * @param elemento elemento recomendable
     * @param confianza confianza para la recomendacion
     */
    public Recomendacion(IRecomendable elemento, double confianza) {
        this.elemento = elemento;
        this.confianza = confianza;
    }

    /**
     * @return la confianza de recomendacion
     */
    public double getConfianza() {
        return this.confianza;
    }

    /**
     * @return el elemento recomendado
     */
    public IRecomendable getElemento() {
        return this.elemento;
    }

    /**
     * Override de compareTo
     */
    @Override
    public int compareTo(Recomendacion arg0) {
        if (arg0 == null) {
            throw new NullPointerException("arg0 can't be null");
        }
        double cmp = this.confianza - arg0.confianza;
        if (cmp == 0) {
            if (!(this.elemento.getDescripcion().equals(arg0.getElemento().getDescripcion()))) {
                if (this.elemento.getDescripcion().split(" ")[0].equals("ALBUM:")) {
                    return -1;
                } else
                    return 1;
            }
        }
        return (int) cmp;
    }

}

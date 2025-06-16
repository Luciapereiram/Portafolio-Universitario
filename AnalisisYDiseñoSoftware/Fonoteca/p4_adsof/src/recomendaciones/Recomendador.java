package recomendaciones;

import valoraciones.AlmacenValoraciones;

/**
 * Esta es la clase Recomendador, que hereda de AlmacenValoraciones
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public abstract class Recomendador extends AlmacenValoraciones implements IRecomendador {
    private double corte;

    /**
     * Constructor de Recomendador
     * 
     * @param corte corte de confianza
     */
    public Recomendador(double corte) {
        super();
        this.corte = corte;
    }

    /**
     * Metodo de la interfaz IRecomendador
     * Establece el corte de confianza 
     */
    @Override
    public void setCorte(double corte) {
        this.corte = corte;
    }

    /**
     * @return el corte de confianza
     */
    public double getCorte() {
        return this.corte;
    }
}

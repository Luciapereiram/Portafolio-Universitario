package recomendaciones;

import java.util.Collection;

import valoraciones.IAlmacenValoraciones;
import valoraciones.IUsuario;

/**
 * Esta es la interfaz IRecomendador
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public interface IRecomendador extends IAlmacenValoraciones {
    /**
     * Metodo para recoger las recomendaciones de un usuario determinado
     * 
     * @param usuario el usuario del que se quiere las recomendaciones
     * 
     * @return conjunto de recomendaciones
     */
    Collection<Recomendacion> getRecomendaciones(IUsuario usuario);
    
    /**
     * Metodo para establecer corte de afinidad
     * 
     * @param corte el corte de afinidad
     */
    void setCorte(double corte);
}

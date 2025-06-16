package recomendaciones;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.*;

import valoraciones.IRecomendable;
import valoraciones.IUsuario;
import valoraciones.Valoracion;

/**
 * Esta es la clase RecomendadorPopularidad, que hereda de Recomendador
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class RecomendadorPopularidad extends Recomendador {

    /**
     * Constructor de RecomendadorPopularidad
     * 
     * @param corte corte de popularidad
     */
    public RecomendadorPopularidad(double corte) {
        super(corte);

    }

    /**
     * Metodo de la interfaz IRecomendador
     * Recoge las recomendaciones por popularidad de un usuario determinado
     */
    @Override
    public Collection<Recomendacion> getRecomendaciones(IUsuario usuario) {
        List<IRecomendable> elementos;
        List<Recomendacion> recomendados = new ArrayList<Recomendacion>();
        if (usuario == null) {
            throw new NullPointerException("El usuario no puede ser null");
        }

        elementos = super.getElementos();

        for (IRecomendable elem : elementos) {
            Recomendacion r = new Recomendacion(elem, this.calcularPopularidad(elem));
            if (r.getConfianza() >= super.getCorte() && !(super.haValorado(usuario, elem))) {
                recomendados.add(r);
            }
        }
        recomendados.sort(Comparator.naturalOrder());

        return recomendados;
    }

    /**
     * Metodo para calcular la popularidad de un elemento 
     * 
     * @param recomendable elemento recomendable
     * 
     * @return popularidad del elemento dado
     */
    private double calcularPopularidad(IRecomendable recomendable) {
        double popularidad = 0;
        Collection<Map<IRecomendable, Valoracion>> valoraciones;
        BigDecimal decimales;
        if (recomendable == null) {
            throw new NullPointerException("recomendable cant be null");
        }

        valoraciones = super.getValoraciones().values();

        for (Map<IRecomendable, Valoracion> valoracion : valoraciones) {
            Valoracion v = valoracion.get(recomendable);
            if (v == Valoracion.LIKE) {
                popularidad += 1;
            } else if (v == Valoracion.DISLIKE) {
                popularidad -= 0.5;
            }
        }

        decimales = BigDecimal.valueOf(popularidad / super.getValoraciones().size());
        decimales = decimales.setScale(2, RoundingMode.UP);
        popularidad = decimales.doubleValue();

        return popularidad;
    }

}

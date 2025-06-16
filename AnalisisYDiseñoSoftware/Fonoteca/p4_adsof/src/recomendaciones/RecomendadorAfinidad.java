package recomendaciones;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.*;

import valoraciones.IRecomendable;
import valoraciones.IUsuario;
import valoraciones.Valoracion;

/**
 * Esta es la clase RecomendadorAfinidad, que hereda de Recomendador
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class RecomendadorAfinidad extends Recomendador {

    /**
     * Constructor de RecomendadorAfinidad
     * 
     * @param corte corte de afinidad
     */
    public RecomendadorAfinidad(double corte) {
        super(corte);
    }

    /**
     * Metodo de la interfaz IRecomendador
     * Recoge las recomendaciones por afinidad de un usuario determinado
     */
    @Override
    public Collection<Recomendacion> getRecomendaciones(IUsuario usuario) {
        Collection<IUsuario> usuarios;
        double afinidad;
        double confianza;
        double numElementos;
        Map<IRecomendable, Double> posiblesRecomendaciones = new HashMap<IRecomendable, Double>();
        List<Recomendacion> recomendaciones = new ArrayList<Recomendacion>();
        if (usuario == null) {
            throw new NullPointerException("Usuario no puede ser null");
        }

        usuarios = super.getUsuarios().values();
        numElementos = super.getElementos().size();

        for (IUsuario u : usuarios) {
            Collection<IRecomendable> elementosValorados;
            if (u.getId().equals(usuario.getId()))
                continue;
            afinidad = this.calcularAfinidad(usuario, u); // calculamos afinidad

            elementosValorados = super.elementosValorados(u);

            // anyadimos los elementos valorados positivamente por los usuarios y su
            // confianza a un mapa
            // que contiene todas las potenciales recomendaciones. En caso de encontrar dos
            // veces el mismo
            // elemento, nos quedamos con el que tenga la mayor confianza, ademas,
            // comprobamos que el usuario no haya valorado este recomendable con
            // anterioridad
            for (IRecomendable e : elementosValorados) {
                if (super.valoracion(u, e) == Valoracion.LIKE) {
                    confianza = afinidad / numElementos;
                    if ((!posiblesRecomendaciones.containsKey(e)
                            || posiblesRecomendaciones.get(e) < confianza)) {
                        // redondeamos a dos decimales
                        BigDecimal decimales = BigDecimal.valueOf(confianza);
                        decimales = decimales.setScale(2, RoundingMode.UP);
                        confianza = decimales.doubleValue();
                        posiblesRecomendaciones.put(e, confianza);
                    }
                }
            }
        }

        // por cada una de las posibles recomendaciones, revisamos si pasa el corte
        // y se anyade a la coleccion de recomendaciones en caso de que asi sea
        for (IRecomendable r : posiblesRecomendaciones.keySet()) {
            confianza = posiblesRecomendaciones.get(r);
            if (confianza >= super.getCorte() && !super.haValorado(usuario, r)) {
                recomendaciones.add(new Recomendacion(r, confianza));
            }
        }

        recomendaciones.sort(Comparator.naturalOrder());

        return recomendaciones;
    }

    /**
     * Metodo para calcular la afinidad 
     * 
     * @param usuario1 primer usuario 
     * @param usuario2 segundo usuario
     * 
     * @return afinidad entre usuarios
     */
    private double calcularAfinidad(IUsuario usuario1, IUsuario usuario2) {
        Collection<IRecomendable> elementosValoradosU1;

        double afinidad = 0;

        if (usuario1 == null || usuario2 == null) {
            throw new NullPointerException("Los usuarios pasados como argumentos no pueden ser null");
        }

        elementosValoradosU1 = super.elementosValorados(usuario1);

        for (IRecomendable recomendable : elementosValoradosU1) {
            Valoracion v;
            if (super.haValorado(usuario2, recomendable) && super.haValorado(usuario1, recomendable)) {
                v = super.valoracion(usuario2, recomendable);
                if (v == super.valoracion(usuario1, recomendable)) {
                    if (v == Valoracion.LIKE) {
                        afinidad++;
                    } else
                        afinidad += 0.5;
                } else
                    afinidad -= 0.5;
            }
        }
        
        return afinidad;
    }
}

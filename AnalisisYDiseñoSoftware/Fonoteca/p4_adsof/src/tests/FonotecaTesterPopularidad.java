package tests;

import excepciones.ExcepcionCancionRepetida;
import fonoteca.Album;
import fonoteca.Fonoteca;
import fonoteca.Usuario;
import valoraciones.Valoracion;

/**
 * Esta es la clase test FonotecaTesterPopularidad
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class FonotecaTesterPopularidad extends FonotecaTesterErrores {
    private Album album2;

    /**
	 * Aplicacion para comprobar el funcionamiento de la clase RecomendadorPopularidad. Imprime por
	 * pantalla el resultado de la fonoteca tras generar recomendaciones por popularidad.
	 * 
	 * @param args argumentos de entrada
	 */
    public static void main(String[] args) {
        FonotecaTesterPopularidad main = new FonotecaTesterPopularidad();
        Fonoteca fonoteca = new Fonoteca(0.4); // corte 0.4 para el recomendador
        main.crearMusica(fonoteca);
        main.recomendaciones(fonoteca);
    }

    /**
     * Metodo para crear el album 2 y agregarlo a la fonoteca
     */
    public void crearMusica(Fonoteca fonoteca) {
        super.crearMusica(fonoteca);
        try {
            this.album2 = fonoteca.crearAlbum("Resistire", "Duo dinamico", canciones[3], canciones[4]);
        } catch (ExcepcionCancionRepetida e) {
            e.printStackTrace();
        }
    }

    /**
     * Metodo para generar las recomendaciones de elementos musicales
     * 
     * @param fonoteca la fonoteca
     */
    protected void recomendaciones(Fonoteca fonoteca) {
        Usuario[] usuarios = { fonoteca.registrarUsuario("Sonia Melero Vegas", "smelero"),
                fonoteca.registrarUsuario("Miguel Cuevas Alonso", "mcuevas"),
                fonoteca.registrarUsuario("Lucas Varas Peinado", "lvaras") };
        
        fonoteca.valorar(usuarios[0], album1, Valoracion.LIKE)
                .valorar(usuarios[0], canciones[3], Valoracion.LIKE)
                .valorar(usuarios[1], canciones[0], Valoracion.LIKE)
                .valorar(usuarios[1], canciones[1], Valoracion.LIKE)
                .valorar(usuarios[1], album2, Valoracion.LIKE)
                .valorar(usuarios[2], canciones[2], Valoracion.LIKE)
                .valorar(usuarios[2], canciones[3], Valoracion.LIKE)
                .valorar(usuarios[2], canciones[1], Valoracion.DISLIKE);
        
        for (Usuario u : usuarios) {
            System.out.println("---------------------------");
            fonoteca.mostrarRecomendaciones(u);
        }
    }
}

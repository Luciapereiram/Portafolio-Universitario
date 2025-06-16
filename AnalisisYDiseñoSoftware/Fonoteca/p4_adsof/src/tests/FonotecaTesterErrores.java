package tests;

import fonoteca.*;
import excepciones.*;

/**
 * Esta es la clase test FonotecaTesterErrores
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class FonotecaTesterErrores {
    protected Album album1; // protected porque extenderemos esta clase en los próximos apartados
    protected Cancion[] canciones = { new Cancion("Radio ga ga", 5, 48),
            new Cancion("Tear it up", 3, 28),
            new Cancion("It's a hard life", 4, 8),
            new Cancion("Resistire", 4, 4),
            new Cancion("Dos corazones", 3, 6) };

    /**
     * Aplicacion para comprobar el funcionamiento de la clase Fonoteca
     * Imprime por pantalla el resultado de la fonoteca tras agregar elementos
     * 
     * @param args argumentos de entrada
     */
    public static void main(String[] args) {
        FonotecaTesterErrores main = new FonotecaTesterErrores();
        Fonoteca fonoteca = new Fonoteca();
        main.crearMusica(fonoteca);
        fonoteca.mostrar();
    }

    /**
     * Metodo para rellenar una fonoteca con elementos musicales 
     * 
     * @param fonoteca la fonoteca en la cual se agrgean los elementos
     */ 
    public void crearMusica(Fonoteca fonoteca) {
        try {
            this.album1 = fonoteca.crearAlbum("The Works", "Queen", EstiloMusical.ROCK,
                    canciones[0], canciones[1], canciones[2]);
            fonoteca.crearAlbum("Resistire", "Duo dinamico",
                    canciones[3], new Cancion("Resistire", 4, 4)); // cancion repetida
        } catch (ExcepcionCancionRepetida cr) {
            System.err.println(cr);
        }
        ListaMusica favoritas = fonoteca.crearListaMusica("Mis favoritas");
        try {
            fonoteca.aniadirMusicaALista(favoritas, album1)
                    .aniadirMusicaALista(favoritas, canciones[1]);
        } catch (ExcepcionFonoteca e) {
            System.err.println(e);
        }
    }
}

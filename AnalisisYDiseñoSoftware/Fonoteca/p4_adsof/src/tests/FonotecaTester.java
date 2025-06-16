package tests;

import excepciones.*;
import fonoteca.*;

/**
 * Esta es la clase test FonotecaTester
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class FonotecaTester {
	
    /**
     * Aplicacion para comprobar el funcionamiento de la clase Fonoteca
     * Imprime por pantalla el resultado de la fonoteca tras agregar elementos
     * 
     * @param args argumentos de entrada
     * 
	 * @throws ExcepcionMusicaNoExistente escepcion de que un elemento no existe en la fonoteca
	 * @throws ExcepcionCancionRepetida excepcion de que una cancion esta repetida
     */
    public static void main(String[] args) throws ExcepcionCancionRepetida, ExcepcionMusicaNoExistente {
        FonotecaTester main = new FonotecaTester();
        Fonoteca fonoteca = main.crearMusica();
        fonoteca.mostrar();
    }

    
    /**
     * Metodo para rellenar una fonoteca con elementos musicales 
     * 
     * @return la fonoteca con los cambios realizados
     * 
     * @throws ExcepcionMusicaNoExistente escepcion de que un elemento no existe en la fonoteca
	 * @throws ExcepcionCancionRepetida excepcion de que una cancion esta repetida
     */
    public Fonoteca crearMusica() throws ExcepcionCancionRepetida, ExcepcionMusicaNoExistente {
        Cancion[] canciones = {
                new Cancion("Radio ga ga", 5, 48), // Canción Radio ga ga, con duración 5:48
                new Cancion("Tear it up", 3, 28),
                new Cancion("It's a hard life", 4, 8),
                new Cancion("Resistire", 4, 4),
                new Cancion("Dos corazones", 3, 6) };
        Fonoteca fonoteca = new Fonoteca();
        Album album1 = fonoteca.crearAlbum("The Works", "Queen", EstiloMusical.ROCK,
                canciones[0], canciones[1], canciones[2]);
        fonoteca.crearAlbum("Resistire", "Duo dinamico", canciones[3], canciones[4]); // sin estilo musical
        ListaMusica favoritas = fonoteca.crearListaMusica("Mis favoritas");
        fonoteca.aniadirMusicaALista(favoritas, album1)
                .aniadirMusicaALista(favoritas, canciones[3])
                .aniadirMusicaALista(favoritas, canciones[4]);
        System.out.println(fonoteca.crearAlbum("Las 4 estaciones", "Vivaldi", EstiloMusical.CLASICA));
        return fonoteca;
    }
}
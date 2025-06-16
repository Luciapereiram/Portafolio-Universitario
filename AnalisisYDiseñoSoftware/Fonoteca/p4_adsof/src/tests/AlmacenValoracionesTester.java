package tests;

import valoraciones.*;
import excepciones.ExcepcionCancionRepetida;
import fonoteca.*;

/**
 * Esta es la clase test AlmacenValoracionesTester 
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class AlmacenValoracionesTester {
	private static Fonoteca f = new Fonoteca();
	
	/**
	 * Aplicacion que comprueba el funcionamiento de la clase AlmacenValoraciones
	 * 
	 * @param args argumentos de entrada
	 * 
	 * @throws ExcepcionCancionRepetida escepcion de que la cancion esta repetida
	 */
	public static void main(String[] args) throws ExcepcionCancionRepetida {
	    boolean ret = true;
		
		// Creamos algunos usuarios
		IUsuario usuario1 = new Usuario("usuario1", "u1");
		IUsuario usuario2 = new Usuario("usuario2", "u2");
		IUsuario usuario3 = new Usuario("usuario3", "u3");

	    // Creamos algunas canciones
		Cancion cancion1 = new Cancion("cancion1", 2, 10);
		Cancion cancion2 = new Cancion("cancion2", 2, 40);
		Cancion cancion3 = new Cancion("cancion3", 1, 30);
		Cancion cancion4 = new Cancion("cancion4", 3, 10);

		// Creamos algunos álbumes
		Album album1 = f.crearAlbum("album1", "artista1", EstiloMusical.CLASICA, cancion1, cancion2);
		Album album2 = f.crearAlbum("album1", "artista1", EstiloMusical.JAZZ, cancion3, cancion4);
	        
		// Creamos el almacen de valoraciones
		IAlmacenValoraciones almacen = new AlmacenValoraciones();
		
		// Agregamos los usuarios y los elementos al almacen
		almacen.addUsuario(usuario1);
		almacen.addUsuario(usuario2);
		almacen.addUsuario(usuario3);

		almacen.addRecomendable(cancion1);
		almacen.addRecomendable(cancion2);
		almacen.addRecomendable(cancion3);
		almacen.addRecomendable(cancion4);
		almacen.addRecomendable(album1);
		almacen.addRecomendable(album2);

		// Usuario 1 valora la cancion 1 y el album 1
		almacen.addValoracion(usuario1, cancion1, Valoracion.LIKE);
		almacen.addValoracion(usuario1, album1, Valoracion.DISLIKE);

		// Usuario 2 valora el album 1 (todas las canciones de album1 deberian ser valoradas)
		almacen.addValoracion(usuario2, album1, Valoracion.LIKE);

		// Usuario 3 valora la cancion 3 y el album 2 (la cancion 4 deberia ser valorada)
		almacen.addValoracion(usuario3, cancion3, Valoracion.LIKE);
		almacen.addValoracion(usuario3, album2, Valoracion.DISLIKE);

		// Comprobamos las valoraciones de los usuarios
		if (almacen.valoracion(usuario1, cancion1) != Valoracion.LIKE) {
			ret = false;
			System.out.println("Error en la valoracion de usuario1 para cancion1");
	    }

		if (almacen.valoracion(usuario1, album1) != Valoracion.DISLIKE) {
			ret = false;
			System.out.println("Error en la valoracion de usuario1 para album1");
		}

		if (almacen.valoracion(usuario2, album1) != Valoracion.LIKE) {
			ret = false;
			System.out.println("Error en la valoracion de usuario2 para cancion1");
		}
		
		if (ret) System.out.println("Test AlmacenValoraciones correcto");
		else System.out.println("Test AlmacenValoraciones erroneo");
	}
}

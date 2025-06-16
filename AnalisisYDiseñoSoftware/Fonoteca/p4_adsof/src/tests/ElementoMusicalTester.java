package tests;

import excepciones.ExcepcionCancionRepetida;
import excepciones.ExcepcionMusicaNoExistente;

import fonoteca.*;
import tiempo.*;

/**
 * Esta es la clase test ElementoMusicalTester
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class ElementoMusicalTester {
	private static Fonoteca f = new Fonoteca();
	
	/**
	 * Aplicacion para comprobar el funcionamiento de las distintas clases que
	 * heredan de ElementoMusical
	 * 
	 * @param args argumentos de entrada
	 * @throws ExcepcionMusicaNoExistente escepcion de que un elemento no existe en la fonoteca
	 * @throws ExcepcionCancionRepetida excepcion de que una cancion esta repetida
	 */
	public static void main(String[] args) throws ExcepcionMusicaNoExistente, ExcepcionCancionRepetida {
		CancionTest();
		AlbumTest();
		ListaTest();
		
	    System.out.println("\nTests pasados correctamente");
	}
	
	/**
	 * Metodo para probar la clase Cancion
	 */
	private static void CancionTest() {
		System.out.println("---- Test ElementoMusical CANCION ----");
		
		Cancion c = new Cancion("c1", 2, 30);
	    Cancion cRepetida = new Cancion("c1", 2, 30);
	    
	    if (c.contieneMusica(cRepetida)) System.out.println("--> Test correcto");
	    else System.out.println("--> Test erroneo");
	}
	
	/**
	 * Metodo para probar la clase Album
	 */
	private static void AlbumTest() throws ExcepcionCancionRepetida {
		System.out.println("\n---- Test ElementoMusical ALBUM ----");
	    
		// Creamos algunas canciones
	    Cancion c1 = new Cancion("c1", 2, 30);
	    Cancion c2 = new Cancion("c2", 3, 10);
	    Cancion c3 = new Cancion("c3", 3, 0);
	    Cancion c4 = new Cancion("c4", 2, 40);
	    
	    // Creamos una lista principal de elementos musicales
	    Album a = f.crearAlbum("Album1", "Paco", c1, c2, c3, c4);
	    
	    
	    // Comprobar que no tiene estilo musical
	    if (!a.getEstilo().equals(EstiloMusical.SINESTILO)) System.out.println("Error. El album si tiene estilo musical");
	    
	    // Comprobar que lanza excepcion si la cancion esta repetida
	    Cancion c5 = new Cancion("c5", 2, 10);
	    try {
	    	f.crearAlbum("Album con fallo", "Paco", c5, c5);
	    } catch (ExcepcionCancionRepetida e) {
	    	System.out.println("Se lanza excepcion");
	    	System.out.println("--> Test correcto");
	    	return;
	    }
	    
	    System.out.println("--> Test erroneo");
	}
	
	/**
	 * Metodo para probar la clase ListaMusica
	 */
	private static void ListaTest() throws ExcepcionCancionRepetida, ExcepcionMusicaNoExistente {
		boolean ret = true;
		
		System.out.println("\n---- Test ElementoMusical LISTA ----");
		
	    // Creamos una lista principal de elementos musicales
	    ListaMusica l1 = f.crearListaMusica("Lista1");

	    // Creamos algunos elementos musicales y los agregamos a la lista principal
	    Cancion c1 = new Cancion("c1", 2, 30);
	    Cancion c2 = new Cancion("c2", 3, 10);
	    Cancion c3 = new Cancion("c3", 3, 0);
	    Cancion c4 = new Cancion("c4", 2, 40);
	    
	    // Agregamos elementos a la fonoteca creando un album
	    f.crearAlbum("album1", "Paco", c1, c2, c3 ,c4);
	    
	    ListaMusica l2 = f.crearListaMusica("Lista2");
	    f.aniadirMusicaALista(l2, c1).aniadirMusicaALista(l2, c2);
	    
	    ListaMusica l3 = f.crearListaMusica("Lista3");
	    f.aniadirMusicaALista(l3, c3).aniadirMusicaALista(l3, c4);
	    
	    // Agregamos las listas a la lista principal
	    f.aniadirMusicaALista(l1, l2).aniadirMusicaALista(l1, l3);

	    // Comprobamos que la duracion de la lista es correcta (debe ser 11:20)
	    assert l1.getDuracion().equals(new Tiempo(11, 20));

	    // Comprobamos que la lista contiene los elementos musicales añadidos
	    if (!l1.contieneMusica(c1)) {
	    	ret = false;
	    	System.out.println("Error. La cancion " + c1.getTitulo()+ " si deberia estar en la lista\n");
	    }
	    
	    if(!l1.contieneMusica(c2)) {
	    	ret = false;
	    	System.out.println("Error. La cancion " + c2.getTitulo()+ "  si deberia estar en la lista\n");
	    }
	    
	    if(!l1.contieneMusica(c3)) {
	    	ret = false;
	    	System.out.println("Error. La cancion " + c3.getTitulo()+ "  si deberia estar en la lista\n");
	    }
	    
	    if(!l1.contieneMusica(c4)) {
	    	ret = false;
	    	System.out.println("Error. La cancion " + c4.getTitulo()+ "  si deberia estar en la lista\n");
	    }
	    
	    if(!l1.contieneMusica(l2)) {
	    	ret = false;
	    	System.out.println("Error. La cancion " + l2.getTitulo()+ "  si deberia estar en la lista\n");
	    }
	    
	    if(!l1.contieneMusica(l3)) {
	    	ret = false;
	    	System.out.println("Error. La cancion " + l3.getTitulo()+ "  si deberia estar en la lista\n");
	    }

	    // Comprobamos que la lista no contiene un elemento musical que no ha sido agregado
	    Cancion c5 = new Cancion("c5", 1, 25);
	    l1.contieneMusica(c5);

	    // Comprobamos que la lista lanza excepcion cuando el elemento es repetido
	    try {
	    	l1.contieneMusica(c1, true);
	    } catch (ExcepcionCancionRepetida e) {
	    	System.out.println("Se lanza excepcion");
	    }
	    
	    if (ret) System.out.println("--> Test correcto");
	    else System.out.println("--> Test con fallos");
	}
}



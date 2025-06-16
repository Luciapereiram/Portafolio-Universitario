package tests;

import fonoteca.*;
import valoraciones.*;

/**
 * Esta es la clase test FonotecaTesterValoraciones
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class FonotecaTesterValoraciones extends FonotecaTesterErrores {
	/**
	 * Aplicacion para comprobar el funcionamiento de la clase Fonoteca junto con la implementacion
	 * de un almacen. Imprime por pantalla el resultado de la fonoteca tras las valoraciones.
     *  
	 * @param args argumentos de entrada
	 */
	public static void main(String[] args) {
		FonotecaTesterValoraciones main = new FonotecaTesterValoraciones();
		Fonoteca fonoteca = new Fonoteca();
		main.crearMusica(fonoteca);
		main.valoraciones(fonoteca);
	}

	/**
	 * Metodo para valorar elementos por usuarios de la fonoteca
	 * 
	 * @param fonoteca la fonoteca de la cual se realizan las valoraciones
	 */
	public void valoraciones(Fonoteca fonoteca) {
		Usuario usuario1 = fonoteca.registrarUsuario("Sonia Melero Vegas", "smelero"),
				usuario2 = fonoteca.registrarUsuario("Miguel Cuevas Alonso", "mcuevas");
		fonoteca.valorar(usuario1, this.canciones[0], Valoracion.DISLIKE)
				.valorar(usuario1, this.album1, Valoracion.LIKE)
				.valorar(usuario1, this.canciones[3], Valoracion.DISLIKE) // no se valora, porque no esta en la fonoteca
				.valorar(usuario2, this.canciones[1], Valoracion.DISLIKE);
		fonoteca.mostrarValoraciones(usuario1);
		fonoteca.mostrarValoraciones(usuario2);
	}
}

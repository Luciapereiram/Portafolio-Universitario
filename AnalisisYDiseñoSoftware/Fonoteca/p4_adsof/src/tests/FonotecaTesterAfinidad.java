package tests;

import fonoteca.Fonoteca;
import recomendaciones.RecomendadorAfinidad;

/**
 * Esta es la clase test FonotecaTesterAfinidad
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class FonotecaTesterAfinidad extends FonotecaTesterPopularidad {

	/**
	 * Aplicacion para comprobar el funcionamiento de la clase RecomendadorAfinidad. Imprime por
	 * pantalla el resultado de la fonoteca tras generar recomendaciones por afinidad.
	 * 
	 * @param args argumentos de entrada
	 */
	public static void main(String[] args) {
		FonotecaTesterAfinidad main = new FonotecaTesterAfinidad();
		Fonoteca fonoteca = new Fonoteca(new RecomendadorAfinidad(0.2)); // Con rec. afinidad de corte 0.2
		main.crearMusica(fonoteca);
		main.recomendaciones(fonoteca);
	}
}

package intents;

import java.util.List;

/**
 * Clase de utilidad para la definición de Intents
 * 
 * @author profesores ADSOF
 */
public class IntentHelper { 

	/**
	 * Metodo estatico para comprobar si una frase dada contiene unos valores
	 * 
	 * @param s frase
	 * @param values valores
	 * 
	 * @return true si lo contiene, false en caso contrario
	 */
	public static boolean containsIgnoreCase(String s, Object[] values) {
		return List.of(values).stream().anyMatch(e -> s.toUpperCase().equals(e.toString()));
	}

}

package intents;

import java.util.*;
import java.util.function.Predicate;
import java.util.function.Function;

/**
 * Esta es la clase genérica de ContextIntent, que hereda de Intent Se trata de
 * un intent que contiene parametros
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 *
 * @param <E> tipo de objeto en el que se basa el intent
 */
public class ContextIntent<E> extends Intent {
	private Map<String, Predicate<String>> match_funcs;
	private Map<String, Function<String, Object>> param_funcs;
	private Function<ContextIntent<E>, E> obtainObject;
	private StructuredPhrase phraseMatch;
	private String phraseIntroduced;

	/**
	 * Constructor de ContextIntent
	 * 
	 * @param name    nombre del intent
	 * @param phrases conjunto de frases que guarda el intent
	 */
	public ContextIntent(String name, List<StructuredPhrase> phrases) {
		super(name, phrases);
		this.match_funcs = new HashMap<String, Predicate<String>>();
		this.param_funcs = new HashMap<String, Function<String, Object>>();
	}

	/**
	 * Metodo para conectar nombre de parametros con sus funciones
	 * correspondientes para obtenerlo
	 * 
	 * @param text  nombre del parametro
	 * @param match funcion de match, para localizarlo en una frase
	 * @param param funcion para obtener dicho parametro
	 * 
	 * @return el propio ContextIntent
	 */
	public ContextIntent<E> withParameter(String text, Predicate<String> match, Function<String, Object> param) {
		if (match == null || text == null || param == null)
			return null;

		// Guardar los procedimientos necesarios para hacer el match y procesar un tipo
		// de parametro
		this.match_funcs.put(text, match);
		this.param_funcs.put(text, param);

		return this;
	}

	/**
	 * Metodo para enlazar el constructor del objeto con el intent
	 * 
	 * @param obj funcion correspondiente al constructor del objeto
	 * 
	 * @return el propio ContextIntent
	 */
	public ContextIntent<E> resultObject(Function<ContextIntent<E>, E> obj) {
		if (obj == null)
			return null;

		this.obtainObject = obj;

		return this;
	}

	/**
	 * Metodo para establecer la respuesta a las frases del intent
	 */
	public ContextIntent<E> replies(String text) {
		super.replies(text);
		return this;
	}

	/**
	 * Metodo privado para obtener la frase del intent con la que una frase
	 * introducida por el usuario coincide
	 * 
	 * @param text frase a comprobar
	 * 
	 * @return la frase con la que coincide
	 */
	private StructuredPhrase containsPhrase(String text) {
		String[] textAux = text.split(" ");
		List<String> phrase;
		String parameter = "";
		boolean match = true;

		for (StructuredPhrase stPhrase : this.getPhrases()) {
			phrase = stPhrase.getPhrase();

			if (textAux.length != phrase.toArray().length) {
				match = false;
				continue;
			}

			for (int i = 0; i < textAux.length; i++) {
				match = true;

				// Si el string de phrase es un parametro, se sigue avanzando para ver si la
				// estructura de la frase coincide
				if (phrase.get(i).startsWith("[") && phrase.get(i).endsWith("]")) {
					parameter = phrase.get(i).replace("[", "").replace("]", "");
					if (!this.match_funcs.containsKey(parameter) || !this.match_funcs.get(parameter).test(textAux[i])) {
						match = false;
						break;
					}
				} else {
					// Si no es un parametro, se comprueba que coincide con el string
					// siguiente de textAux
					if (!phrase.get(i).equalsIgnoreCase(textAux[i])) {
						match = false;
						break;
					}
				}
			}

			// Si no se ha puesto a false, significa que existe una StructuredPhrase que
			// coincide con el texto que nos han pasado, por tantp devolvemos la frase dada
			// convertida a StructuredPhrase
			if (match) {
				return stPhrase;
			} else
				match = true;
		}

		// En caso de no existir, se devuelve null
		return null;
	}

	/**
	 * Override de matches (metodo de la clase Intent)
	 */
	@Override
	public boolean matches(String text) {
		if (text == null)
			return false;

		String[] textAux = text.split(" ");
		List<String> matching;
		boolean match = true;

		for (StructuredPhrase sp : this.getPhrases()) {
			matching = sp.getPhrase();

			if (matching.toArray().length != textAux.length) {
				continue;
			}

			for (int i = 0; i < matching.size(); i++) {
				// Si es un parametro, se matchea con su funcion correspondiente
				if (matching.get(i).startsWith("[") && matching.get(i).endsWith("]")) {
					String parameter = matching.get(i).replace("[", "").replace("]", "");
					if (!this.match_funcs.containsKey(parameter) || !this.match_funcs.get(parameter).test(textAux[i])) {
						match = false;
						break;
					}
				} else {

					// Si es una palabra, se comprueba que sea igual
					if (!matching.get(i).equalsIgnoreCase(textAux[i])) {
						match = false;
						break;
					}
				}
			}

			// Si matchea sigue en valor a true, entonces se ha encontrado una frase que
			// concuerda
			if (match)
				return true;

			// Sino, hay que seguir mirando las demas
			match = true;
		}

		return false;
	}

	/**
	 * Override de process (metodo de la clase Intent)
	 */
	@Override
	public Intent process(String text) {
		if (text == null)
			return this;

		String parameter = "";
		String[] reply = this.getReplyAttribute();
		String[] newReply = reply.clone();
		StructuredPhrase phraseOfText = this.containsPhrase(text);
		boolean noMatch = true;

		// Si no existe la frase en el Intent, se devuelve null
		if (phraseOfText == null) {
			return this;
		} else {
			// Si existe, se añade la frase con la que coincide
			this.phraseMatch = phraseOfText;
			this.phraseIntroduced = text;
		}

		// Si reply contiene parametros, son sustituidos por los
		// valores correspondientes
		for (int i = 0; i < reply.length; i++) {

			if (reply[i].startsWith("#") && reply[i].endsWith("#")) {
				parameter = reply[i].replaceAll("#", "");

				// Se comprueba si en la frase del usuario hay algun parametro que matchee
				// para asi tomar su valor.
				for (String s : this.phraseIntroduced.split(" ")) {
					if (this.match_funcs.get(parameter).test(s)) {
						newReply[i] = this.param_funcs.get(parameter).apply(s).toString();
						noMatch = false;
					}
				}
				if (noMatch) {
					// En caso contrario, se toma el valor del parametro por defecto
					// de la frase con la que coincide en el ContextIntent.
					newReply[i] = phraseOfText.getValue(parameter);
				}
			}
		}

		this.setLastReply(newReply);

		return this;
	}

	/**
	 * Override de getObject (metodo de la clase Intent)
	 */
	@Override
	public E getObject() {
		return this.obtainObject.apply(this);
	}

	/**
	 * Metodo para obtener un determinado parametro
	 * 
	 * @param <P>  parametrizacion
	 * @param text nombre del parametro
	 * 
	 * @return el parametro
	 */
	public <P extends Object> P getParam(String text) {
		if (text == null)
			return null;

		for (String s : this.phraseIntroduced.split(" ")) {
			if (this.match_funcs.get(text).test(s)) {
				return (P) this.param_funcs.get(text).apply(s);
			}
		}

		return (P) this.phraseMatch.getRealValue(text);
	}
}

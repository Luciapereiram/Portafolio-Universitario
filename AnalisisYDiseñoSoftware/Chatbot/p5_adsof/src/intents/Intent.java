package intents;

import java.util.List;

/**
 * Esta es la clase de Intent.
 * Guarda frases que no contienen parametros
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class Intent {
	private String name;
	private String[] replyAttribute;
	private String[] lastReply;
	private List<StructuredPhrase> phrases;

	/**
	 * Constructor de Intent
	 * 
	 * @param name   nombre del intent
	 * @param phrase conjunto de frases que guarda el intent
	 */
	public Intent(String name, List<StructuredPhrase> phrase) {
		this.name = name;
		this.phrases = phrase;
	}

	/**
	 * Metodo para procesar una frase.
	 * En este caso no se hace nada, ya que la frase no contiene parametros
	 * 
	 * @param text frase a procesar
	 * 
	 * @return el propio Intent
	 */
	public Intent process(String text) {
		return this;
	}

	/**
	 * Metodo para comprobar si una frase se corresponde con
	 * alguna existente en el intent
	 * 
	 * @param text frase a comprobar
	 * 
	 * @return true si matchea, false en caso contrario
	 */
	public boolean matches(String text) {
		if (text == null)
			return false;

		String[] t = text.split(" ");
		boolean match = true;
		List<String> phrase;

		for (StructuredPhrase p : this.phrases) {
			phrase = p.getPhrase();

			for (int i = 0; i < t.length; i++) {
				if (!(phrase.get(i).equalsIgnoreCase(t[i]))) {
					match = false;
					break;
				}
			}

			// Hay una frase que coincide
			if (match)
				return true;

			match = true;
		}

		return false;
	}

	/**
	 * Metodo para establecer la respuesta a las frases del intent
	 * 
	 * @param text la frase a establecer como respuesta
	 * 
	 * @return el propio Intent
	 */
	public Intent replies(String text) {
		if (text == null)
			return null;

		this.replyAttribute = text.split(" ");

		return this;
	}

	/**
	 * Metodo para obtener la respuesta
	 * 
	 * @return la respuesta
	 */
	public String getReply() {
		String replyPhrase = "";
		int i = 0;

		if (this.lastReply != null) {
			for (String s : this.lastReply) {
				if (i == this.lastReply.length)
					replyPhrase += s;
				else
					replyPhrase += s + " ";

				i++;
			}
		} else {
			for (String s : this.replyAttribute) {
				if (i == this.replyAttribute.length)
					replyPhrase += s;
				else
					replyPhrase += s + " ";

				i++;
			}
		}

		return replyPhrase;
	}

	/**
	 * @return la respuesta del intent
	 */
	protected String[] getReplyAttribute() {
		return this.replyAttribute;
	}

	/**
	 * @return el conjunto de frases que guarda el intent
	 */
	public List<StructuredPhrase> getPhrases() {
		return this.phrases;
	}

	/**
	 * Metodo para obtener el objeto generado con el intent
	 * 
	 * @return el objeto generado (en la clase Intent es nulo)
	 */
	public Object getObject() {
		return null;
	}

	/**
	 * Metodo para establecer la ultima respuesta generada
	 * 
	 */
	public void setLastReply(String[] lastReply) {
		this.lastReply = lastReply;
	}

	/**
	 * Metodo para obtener la ultima respuesta generada
	 * 
	 * @return la ultima respuesta generada
	 */
	public String[] getLastReply() {
		return this.lastReply;
	}
}

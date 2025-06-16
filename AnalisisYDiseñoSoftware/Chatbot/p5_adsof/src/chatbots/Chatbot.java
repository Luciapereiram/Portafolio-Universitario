package chatbots;

import intents.*;
import java.util.*;

/**
 * Esta es la clase Chatbot
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 *
 * @param <E> tipo de objeto en el que se basa el chatbot
 */
public class Chatbot<E> {
	private String name;
	private List<Intent> intents;
	private String failedReply;
	private E objectGenerated;

	/**
	 * Constructor de Chatbot
	 * 
	 * @param name nombre del chatbot
	 */
	public Chatbot(String name) {
		this.name = name;
		this.intents = new ArrayList<Intent>();
	}

	/**
	 * Metodo para agregar intents
	 * 
	 * @param intent intent a agregar
	 * 
	 * @return el propio chatbot o null en caso de error
	 */
	public Chatbot<E> withIntent(Intent intent) {
		if (intent == null)
			return null;

		this.intents.add(intent);

		return this;
	}

	/**
	 * Metodo para agregar fallback
	 * 
	 * @param fallback frase fallback a agregar
	 * 
	 * @return el propio chatbot o null en caso de error
	 */
	public Chatbot<E> withFallback(String fallback) {
		if (fallback == null)
			return null;

		this.failedReply = fallback;

		return this;
	}

	/**
	 * Metodo para imprimir respuesta del chatbot a una determinada frase
	 * 
	 * @param userEntry frase que introduce el usuario
	 * 
	 * @return el propio chatbot o null en caso de error
	 */
	public Chatbot<E> reactTo(String userEntry) {
		String user = "User> ", chatbot = this.name + "> ";

		// En caso de error o mensaje vacio, el chatbot imprime mensaje de error
		if (userEntry == null || userEntry.isBlank()) {
			System.out.println(chatbot + this.failedReply);
			return this;
		}

		// Se imprime mensaje introducido por el usuario
		System.out.println(user + userEntry);

		// Si hay un intent que puede procesar dicho mensaje,
		// imprime la respuesta
		for (Intent i : this.intents) {
			if (i.matches(userEntry)) {
				System.out.println(chatbot + i.process(userEntry).getReply());
				// si el intent genera un objeto, este pasa a ser el objeto que se almacena en
				// el chatbot
				if ((E) i.getObject() != null) {
					this.objectGenerated = (E) i.getObject();
				}
				return this;
			}
		}

		// En caso contrario, se imprime mensaje de error
		System.out.println(chatbot + this.failedReply);
		return this;
	}

	/**
	 * Metodo para obtener el objeto
	 * 
	 * @return el objeto generado
	 */
	public E getObject() {
		return this.objectGenerated;
	}
}

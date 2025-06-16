package chatbots;

import intents.*;

/**
 * Esta es la clase ChatbotBuilder
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 *
 * @param <E> tipo de objeto en el que se basa el chatbotBuilder
 */
public class ChatbotBuilder<E> implements Builder<Chatbot<E>> {
	private Chatbot<E> chatbot;
	
	/**
	 * Constructor de ChatbotBuilder
	 * 
	 * @param name nombre para el chatbot
	 */
	public ChatbotBuilder(String name) {
		this.chatbot = new Chatbot<E>(name);
	}
	
	/**
	 * Metodo para agregar intents al chatbot
	 * 
	 * @param intent intent a agregar al chatbot
	 */
	public void withIntent(Intent intent) {
		this.chatbot.withIntent(intent);
	}
	
	/**
	 * Metodo para agregar fallback al chatbot
	 * 
	 * @param fallback frase fallback a agregar al chatbot
	 */
	public void withFallback(String fallback) {
		this.chatbot.withFallback(fallback);
	}
	
	/**
	 * @return el chatbot 
	 */
	public Chatbot<E> getChatbot() {
		return this.chatbot;
	}
	
	/**
	 * Metodo de la interfaz Builder
	 */
	@Override
	public Chatbot<E> build() {
		return this.chatbot;
	}
}

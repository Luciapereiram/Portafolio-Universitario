package chatbots;

import java.util.List;

import intents.Intent;
import intents.StructuredPhrase;

/**
 * Esta es la clase ChitChatChatbot
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 *
 * @param <E> tipo de objeto en el que se basa el chatbot
 */
public class ChitChatChatbotBuilder<E> extends ChatbotBuilder<E> {

	/**
	 * Constructor del ChitChatChatbotBuilder. Por defecto, se añaden al chatbot
	 * intents de bienvenida, informales y despedida, además del fallback.
	 * 
	 * @param name nombre para el chatbot
	 */
	public ChitChatChatbotBuilder(String name) {
		super(name);

		// Se agregan las frases de bienvenida, informales y despedida
		this.getChatbot().withIntent(new Intent("bienvenida", List.of(new StructuredPhrase().with("Hello").with("Hi!")))
				.replies("Welcome to Java Cafe, how can I help you?"));

		this.getChatbot().withIntent(new Intent("informal", List.of(new StructuredPhrase().with("How are you?")))
				.replies("I'm good, what can I do for you today?"));

		this.getChatbot().withIntent(new Intent("despedida", List.of(new StructuredPhrase().with("Bye bye!")))
				.replies("Thank you, please call again!"));

		// Se agrega frase de fallback por defecto
		this.getChatbot().withFallback("Sorry, I don't understand you. Can you repeat it?");
	}

	/**
	 * Metodo de la interfaz Builder
	 */
	@Override
	public Chatbot<E> build() {
		return this.getChatbot();
	}

}

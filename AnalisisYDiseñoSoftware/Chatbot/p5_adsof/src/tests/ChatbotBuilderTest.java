package tests;

import coffee.*;
import chatbots.*;

public class ChatbotBuilderTest {
	public static void main(String[] args) {
		Chatbot<CoffeeOrder> chatbot = createChatbot(new ChatbotBuilder<CoffeeOrder>("Java Cafe"),
				"Sorry, I did not understand that, but I may help you ordering coffee.");
		doInteraction(chatbot);
		System.out.println("==============================");
		chatbot = createChatbot(new ChitChatChatbotBuilder<CoffeeOrder>("Java Cafe"), null);
		doInteraction(chatbot);
	}

	private static void doInteraction(Chatbot<CoffeeOrder> cb) {
		cb.reactTo("Hello").reactTo("How are you?").reactTo("I'd like a coffee").reactTo("Bye bye!");
		System.out.println("Returned object: " + cb.getObject());
	}

	private static Chatbot<CoffeeOrder> createChatbot(ChatbotBuilder<CoffeeOrder> builder, String fallBack) {
		builder.withIntent(IntentTest.orderIntent());
		if (fallBack != null)
			builder.withFallback(fallBack);
		return builder.build();
	}
}

package tests;

import chatbots.*;
import coffee.*;

public class ChatbotTest {
	public static void main(String[] args) {
		Chatbot<CoffeeOrder> coffeeShop = createChatbot();
		coffeeShop.reactTo("Hello").reactTo("How are you?").reactTo("I'd like a coffee");
		CoffeeOrder co = coffeeShop.getObject();
		System.out.println("Returned object: " + co);
	}

	public static Chatbot<CoffeeOrder> createChatbot() {
		Chatbot<CoffeeOrder> coffeeShop = new Chatbot<CoffeeOrder>("Java Cafe").withIntent(IntentTest.greetingIntent())
				.withIntent(IntentTest.orderIntent())
				.withFallback("Sorry, I did not understand that, but I may help you ordering coffee");
		return coffeeShop;
	}
}

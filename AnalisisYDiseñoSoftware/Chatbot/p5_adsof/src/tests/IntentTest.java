package tests;

import coffee.*;
import intents.*;

import java.util.List;

public class IntentTest {
	public static void main(String[] args) {
		Intent greeting = greetingIntent();
		ContextIntent<CoffeeOrder> order = orderIntent();
		System.out.println(greeting.matches("Hello"));
		System.out.println(greeting.process("Hello").getReply());
		System.out.println(order.matches("I'd like a capuccino"));
		System.out.println(order.process("I'd like a capuccino").getReply());

		CoffeeOrder coffeeOrder = order.getObject();
		System.out.println(coffeeOrder);
		System.out.println(order instanceof Intent); // ContextIntents are Intents
	}

	public static ContextIntent<CoffeeOrder> orderIntent() {
		return new ContextIntent<CoffeeOrder>("Coffee Order", List.of(TextInputMain.createPhrases()))
				.withParameter("coffee-number", s -> s.matches("\\d+"), s -> Integer.valueOf(s))
				.withParameter("coffee-type", s -> IntentHelper.containsIgnoreCase(s, CoffeeType.values()),
						s -> CoffeeType.valueOf(s.toUpperCase()))
				.resultObject(c -> new CoffeeOrder(c.<Integer>getParam("coffee-number"),
						c.<CoffeeType>getParam("coffee-type")))
				.replies("All right, you ordered #coffee-number# #coffee-type#");
	}

	public static Intent greetingIntent() {
		return new Intent("Greetings", List.of(new StructuredPhrase().with("Hello")))
				.replies("Welcome to Java Cafe, how can I help you?");
	}
}

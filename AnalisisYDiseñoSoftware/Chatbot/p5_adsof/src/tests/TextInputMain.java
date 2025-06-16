package tests;

import coffee.*;
import intents.*;

public class TextInputMain {
	public static void main(String[] args) {
		StructuredPhrase[] phrases = createPhrases();
		for (StructuredPhrase sp : phrases) {
			System.out.println("'" + sp + "' with parameters:");
			System.out.println(" + coffee-type = " + sp.getValue("coffee-type"));
			System.out.println(" + coffee-number = " + sp.getValue("coffee-number"));
		}
	}

	public static StructuredPhrase[] createPhrases() {
		StructuredPhrase phrases[] = {
				new StructuredPhrase().with("I'd like a").with("coffee-type", CoffeeType.CAPUCCINO)
						.setting("coffee-number", 1),
				// coffee-number vale 1
				new StructuredPhrase().with("I'd like a coffee").setting("coffee-number", 1)
						// coffee-number vale 1
						.setting("coffee-type", CoffeeType.ESPRESSO), // coffee-type vale espresso
				new StructuredPhrase().with("Can I have").with("coffee-number", 2)
						.with("coffee-type", CoffeeType.ESPRESSO).with("please?") };
		return phrases;
	}
}

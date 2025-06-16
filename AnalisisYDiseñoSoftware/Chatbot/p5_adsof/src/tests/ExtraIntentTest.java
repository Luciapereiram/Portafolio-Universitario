package tests;

import coffee.*;
import intents.*;
import java.util.*;

public class ExtraIntentTest {
    public static void main(String[] args) {
        ContextIntent<CoffeeOrder> orderTry1 = orderIntent();
        ContextIntent<CoffeeOrder> orderTry2 = orderIntent();
        ContextIntent<CoffeeOrder> orderTry3 = orderIntent();
        ContextIntent<CoffeeOrder> orderTry4 = orderIntent();

        System.out.println(orderTry1.matches("I'd like a americano"));
        System.out.println(orderTry1.process("I'd like a americano").getReply());

        CoffeeOrder coffeeOrder1 = orderTry1.getObject();
        System.out.println(coffeeOrder1);

        // probando con otro tipo de cafe
        System.out.println(orderTry2.matches("I'd like a espresso"));
        System.out.println(orderTry2.process("I'd like a espresso").getReply());

        CoffeeOrder coffeeOrder2 = orderTry2.getObject();
        System.out.println(coffeeOrder2);

        // probando que ocurre si falta un parametro (debe retornar FALSE)
        System.out.println(orderTry3.matches("I'd like a "));

        // probando con variacion en las mayusculas
        System.out.println(orderTry4.matches("CaN i haVe 42069 CaPuCcINO plEase?"));
        System.out.println(orderTry4.process("CaN i haVe 42069 CaPuCcINO plEase?").getReply());

        CoffeeOrder coffeeOrder4 = orderTry4.getObject();
        System.out.println(coffeeOrder4);

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
}

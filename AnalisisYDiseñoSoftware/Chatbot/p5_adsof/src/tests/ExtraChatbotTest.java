package tests;

import coffee.*;
import chatbots.*;

public class ExtraChatbotTest {
    public static void main(String[] args) {
        Chatbot<CoffeeOrder> coffeeShop = ChatbotTest.createChatbot();
        coffeeShop.reactTo("Hello").reactTo("How are you?");
        coffeeShop.reactTo("I'd like a coffee");
        CoffeeOrder co = coffeeShop.getObject();
        System.out.println("Returned object: " + co);

        // cambiando de pedido (hemos hecho esto posible manejando las respuestas de los
        // intents de manera independiente, teniendo un campo para la respuesta "Tipo" y
        // otro para la ultima respuesta generada)

        coffeeShop.reactTo("can i have 3 americano please?");
        co = coffeeShop.getObject();
        System.out.println("Returned object: " + co);
    }
}

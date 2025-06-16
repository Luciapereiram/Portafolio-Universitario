package intents;

import java.util.*;

/**
 * Esta es la clase StructuredPhrase
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class StructuredPhrase {
    private Map<String, Object> parameters;
    private List<String> phrase;

    /**
     * Constructor de StructuredPhrase
     */
    public StructuredPhrase() {
        this.phrase = new ArrayList<String>();
        this.parameters = new HashMap<String, Object>();
    }

    /**
     * Metodo para agregar elementos a la frase
     * 
     * @param text elementos a agregar
     * 
     * @return la propia StructuredPhrase
     */
    public StructuredPhrase with(String text) {
        if (text == null) {
            return this;
        }

        for (String s : text.split(" ")) {
            this.phrase.add(s);
        }

        return this;
    }

    /**
     * @return los parametros de la frase
     */
    public Map<String, Object> getParameters() {
        return parameters;
    }

    /**
     * @param parameters los parametros a establecer
     */
    public void setParameters(Map<String, Object> parameters) {
        this.parameters = parameters;
    }

    /**
     * @return la frase en si
     */
    public List<String> getPhrase() {
        return phrase;
    }

    /**
     * @param phrase la frase a establecer
     */
    public void setPhrase(List<String> phrase) {
        this.phrase = phrase;
    }

    /**
     * Metodo para agregar un parametro a la frase
     * 
     * @param text      nombre del parametro
     * @param parameter valor del parametro
     * 
     * @return la propia StructuredPhrase
     */
    public StructuredPhrase with(String text, Object parameter) {
        if (text == null || parameter == null) {
            return this;
        }

        this.setting(text, parameter);

        return this.with("[" + text + "]");
    }

    /**
     * Metodo para agregar a un parametro un valor determinado
     * 
     * @param text      nombre del parametro
     * @param parameter valor del parametro a agregar
     * 
     * @return la propia StructuredPhrase
     */
    public StructuredPhrase setting(String text, Object parameter) {
        if (text == null || parameter == null) {
            return this;
        }

        this.parameters.put(text, parameter);

        return this;
    }

    /**
     * Metodo para obtener el valor en String de un parametro dado
     * 
     * @param text nombre del parametro
     * 
     * @return el valor en formato String
     */
    public String getValue(String text) {
        if (text == null || !this.parameters.containsKey(text))
            return null;

        return this.parameters.get(text).toString();
    }

    /**
     * Metodo para obtener el valor de un parametro
     * 
     * @param <P>  parametrizacion
     * @param text nombre del parametro
     * 
     * @return el valor
     */
    public <P extends Object> P getRealValue(String text) {
        if (text == null)
            return null;

        return (P) this.parameters.get(text);
    }

    /**
     * Override de toString
     */
    @Override
    public String toString() {
        String returnValue = "";
        CharSequence aux;
        int i = 0;

        for (String s : this.phrase) {
            if (s.startsWith("[")) {
                aux = s.subSequence(1, (s.length() - 1));
                s = "[" + aux + ":" + this.parameters.get(aux).getClass().getSimpleName() +
                        "(" + this.parameters.get(aux) + ")]";
            }

            if (i == this.phrase.size() - 1)
                returnValue += s;
            else
                returnValue += s + " ";

            i++;
        }

        return returnValue;
    }
}
package tiempo;

/**
 * Esta es la clase Tiempo 
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class Tiempo {
    private int minutos;
    private int segundos;

    /**
     * Constructor de Tiempo. 
     * Se recalcula automaticamente en caso de que algun parametro sobrepase el 60.
     * 
     * @param minutos los minutos
     * @param segundos los segundos
     */
    public Tiempo(int minutos, int segundos) {
        if (minutos < 0) {
            this.minutos = 0;
        } else {
            this.minutos = minutos;
        }

        if (segundos < 0) {
            this.segundos = 0;
        } else if (segundos > 59) {
            this.minutos += segundos / 60;
            this.segundos = segundos % 60;
        } else {
            this.segundos = segundos;
        }
    }

    /**
     * Metodo para sumar tiempos
     * 
     * @param t el tiempo a sumar
     * 
     * @return el tiempo resultante de la suma
     */
    public Tiempo sumarTiempo(Tiempo t) {
        int s_aux;

        this.minutos += t.minutos;

        s_aux = this.segundos + t.segundos;

        // vease que no puede darse el caso en el que s_aux sea negativo, ya que la
        // propia clase
        // Tiempo no permite que se creen objetos con valores negativos para los
        // atributos
        if (s_aux > 59) {
            this.minutos += s_aux / 60;
            this.segundos = s_aux % 60;
        } else {
            this.segundos = s_aux;
        }

        return this;
    }

    /**
     * @return los minutos
     */
    public int getMinutos() {
        return this.minutos;
    }

    /**
     * @return los segundos
     */
    public int getSegundos() {
        return this.segundos;
    }

    /**
     * Metodo para comparar tiempos
     * 
     * @param t tiempo a comparar
     * 
     * @return true si son iguales, false en caso contrario
     */
    public boolean mismoTiempo(Tiempo t) {
    	if (this.minutos == t.minutos && this.segundos == t.segundos) {
    		return true;
    	}
    	
    	return false;
    }
    
    /**
     * Override de toString
     */
    @Override
    public String toString() {
        return minutos + ":" + String.format("%02d", segundos);
    }
}

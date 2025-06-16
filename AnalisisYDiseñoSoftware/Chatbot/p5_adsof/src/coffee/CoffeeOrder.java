package coffee;

/**
 * Esta es la clase CoffeeOrder
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class CoffeeOrder {
	private int num;
	private CoffeeType ct;

	/**
	 * Constructor de CoffeeOrder
	 * 
	 * @param num numero de cafes
	 * @param ct tipo de cafe
	 */
	public CoffeeOrder(int num, CoffeeType ct) {
		this.num = num;
		this.ct = ct;
	}

	/**
	 * Override de toString
	 */
	@Override
	public String toString() {
		return "CoffeeOrder[" + num + ", " + this.ct + "]";
	}
}

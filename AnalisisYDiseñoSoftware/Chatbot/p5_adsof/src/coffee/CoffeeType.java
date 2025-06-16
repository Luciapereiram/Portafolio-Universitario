package coffee;

/**
 * Esta es la enumeracion CoffeeType
 */
public enum CoffeeType {
    /**
     * Tipo de cafe capuccino
     */
    CAPUCCINO,
    /**
     * Tipo de cafe americano
     */
    AMERICANO,
    /**
     * Tipo de cafe espresso
     */
    ESPRESSO;

    /**
     * Override de toString
     */
    @Override
    public String toString() {
        switch (this) {
            case CAPUCCINO:
                return "CAPUCCINO";

            case AMERICANO:
                return "AMERICANO";

            case ESPRESSO:
                return "ESPRESSO";

            default:
                return "CAPUCCINO";

        }
    }
}
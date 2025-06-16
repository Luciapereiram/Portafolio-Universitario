package fonoteca;

/**
 * Esta es la enumeracion EstiloMusical 
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public enum EstiloMusical {
    /**
     * Estilo POP
     */
    POP,
    /**
     * Estilo ROCK
     */
    ROCK,
    /**
     * Estilo DISCO
     */
    DISCO,
    /**
     * Estilo METAL
     */
    METAL,
    /**
     * Estilo REGGAETON
     */
    REGGAETON,
    /**
     * Estilo JAZZ
     */
    JAZZ,
    /**
     * Estilo SOUL
     */
    SOUL,
    /**
     * Estilo CLASICA
     */
    CLASICA,
    /**
     * Estilo SINESTILO
     */
    SINESTILO;

    /**
     * Override de toString
     */
    @Override
    public String toString() {
        switch (this) {
            case POP:
                return "POP";
            case ROCK:
                return "ROCK";
            case DISCO:
                return "DISCO";
            case METAL:
                return "METAL";
            case REGGAETON:
                return "REGGAETON";
            case JAZZ:
                return "JAZZ";
            case SOUL:
                return "SOUL";
            case CLASICA:
                return "CLASICA";
            case SINESTILO:
                return "SIN ESTILO";
            default:
                return "SIN ESTILO";
        }
    }
}

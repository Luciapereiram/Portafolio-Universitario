package fonoteca;

import valoraciones.IUsuario;

/**
 * Esta es la clase Usuario 
 * 
 * @author Jose Luis Capote jose.capote@estudiante.uam.es
 * @author Lucia Pereira lucia.pereiram@estudiante.uam.es
 */
public class Usuario implements IUsuario{
	private static int nIds = 0;
	private String id;
	private String nombre;
	private String nickname;
	
	/**
	 * Constructor de Usuario
	 * 
	 * @param nombre nombre del usuario
	 * @param nickname nickname unico
	 */
	public Usuario(String nombre, String nickname) {
		this.nombre = nombre;
		this.nickname = nickname;
		this.id = String.valueOf(nIds);
		nIds++;
	}
	
	/**
	 * @return el nombre del usuario
	 */
	public String getNombre() {
		return nombre;
	}

	/**
	 * @return el nickname del usuario
	 */
	public String getNickname() {
		return nickname;
	}

	/**
	 * Metodo de la interfaz IUsario
	 */
	@Override
	public String getId() {
		return this.id;
	}

}

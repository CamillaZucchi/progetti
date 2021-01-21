package prg_piscine;

// eccezione creata da noi
public class eccezione extends Exception {
	int numero;
	
	public eccezione (int n) {
		this.numero=n;
	}

}

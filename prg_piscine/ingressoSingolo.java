package prg_piscine;


public class ingressoSingolo extends ingresso {
private double prezzo; 
private int eta;
	
	//costruttore
	public ingressoSingolo(String nome, int data, boolean abbonato, int eta) {
		super(nome, data, abbonato); 
		this.eta=eta;
		setPrezzo();
	}
	
	public ingressoSingolo(int data) {
		super(data);
		eta=0;
	}
		
		public double getPrezzo() {
			return prezzo;
		}
	
		//set prezzo
		
		public void setPrezzo() {
				if (eta<18||eta>65) {
					prezzo=5.50;
					}
				else {
					prezzo=7.00;
					}
				}
		
	public boolean equals (Object o) {
		boolean trovato=false;
		if(o instanceof ingressoSingolo) {
			trovato= ((this.getData())==((ingressoSingolo)o).getData());
		}
		else if (o instanceof ingresso) { 
			trovato=((this.getNome()).equals(((ingresso)o).getNome())) || ((this.getData())==((ingresso)o).getData());
		}
		return trovato;
	}
}

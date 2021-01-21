package prg_piscine;

import java.io.Serializable;

public class ingresso implements Comparable<Object>, Serializable{
	
	private String nome; //nome
	private Integer data; //formato AAAAMMGG non int e non Integer per il toString
	protected boolean abbonato = false;
	
	
	static final long serialVersionUID=1; //richiesta da Serializable

	//costruttore
	public ingresso(String nome,int data,boolean abbonato){
		
		this.nome=nome;
		this.data=data;
		this.abbonato=abbonato;		
	}
	
	public ingresso (int data) { // costruttore per fare la ricerca secondo giorno
		
		nome="";
		this.data=data;
		abbonato=false;
	}
	
	public int getData() {
		return data;
	}
	
	public String getStringData() {
		String dataS=Integer.toString(data); //cast da Integer a String
		String t=dataS.substring(6)+" / "+dataS.substring(4, 6)+" / "+dataS.substring(0,4);
		return t;
	}
	
	
	public String getNome() {
		return nome;
	}
	
	public boolean getAbbonato() {
		return abbonato;
	}
	
	//per scrivere a video
	public String toString() {
		String testo= "\nNome: "+nome+"\nData: "+getStringData();
		if (abbonato) testo+=" abbonato\n";
		else testo+= "non abbonato\n";
		return testo;
	}
	
	// overriding del metodo compareTo in base alla data
	public int compareTo(Object p) {
		ingresso o = (ingresso)p;
		if(this.data<o.data)
			return -1; 
		else if(this.data>o.data)
			return 1;
		else 
			return 0;
	}

	double getPrezzo() {
		return 0;
	}
}

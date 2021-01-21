package prg_piscine;

import java.io.Serializable;

public class ingresso implements Serializable{
	
	private String nome; //nome
	private Integer data; //formato AAAAMMGG non int e non Integer per il toString
	protected boolean abbonato = false; //variabile ereditata dalla sottoclasse, distingue le due classi
	
	
	static final long serialVersionUID=1; //richiesta da Serializable

	//costruttore
	public ingresso(String nome,int data,boolean abbonato){
		
		this.nome=nome;
		this.data=data;
		this.abbonato=abbonato;		
	}
	
	//restituisce la data
	public int getData() {
		return data;
	}

	//restituisce la data come stringa dopo averla trasformata
	public String getStringData() {
		String dataS=Integer.toString(data); //cast da Integer a String
		String t=dataS.substring(6)+" / "+dataS.substring(4, 6)+" / "+dataS.substring(0,4);
		return t;
	}
	
	//restituisce il nome
	public String getNome() {
		return nome;
	}
	
	//restituisce il booleano abbonato
	public boolean getAbbonato() {
		return abbonato;
	}
	
	//restituisce il prezzo
	double getPrezzo() {
		return 0;
	}
	
	//per scrivere a video
	public String toString() {
		String testo= "\nNome: "+nome+"\nData: "+getStringData();
		if (abbonato) testo+=" abbonato\n";
		else testo+= "non abbonato\n";
		return testo;
	}
	
	
}

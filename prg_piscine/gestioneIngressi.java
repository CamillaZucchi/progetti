package prg_piscine;
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.*;


public class gestioneIngressi {
	private Scanner input=new Scanner (System.in);
	private Vector <ingresso> ingressi=new Vector <ingresso>();
	private String nomefile; //nome del file
	private boolean modificato=false; //tenere traccia delle modifiche non salvate su file
	private boolean abbonato;
	
	//costruttore
	public gestioneIngressi(String nomefile) {
		this.nomefile=nomefile;
		
		try {
			ObjectInputStream file_input = new ObjectInputStream(new BufferedInputStream(new FileInputStream(nomefile)));
			// legge l'intero vettore da file
			ingressi = (Vector<ingresso>) file_input.readObject();
			System.out.println("File trovato e aperto.");
			//nome=(ingressi.get(ingressi.size()-1).getNome())+1; //prende nome da ultimo oggetto del vettore e lo incrementa
			file_input.close();
		} catch (FileNotFoundException e) {
			// gestisce il caso in cui il file non sia presente 
			System.out.println("ATTENZIONE: Il file " + nomefile + " non esiste");
			System.out.println("Sara' creato al primo salvataggio");
			System.out.println();
		} catch (ClassNotFoundException e) {
			// gestisce il caso in cui il file non contenga un oggetto
			System.out.println("ERRORE di lettura");
			System.out.println(e);
		} catch (IOException e) {
			// gestisce altri errori di input/output
			System.out.println("ERRORE di I/O");
			System.out.println(e);
		}
		
		
	}
	
	//crea un nuovo ingresso e lo aggiunge al vettore
	public void aggiungiIngresso() {
		String nome="";
		String [] caratteriEvitare= {"1","2","3","4","5","6","7","8","9","0",".",";",",","!","?",":","(",")"}; //array di caratteri non validi come nome
		int controllo;
		boolean trovato=false;
		boolean ok;
		
		//chiediamo il nome all'utente
		do {
			ok=true;
			trovato=false;	
			System.out.println("Digita il nome");
			nome=(input.nextLine()).toUpperCase(); //nome scritto dall'utente
			if(nome.equals("")) { //controlla se scrive qualcosa
				System.out.println("Input non valido, riprova.");
				ok=false;
			}
			else {
				for (int i=0;i<caratteriEvitare.length && !trovato;i++) { //esce dal ciclo quando trova un carattere sbagliato
					controllo=nome.indexOf(caratteriEvitare[i]); //controlla uno alla volta se i caratteri dell'array sono nella stringa
					if(controllo!=-1) {
						trovato=true; //trovato un carattere non adeguato
						ok=false;
						nome=""; //azzera l'input
						System.out.println("Input non valido, riprova.");
					}
				}
			}
		}while(!ok); // se ok e' false, richiede il nome
		
		//chiediamo la data
		int[] giorniMese = {31,28,31,30,31,30,31,31,30,31,30,31};
		int a=0;
		int m=0;
		int gi=0;
		char c= ' ';
		do {
			ok=true;
			try {
				System.out.println("Digita l'anno in formato numerico");
				a =input.nextInt();
				input.nextLine();
				if(a<2020)
					throw new eccezione(a);
				
				System.out.println("Digita il mese in formato numerico");
				m = input.nextInt();
				input.nextLine();
				if(m<1 || m>13)
					throw new eccezione(m);
				
				System.out.println("Digita il giorno in formato numerico");
				gi=input.nextInt();
				input.nextLine();
				if (gi<0 || gi>giorniMese[m-1])
					throw new eccezione(gi);
			}
			catch(InputMismatchException | eccezione e) {
				input.nextLine();
				System.out.println("Input non valido, riprova.");
				ok=false;
			}
		}while(!ok);
		//moltiplichiamo per mantenere la posizione
		a*=10000; 
		m*=100;
		int data=a+m+gi; //trasforma in formato int AAAAMMGG
		
		//chiediamo se l'utente è abbonato
		do {
			ok=true;
			System.out.println("Sei abbonato? (S/N)");
			String s = input.next().toUpperCase();
			if(s.length()!=0) //gestisce la stringa vuota (a capo)
				c=s.charAt(0);
			else
					c=' ';
				switch(c) {
				case 'S':abbonato=true;break;
				case 'N':abbonato=false;break;
				default:System.out.println("Input non valido, riprova.\n");ok=false; // il booleano ok per far ripetere il ciclo
				}
				}while(!ok);
			
		//crea l'oggetto ingresso
		if(abbonato) {
				ingresso ia = new ingresso(nome, data, abbonato);
				ingressi.add(ia);
				System.out.println("Benvenuto! "+ ia.getNome());
		}
		else {
				System.out.println("Quanti anni hai?");
				int eta=input.nextInt();
				ingressoSingolo p = new ingressoSingolo(nome, data, abbonato, eta);
				p.setPrezzo();
				ingressi.add(p);
				System.out.println("Il prezzo e': "+p.getPrezzo());
			}	
				
		modificato=true; // per il salvataggio su file	
		input.nextLine();
	}

	
	//visualizza fatturato giornaliero
	public void fatturatoGiornaliero() {
		int[] giorniMese = {31,28,31,30,31,30,31,31,30,31,30,31};
		int a=0;
		int m=0;
		int gi=0;
		boolean ok;
		double cassaGiornaliera=0;
		do {
			ok=true;
			try {
				System.out.println("Digita l'anno in formato numerico");
				a =input.nextInt();
				input.nextLine();
				if(a<2020)
					throw new eccezione(a);
				
				System.out.println("Digita il mese in formato numerico");
				m = input.nextInt();
				input.nextLine();
				if(m<1 || m>13)
					throw new eccezione(m);
				
				System.out.println("Digita il giorno in formato numerico");
				gi=input.nextInt();
				input.nextLine();
				if (gi<0 || gi>giorniMese[m-1])
					throw new eccezione(gi);
			}
			catch(InputMismatchException | eccezione e) {
				input.nextLine();
				System.out.println("Input non valido, riprova.");
				ok=false;
			}
		}while(!ok);
		
		//moltiplichiamo per mantenere la posizione
		a*=10000;
		m*=100;
		int data=a+m+gi; // formato AAAAMMGG
		for (ingresso i: ingressi) {
			if((i.getData()==data)&&(!i.getAbbonato())) {
				double p=i.getPrezzo();
				cassaGiornaliera+=p;
			}
		}
		System.out.println(cassaGiornaliera);
		}
	
	//ricerca l'ingresso in base al nome o alla data
	public void ricerca() throws eccezione {
		String s="";
		char c=' ';
		boolean ok=false;
		do {	
			System.out.println("Digita N se vuoi cercare per nome, D se vuoi cercare per data e A per annullare.");
			s=input.nextLine().toUpperCase();
			if(s.length()!=0) //gestisce la stringa vuota (a capo)
				c=s.charAt(0);
			else
				c=' '; //azzera il valore precedentemente preso
			switch(c) {
			case 'N':ricercaNome();ok=true;break;
			case 'D':ricercaData();ok=true;break;
			case 'A': break; //per evitare messaggio di default
			default:System.out.println("Input non valido, riprova.\n");break;
			}
		} while(c!='A' && !ok);
	}
	
	public void ricercaNome() {
		String n="";
		while(n.equals("")) {
			System.out.println("Inserisci il nome associato all'abbonamento");
			n=(input.nextLine()).toUpperCase(); //nome scritto dall'utente
		}
		for(ingresso i : ingressi) {
		if((i.getNome().equals(n))&&(i.getAbbonato())) {
			System.out.println("Ingressi dell'abbonato "+ i.getNome()+": "+i.getStringData());
		}
		else
			System.out.println("Nessun abbonato associato al nome");
		}
	}
	
	public void ricercaData() throws eccezione {
		int[] giorniMese = {31,28,31,30,31,30,31,31,30,31,30,31};
		int a=0;
		int m=0;
		int gi=0;
		boolean ok;
		do {
			ok=true;
			try {
				System.out.println("Digita l'anno in formato numerico");
				a =input.nextInt();
				input.nextLine();
				if(a<2020)
					throw new eccezione(a);
				
				System.out.println("Digita il mese in formato numerico");
				m = input.nextInt();
				input.nextLine();
				if(m<1 || m>13)
					throw new eccezione(m);
				
				System.out.println("Digita il giorno in formato numerico");
				gi=input.nextInt();
				input.nextLine();
				if (gi<0 || gi>giorniMese[m-1])
					throw new eccezione(gi);
			}
			catch(InputMismatchException | eccezione e) {
				input.nextLine();
				System.out.println("Input non valido, riprova.");
				ok=false;
			}
		}while(!ok);
		
		//moltiplichiamo per mantenere la posizione
		a*=10000;
		m*=100;
		int data=a+m+gi; // formato AAAAMMGG

		for(ingresso i : ingressi) {
		if((i.getData()==data)&&(i.getAbbonato())) 
			System.out.println("Abbonato "+i.getNome()+" "+i.getStringData());
		}
	}
	
	public void visualizza() throws eccezione {
		String s="";
		char c=' ';
		boolean ok=false;
		do {	
		System.out.println("Digita G se vuoi cercare per giorno, M se vuoi cercare per mese e A per annullare.");
		s=input.nextLine().toUpperCase();
		if(s.length()!=0) //gestisce la stringa vuota (a capo)
			c=s.charAt(0);
		else
			c=' '; //azzera il valore precedentemente preso
		switch(c) {
		case 'G':visualizzaGiorno();ok=true;break;
		case 'M':visualizzaMese();ok=true;break;
		case 'A': break; //per evitare messaggio di default
		default:System.out.println("Input non valido, riprova.\n");break;
		}
	} while(c!='A' && !ok);
}
	
	public void visualizzaGiorno () throws eccezione {
		int[] giorniMese = {31,28,31,30,31,30,31,31,30,31,30,31};
		int a=0;
		int m=0;
		int gi=0;
		boolean ok;
		do {
			ok=true;
			try {
				System.out.println("Digita l'anno in formato numerico");
				a =input.nextInt();
				input.nextLine();
				if(a<2020)
					throw new eccezione(a);
				
				System.out.println("Digita il mese in formato numerico");
				m = input.nextInt();
				input.nextLine();
				if(m<1 || m>13)
					throw new eccezione(m);
				
				System.out.println("Digita il giorno in formato numerico");
				gi=input.nextInt();
				input.nextLine();
				if (gi<0 || gi>giorniMese[m-1])
					throw new eccezione(gi);
			}
			catch(InputMismatchException | eccezione e) {
				input.nextLine();
				System.out.println("Input non valido, riprova.");
				ok=false;
			}
		}while(!ok);
		
		//moltiplichiamo per mantenere la posizione
		a*=10000;
		m*=100;
		int data=a+m+gi; // formato AAAAMMGG

		for(ingresso i : ingressi) {
		if((i.getData()==data)) 
			System.out.println("Utente "+i.getNome()+" "+i.getStringData());
		else
			System.out.println("Nessun ingresso associato al giorno");
		}
	}
	
	public void visualizzaMese () throws eccezione {
		int a=0;
		int m=0;
		int gi=0;
		boolean ok;
		do {
			ok=true;
			try {
				System.out.println("Digita l'anno in formato numerico");
				a =input.nextInt();
				input.nextLine();
				if(a<2020)
					throw new eccezione(a);
				
				System.out.println("Digita il mese in formato numerico");
				m = input.nextInt();
				input.nextLine();
				if(m<1 || m>13)
					throw new eccezione(m);
			}
			catch(InputMismatchException | eccezione e) {
				input.nextLine();
				System.out.println("Input non valido, riprova.");
				ok=false;
			}
		}while(!ok);
		
		//moltiplichiamo per mantenere la posizione
		int [] giorni = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31};
		a*=10000;
		m*=100;
		for(int i=0; i<giorni.length; i++) {
			gi=giorni[i];
			int data=a+m+gi;
			for (ingresso z: ingressi)
			if(z.getData()==data)
				System.out.println("Utente "+z.getNome());
		}
	}

	// verifica se ci sono modifiche non salvate
	public boolean daSalvare() {
		return modificato;
	}
	
	// salva il registro nel file
	// restituisce true se il salvataggio e' andato a buon fine
	public boolean salva() {
		if (daSalvare()) { // salva solo se necessario (se ci sono modifiche)
			try {
				ObjectOutputStream file_output = new ObjectOutputStream(new BufferedOutputStream(new FileOutputStream(nomefile)));
				// salva l'intero oggetto (vettore ingressi) nel file
				file_output.writeObject(ingressi);
				file_output.close();
				modificato = false; // le modifiche sono state salvate
				return true;
			} catch (IOException e) {
				System.out.println("ERRORE di I/O");
				System.out.println(e);
				return false;
			}		
		} else return true;
	}
}


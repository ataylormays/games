class patrolBoat extends ship {
	public patrolBoat(){
		squares = 2;
		name = "Patrol boat";
	}
}

class destroyer extends ship {
	public destroyer(){
		squares = 3;
		name = "Destroyer";
	}
}

class submarine extends ship {
	public submarine(){
		squares = 3;
		name = "Submarine";
	}
}

class battleship extends ship {
	public battleship(){ 
		squares = 4;
		name = "Battleship";
	}
}
 
class aircraftCarrier extends ship {
	public aircraftCarrier(){ 
		squares = 5;
		name = "Aircraft carrier";
	}
}

public class Battleship {
	public static void setO(ship S){
		if (Math.random() >= .5) {
			S.setOrtn('H');
		} else {
			S.setOrtn('V');
		}
	}

	public static void main(String[] args){

		submarine s = new submarine();
		s.printShip();
		setO(s);
		s.printShip();
		System.out.println("Hello world!");
	}

}
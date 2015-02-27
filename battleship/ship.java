public class Ship {
	char orientation;
	int squares;
	String name;
	boolean sunk;

	public Ship(){
		sunk = false;
	}

	public void printShip(){
		System.out.println("Ship name: " + name);
		System.out.println("Squares: " + squares);
		System.out.println("Orientation: " + orientation);
	}

	public void setOrtn(char o) {
		System.out.println("HERE");
		if (!(o == 'H' || o == 'V')){
			System.out.println("Orientation must be set to either V or H.");
			System.exit(0);
		} else {
			orientation = o;
		}

	}
}
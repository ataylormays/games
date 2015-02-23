public class ship {
	char orientation;
	int squares;
	String name;

	public void printShip(){
		System.out.println("Name: " + name);
		System.out.println("Orientation: " + orientation);
		System.out.println("Number of squares: " + squares);
	}

	public void setOrtn(char o){
		if (o != 'H' && o != 'V'){
			System.out.println("Must set orientation to H or V");
			System.exit(0);
		} else{
			orientation = o;
		}
	}
}

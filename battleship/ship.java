public class Ship {
	char orientation;
	int[] xs;
	int[] ys;
	int squares;
	int hits;
	String name;
	boolean sunk;

	public Ship(){
		sunk = false;
	}

	public void printShip(){
		System.out.println("Ship name: " + name);
		System.out.println("Squares: " + squares);
		System.out.println("Hits: " + hits);
		System.out.println("Orientation: " + orientation);
		for(int i = 0; i < xs.length; i++){
			System.out.println(xs[i] + "-" + ys[i]);
		}
	}

	public void setXs(int[] x){
		xs = x;
	}

	public void setYs(int[] y){
		ys = y;
	}


	public void hit(){
		hits++;
		System.out.println("Hit!");
		if(hits==squares){
			sunk = true;
			System.out.println("SUNK!");
		}	
	}

	public void setOrtn(char o) {
		if (!(o == 'H' || o == 'V')){
			System.out.println("Orientation must be set to either V or H.");
			System.exit(0);
		} else {
			orientation = o;
		}

	}
}
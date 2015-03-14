public class Shot{
	int x;
	int y;
	boolean hit;
	boolean sunk;

	public Shot(int xCoor, int yCoor, boolean h, boolean s){
		x = xCoor;
		y = yCoor;
		hit = h;
		sunk = s;
	}

	public void printShot(){
		System.out.println(x + "-" + y + ", " + hit + ", " + sunk);
	}

}
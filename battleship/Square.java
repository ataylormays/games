public class Square {
	int x;
	int y;
	char status; //'H' for hit, 'M' for miss, 'X' for nothing
	boolean free;
	char boat; // 'A'=aircraft carrier, 'D'=destroyer, 'S'=submarine, 'P'=patrolboat, 'b'=battleship 

	public Square(int xCoor, int yCoor){
		x = xCoor;
		y = yCoor;
		status = 'X';
		free = true;
	}

	public void hit(){
		status = 'H';
	}

	public void miss(){
		status = 'M';
		System.out.println("Miss!");
	}
	
	public void setBoat(char s){
		boat = s;
	}

	public void printSquare(){
		System.out.println(x + "-" + y + ", " + status);
	}

}
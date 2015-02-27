public class Square {
	int x;
	int y;
	char hit; //'H' for hit, 'M' for miss, 'X' for nothing
	boolean free;

	public Square(int xCoor, int yCoor){
		x = xCoor;
		y = yCoor;
		hit = 'X';
		free = true;
	}

	public void printSquare(){
		System.out.println(x + "-" + y + ", " + free);
	}

}
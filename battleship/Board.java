public class Board {
	Square[][] layout;

	public Board(){
		layout = new Square[10][10];

		for(int row = 0; row<layout.length; row++){
			for (int col = 0; col<layout[row].length; col++){
				layout[row][col] = new Square(row, col);
			}
		}
	}

	public Square getSquare(int x, int y){
		return layout[x][y];
	}

	public void printBoard(){
		System.out.print("  ");
		for(int k = 0; k < 10; k++){
			System.out.print(k + " ");
		}

		System.out.println("\n");
		for(int j = 0; j < 10; j++){
			System.out.print(j + " ");
			for(int i = 0; i < 10; i++){
				System.out.print(getSquare(i, j).status + " ");
			}
			System.out.print("\n\n");
		}
	}
}
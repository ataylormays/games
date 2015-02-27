public class Board {
	Square[][] layout;
	Player p1;
	Player p2;

	public Board(Player player1, Player player2){
		p1 = player1;
		p2 = player2;
		layout = new Square[10][10];

		for(int row = 0; row<layout.length; row++){
			for (int col = 0; col<layout[row].length; col++){
				Square s = new Square(row, col);
				layout[row][col] = s;
			}
		}
	}

	public Square getSquare(int x, int y){
		return layout[x][y];
	}

	public void printBoard(){
		for(int i = 0; i < 10; i++){
			for(int j = 0; j < 10; j++){
				getSquare(i, j).printSquare();
			}
		}
		System.out.println("exiting printBoard");
	}
}
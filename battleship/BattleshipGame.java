public class BattleshipGame {
	public static void randOrtn(Ship S){
		if (Math.random() >= .5) {
			S.setOrtn('H');
		} else {
			S.setOrtn('V');
		}
	}

	public static void main(String[] args){
		Player aaron = new Player("Aaron");
		Player jess = new Player("Jess");
		Board b = new Board(aaron, jess);
		b.printBoard();
		aaron.p.setOrtn('H');
		aaron.setShip(aaron.p, b, 1, 1);
		b.printBoard();
	}

}
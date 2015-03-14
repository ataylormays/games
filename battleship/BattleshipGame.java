import java.util.Random;
import java.util.Scanner;

public class BattleshipGame {

	public static int incDiff(int n, int m){
		return m-n+1;
	}

	public static int[] maxArea(Board b, int x, int y){

		int minX = 0;
		int maxX = 9;
		int minY = 0;
		int maxY = 9;

		int[] maxDims = new int[5];

		//go as far to the right on first row as possible
		for(int i = x; i < 9; i++){
			if(b.getSquare(i, y).status != 'X'){
				maxX = i;
				break;
			}
		}

		//go as far to the left on first row as possible
		for(int i = x; i > 0; i--){
			if(b.getSquare(i, y).status != 'X'){
				minX = i;
				break;
			}
		}

		int xStart = 0;
		if (minX != 0){
			xStart = minX + 1;
		}

		//find first non-empty square in down direction
		for(int j = xStart; j < maxX; j++){
			for(int k = y; k < 9; k++){
				if(b.getSquare(j, k).status != 'X'){
					if(k < maxY){
						maxY = k;
					}
					break;
				}
			}
		}

		//find first non-empty square in up direction
		for(int j = xStart; j < maxX; j++){
			for(int k = y; k > 0; k--){
				if(b.getSquare(j, k).status != 'X'){
					if(k > minY){
						minY = k;
					}
					break;
				}
			}
		}

		maxDims[0] = minX;
		maxDims[1] = maxX;
		maxDims[2] = minY;
		maxDims[3] = maxY;
		maxDims[4] = incDiff(minX, maxX)*incDiff(minY, maxY);
		
		return maxDims;

	}

	public static int[] midRect(int[] dims){
		int inc1 = 0;
		int inc2 = 0;
		if (Math.random() >= .5){
			inc1 = 1;
		}

		if (Math.random() >= .5){
			inc2 = 1;
		}


		int[] center = new int[2];
		center[0] = (int) (dims[1]-dims[0])/2 + dims[0] + inc1;
		center[1] = (int) (dims[3]-dims[2])/2 + dims[2] + inc2;
		System.out.println("      " + center[0]);
		System.out.println("      " + center[1]);
		return center;
	}
	/*
	Algo for checking previous hits:
		keep array of previous five shots
		check last element. 
		if hit, check sunk.
			if sunk, fire using maxArea
			if not, go back one more to check direction
				if direction, fire in direction
				if not, fire at 90 degrees
		if not hit (if miss), go back. repeat until hit is found.
			if hit, check sunk. 
				if sunk, fire using maxArea. 
				if not, go back one more to check direction.
					if direction, go back to find first hit. fire at 180 degrees

		after firing, get rid of first elt of array and append fire

	*/
	
	public static void main(String[] args){
		Scanner scanner = new Scanner(System.in);
		System.out.print("Welcome to Battleship! What's your name? ");
		String name = scanner.nextLine();
		Player player = new Player(name);
		Player cpu = new Player("CPU");
		boolean turn = true;
		
		//player.setFleetManual();
		player.setRandFleet();
		cpu.setRandFleet();
		
		while(player.alive() && cpu.alive()){
			if(turn){
				System.out.println(player.name + "'s board:\n\n");
				player.board.printBoard2();
				System.out.println("CPU's board\n");
				cpu.board.printBoard2();
				System.out.print("Where would you like to fire? ");
				String m = scanner.nextLine();
				int[] move = player.parseMove(m);
				player.fire(cpu, move[0], move[1]);
			}
			else {
				
				int[] max = new int[5];
				for(int i = 0; i < 9; i++){
					for(int j = 0; j < 9; j++){
						int[] m = maxArea(player.board, i, j);
						if(m[4] > max[4]){
							max = m;
						}
					}
				}

				for(int i = 0; i < max.length; i++){
					System.out.println("   " + max[i]);
				}
				int[] dest = midRect(max);
				cpu.fire(player, dest[0], dest[1]);
			}
			turn = !turn;
		}
		
		if(player.alive()){
			System.out.println("CONGRATS " + player.name + " YOU WIN!!");
		} else {
			System.out.println("Well  " + player.name + ", you suck at Battleship but at least your algo is good.");
		}

	}

}
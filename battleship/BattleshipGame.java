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
		for(int i = x; i <= 9; i++){
			if(b.getSquare(i, y).status != '-'){
				if(i!=x){
					maxX = i-1;
				}
				else{
					maxX = x;
				}
				break;
			}
		}

		//go as far to the left on first row as possible
		for(int i = x; i >= 0; i--){
			if(b.getSquare(i, y).status != '-'){
				if(i!=x){
					minX = i+1;
				} 
				else{
					minX = x;
				}
				break;
			}
		}

		//find first non-empty square in down direction
		for(int j = minX; j <= maxX; j++){
			for(int k = y; k <= 9; k++){
				if(b.getSquare(j, k).status != '-'){
					if(k < maxY){
						if(k!=y){
							maxY = k-1;
						}
						else{
							maxY = k;
						}
					}
					break;
				}
			}
		}

		//find first non-empty square in up direction
		for(int j = minX; j <= maxX; j++){
			for(int k = y; k >= 0; k--){
				if(b.getSquare(j, k).status != '-'){
					if(k >= minY){
						if(k!=y){
							minY = k+1;
						}
						else{
							minY = k;
						}
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

	public static int halfFloat(int n, int m){
		//if even number of inclusive squares b/w n & m, 
		//50/50 chance of left and right side of middle 
		//eg if 1, 2, 3, 4 -> 2 or 3
		if(incDiff(n, m) % 2 == 0){
			int inc = 0;
			if (Math.random() >= .5){
				inc = 1;
			}
			return incDiff(n, m)/2 + n + inc - 1;
			}
		//if odd, return square directly in the middle 
		//eg if 1, 2, 3 -> 2
		else{
			return incDiff(n, m)/2 + n;
		}
	}

	public static int[] midRect(int[] dims){
		int[] center = new int[2];
		center[0] = halfFloat(dims[0], dims[1]);
		center[1] = halfFloat(dims[2], dims[3]);
		return center;		
	}

	public static int[] maxDir(Board b, int x, int y){
		int[] dirs = {0, 0};
		int max = 0;
		boolean edge = false;

		//check up
		for(int i = y-1; i >= 0; i--){
			if(b.getSquare(x, i).status != '-'){
				edge = true;
				if(y-i-1 > max){
					max = y-i-1;
					dirs[0] = 0;
					dirs[1] = -1;
				}
				break;
			}
		}
		if(!edge && y > max){
			max = y;
			dirs[0] = 0;
			dirs[1] = -1;
		}

		edge = false;
		//check right 
		for(int i = x+1; i < 9; i++){
			if(b.getSquare(i, y).status != '-'){
				edge = true;
				if(i-x-1 > max){
					max = i-x-1;
					dirs[0] = 1;
					dirs[1] = 0;
				}
				break;
			}
		}
		if(!edge && 9-x > max){
			max = 9-x;
			dirs[0] = 1;
			dirs[1] = 0;
		}

		edge = false;
		//check down
		for(int i = y+1; i < 9; i++){
			if(b.getSquare(x, i).status != '-'){
				edge = true;
				if(i-y-1 > max){
					max = i-y-1;
					dirs[0] = 0;
					dirs[1] = 1;
				}
				break;
			}
		}
		if(!edge && 9-y > max){
			max=9-y;
			dirs[0] = 0;
			dirs[1] = 1;
		}

		edge = false;
		//check left 
		for(int i = x-1; i >= 0; i--){
			if(b.getSquare(i, y).status != '-'){
				edge = true;
				if(x-i-1 > max){
					max = x-i-1;
					dirs[0] = -1;
					dirs[1] = 0;
				}
				break;
			}
		}
		if(!edge && x > max){
			max=x;
			dirs[0] = -1;
			dirs[1] = 0;
		}

		return dirs;
	}

	public static int[] maxAreaScan(Board b){
		int[] max = new int[5];
		for(int j = 0; j < 9; j++){
			for(int k = 0; k < 9; k++){
				int[] m = maxArea(b, j, k);
				if(m[4] > max[4]){
					max = m;
				}
			}
		}
		return max;
	}
	
	public static void main(String[] args){
		Scanner scanner = new Scanner(System.in);
		System.out.print("Welcome to Battleship! What's your name? ");
		String name = scanner.nextLine();
		Player player = new Player(name);
		Player cpu = new Player("CPU");
		boolean turn = true;
		BoundedQueue cpuMoves = new BoundedQueue();
		
		System.out.print("Would you like to set your own pieces or have it done randomly? Type R for random, M for manual: ");
		String choice = scanner.nextLine();
		if(choice.toUpperCase().equals("R")){
			player.setRandFleet();
		}
		else {
			player.setFleetManual();
		}
		cpu.setRandFleet();
		
		while(player.alive() && cpu.alive()){
			if(turn){
				System.out.println("CPU's board\n");
				cpu.board.printBoard();
				System.out.println(player.name + "'s board:\n\n");
				player.board.printBoard();
				System.out.print("Where would you like to fire? ");
				String m = scanner.nextLine();
				if(m.toUpperCase().equals("Q")){
					System.out.println("Thanks for playing, play again soon!");
					System.exit(0);
				}
				int[] move = player.parseMove(m);
				System.out.println(player.name + " is firing at " + move[0] + "-" + move[1]);
				player.fire(cpu, move[0], move[1]);
			}
			else {
				/*
				Algo for checking previous hits:

				look at last five moves
				go from newest to oldest to find first hit
				if hit, check sunk
					if sunk, fire using max Area
					if not sunk, go back further to look for previous hit
						if previous hit, check sunk 
							if sunk, fire in direction w/ maximum empty squares
							if not sunk, go forwards to check if theres a miss before first hit
								if there was a miss, reverse direction and shoot in opposite direction
								if no miss, fire in same direction as two hits
						if no previous hit, fire in direction w/ maximum empty squares
				if no hit, fire using maxArea 

				*/			

				boolean fired = false;

				for(int i = cpuMoves.array.length-1; i >= 0; i--){
					if(cpuMoves.array[i].hit){
						if(cpuMoves.array[i].sunk){
							//fire into middle of open area
							int[] max = maxAreaScan(player.board);
							int[] dest = midRect(max);
							System.out.println("CPU fired at " + dest[0] + "-" + dest[1]);
							cpuMoves.add(cpu.fire(player, dest[0], dest[1]));
							fired = true;
						}
						else{
							//look backwards to find previous hit
							boolean h = false;
							int j = i-1;
							for(; j >=0; j--){
								if(cpuMoves.array[j].hit){
									h = true;
									if(cpuMoves.array[j].sunk){
										int[] dirs = maxDir(player.board, cpuMoves.array[i].x, cpuMoves.array[i].y);
										int xShot = cpuMoves.array[i].x+dirs[0];
										int yShot = cpuMoves.array[i].y+dirs[1];
										System.out.println("CPU fired at " + xShot + "-" + yShot);
										cpuMoves.add(cpu.fire(player, xShot, yShot));
										fired = true;
									}
									else{
										int xDir;
										int yDir;
										if(!cpuMoves.array[4].hit){
											//if most recent shot was a miss, find original hit and fire in opposite direction
											int k = j;
											for(; k >= 0; k--){
												if(cpuMoves.array[k].hit && !cpuMoves.array[k].sunk){
													continue;
												}
												else{
													break;
												}
											}
											xDir = cpuMoves.array[j].x-cpuMoves.array[i].x;
											yDir = cpuMoves.array[j].y-cpuMoves.array[i].y;
											if(xDir != 0){
												xDir = xDir/Math.abs(xDir);
											}
											if(yDir != 0){
												yDir = yDir/Math.abs(yDir);
											}
											int xShot = cpuMoves.array[k+1].x+xDir;
											int yShot = cpuMoves.array[k+1].y+yDir;
											System.out.println("CPU fired at " + xShot + "-" + yShot);
											cpuMoves.add(cpu.fire(player, xShot, yShot));
											fired = true;
										} 
										else {
											xDir = cpuMoves.array[i].x-cpuMoves.array[j].x;
											yDir = cpuMoves.array[i].y-cpuMoves.array[j].y;
											if(xDir != 0){
												xDir = xDir/Math.abs(xDir);
											}
											if(yDir != 0){
												yDir = yDir/Math.abs(yDir);
											}
											int xShot = cpuMoves.array[i].x+xDir;
											int yShot = cpuMoves.array[i].y+yDir;
											System.out.println("CPU fired at " + xShot + "-" + yShot);
											cpuMoves.add(cpu.fire(player, xShot, yShot));
											fired = true;
										}
									}
									break;
								}
							}
							if(h == false){
								int[] dirs = maxDir(player.board, cpuMoves.array[i].x, cpuMoves.array[i].y);
								int xShot = cpuMoves.array[i].x+dirs[0];
								int yShot = cpuMoves.array[i].y+dirs[1];
								System.out.println("CPU fired at " + xShot + "-" + yShot);
								cpuMoves.add(cpu.fire(player, xShot, yShot));
								fired = true;
							}
							
						}
						break;
					}
					
				}

				if(fired == false){
					//fire into middle of open area
					int[] max = maxAreaScan(player.board);					
					int[] dest = midRect(max);
					System.out.println("CPU fired at " + dest[0] + "-" + dest[1]);
					cpuMoves.add(cpu.fire(player, dest[0], dest[1]));
				}
			}
			turn = !turn;
		}
		
		if(player.alive()){
			System.out.println("CONGRATS " + player.name + " YOU WIN!!");
		} else {
			System.out.println("Well  " + player.name + ", you suck at Battleship but at least the AI is good.");
		}

	}

}
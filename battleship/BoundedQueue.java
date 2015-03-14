public class BoundedQueue{
	private int numElts = 0;
	private int head = 0;
	private int tail = 0;
	public Shot[] array = new Shot[4];

	public BoundedQueue(){
		for(int i = 0; i < array.length; i++){
			Shot s = new Shot(0, 0, false, false); 
			array[i] = s;
		}
	}

	public void add(Shot elt){
		if(numElts == array.length){
			for(int i = 0; i < array.length-1; i++){
				array[i] = array[i+1];
			}
			array[array.length-1] = elt;
		}
		else {
			array[tail] = elt;
			tail = (tail + 1) % array.length;
		}
		if(numElts < 4){
			numElts++;
		}
	}

	public void printBQ(){
		for(int i = 0; i < array.length; i++){
			array[i].printShot();
		}
	}

}
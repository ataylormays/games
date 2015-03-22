public class BoundedQueue{
	private int numElts = 0;
	private int head = 0;
	private int tail = 4;
	public Shot[] array = new Shot[5];

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
			for(int i = tail+1; i < array.length; i++){
				array[i-1] = array[i];
			}
			array[array.length-1] = elt;
			tail--;
		}
		if(numElts < 5){
			numElts++;
		}
	}

	public void printBQ(){
		for(int i = 0; i < array.length; i++){
			array[i].printShot();
		}
	}

}
public class ListSample {
  Cell head = null; // reference to the head of the list.

  ListSample(){
    Cell c;

    // insert cells into the head of the list.
    for(int i = 0; i < 3; i++){
      c = new Cell();

      c.value = i;
      c.next = head;

      head = c;
    }

    // print the list.
    c = head;
    while(c != null){
      System.out.print(c.value + " ");
      c = c.next;
    }

    System.out.println();
  }

  public static void main(String[] args){
    new ListSample();
  }
}

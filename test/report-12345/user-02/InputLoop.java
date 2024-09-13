import java.io.BufferedReader;
import java.io.InputStreamReader;

public class InputLoop {
  public static void main(String[] args){
    BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));

    try{
      String line;
      while((line = reader.readLine()) != null){
        System.out.println(line);
      }
      reader.close();
    }catch(Exception e){
      e.printStackTrace();
    }
  }
}

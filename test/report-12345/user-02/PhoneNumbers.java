import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;

public class PhoneNumbers {

  /**
   * @param args
   */
  public static void main(String[] args) {
    if(args.length < 1){
      System.err.println("Usage: java PhoneNumbers <file>");
      System.exit(1);
    }

    HashMap<String,String> phones = new HashMap<>();
    try {
      BufferedReader file = new BufferedReader(new FileReader(args[0]));
      String line;
      while((line = file.readLine()) != null){
        String[] columns = line.split(",");
        phones.put(columns[0], columns[1]);
      }
      file.close();
    } catch (FileNotFoundException e) {
      e.printStackTrace();
      System.exit(1);
    } catch (IOException e) {
      e.printStackTrace();
      System.exit(1);
    }
    
    BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
    try {
      String line;
      while((line = stdin.readLine()) != null){
        String number = (String)phones.get(line);
        if(number == null){
          number = "Unknown user: " + line;
        }
        System.out.println(number);
      }
      stdin.close();
    } catch (IOException e) {
      e.printStackTrace();
      System.exit(1);
    }
  }

}

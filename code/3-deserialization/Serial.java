import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.Arrays;


// exercise goal: get this to run RCE by changing repr appropriately
public class Serial {
    public static void main(String []args) {
        try {
            ByteArrayOutputStream os = new ByteArrayOutputStream();
            ObjectOutputStream out = new ObjectOutputStream(os);
            A a = new A();
            out.writeObject(a);
            byte [] repr = os.toByteArray();
            System.out.println(Arrays.toString(repr));
            // change repr here
            InputStream is = new ByteArrayInputStream(repr);
            ObjectInputStream in = new ObjectInputStream(is);
            B b = (B)in.readObject();
            b = null;
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
        
        System.gc();
    }
}

class A implements Serializable {
    private static final long serialVersionUID = 1L;
    public A() {
        System.out.println("buildAh");
    }

    @Override
    protected void finalize()  {
        System.out.println("deleteAh");
    }
}

class B implements Serializable {
    private static final long serialVersionUID = 2L;
    @Override
    protected void finalize() {
        System.out.println("RCE");
    }
}
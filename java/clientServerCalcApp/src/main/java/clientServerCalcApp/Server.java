package clientServerCalcApp;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class Server 
{
	public static void main(String[] args)
	{
		try {
			ServerSocket ss = new ServerSocket(9300);
			Socket soc = ss.accept();
			BufferedReader in = new BufferedReader(new InputStreamReader(soc.getInputStream()));
			PrintWriter out = new PrintWriter(soc.getOutputStream(),true);
			while (true)
			{
				String str[] = in.readLine().split(":");
				
				int option = Integer.parseInt(str[0]);
				int num1 = Integer.parseInt(str[1]);
				int num2 = Integer.parseInt(str[2]);
				String result ="";
				int flag = 0;
				
				switch (option) 
				{
					case 1: result = "Addition is: "+(num1+num2);break;
					case 2: result = "Subtraction is: "+(num1-num2);break;
					case 3: result = "Multiplication is: "+(num1*num2);break;
					case 4: result = "Division is: "+(num1/num2);break;
					case 5: flag = 1;
					default:break;
				}
				if(flag ==1) 
				{
					break;
				}
				out.println(result);
			}
		} 
		catch (IOException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}

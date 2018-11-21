package chatApp;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ConversationHandler extends Thread
{
	Socket socket;
	BufferedReader in;
	PrintWriter out;
	String name;
	PrintWriter pw;
	static FileWriter fw;
	static BufferedWriter bw;
	DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
	Date date = new Date();

	public ConversationHandler(Socket socket) throws Exception
	{
		this.socket = socket;
		fw = new FileWriter("chatServerLogs",true);
		bw = new BufferedWriter(fw);
		pw = new PrintWriter(bw,true);
	}

	public void run()
	{
		try
		{
			in=new BufferedReader(new InputStreamReader(socket.getInputStream()));
			out=new PrintWriter(socket.getOutputStream(),true);
			
			int count = 0;
			while (true)
			{
				if (count>0)
				{
					out.println("NAMEALREADYEXISTS");
				}
				else 
				{
					out.println("NAMEREQUIRED");
				}
				
				name = in.readLine();
				
				if (name == null)
				{
					return;
				}
				
				
				if (!ChatServer.userNames.contains(name))
				{
					ChatServer.userNames.add(name);
					break;
				}
				count ++;
			}
			
			out.println("NAMEACCEPTED"+name);
			ChatServer.printWriters.add(out);
			
			while (true)
			{
				String message = in.readLine();
				
				if (message== null)
				{
					return;
				}
				
				pw.println(dateFormat.format(date)+" - "+name+": "+ message);
				for(PrintWriter writer : ChatServer.printWriters) 
				{
					writer.println(name + ": "+ message);
				}
			}
			
		} 
		catch (Exception e)
		{
			// TODO: handle exception
		}
	}

}

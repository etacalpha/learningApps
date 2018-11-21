package chatApp;

import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;


public class ChatServer
{
	static ArrayList<String> userNames = new ArrayList<String>();
	static ArrayList<PrintWriter> printWriters = new ArrayList<PrintWriter>();
	
	
	public static void main(String[] args)throws Exception
	{
		System.out.println("Waiting for client");
		ServerSocket ss = new ServerSocket(9030);
		while(true)
		{
			Socket soc = ss.accept();
			System.out.println("Connection Established");
			ConversationHandler handler = new ConversationHandler(soc);
			handler.start();
		}
	}
}

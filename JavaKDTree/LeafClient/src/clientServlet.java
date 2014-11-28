

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.ws.rs.core.MultivaluedMap;

import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.WebResource;
import com.sun.jersey.core.util.MultivaluedMapImpl;



/**
 * Servlet implementation class clientServlet
 */
public class clientServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public clientServlet() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
	Client client = Client.create();
	String v = "119.0 54.0 0.0 0.0 0.0 0.0 0.0 3.0 131.0 108.0 0.0 0.0 0.0 1.0 14.0 17.0 28.0 29.0 10.0 3.0 6.0 29.0 61.0 7.0 0.0 0.0 4.0 4.0 97.0 121.0 17.0 0.0 124.0 20.0 0.0 0.0 0.0 0.0 0.0 10.0 131.0 72.0 0.0 0.0 0.0 0.0 0.0 7.0 69.0 33.0 27.0 6.0 2.0 3.0 10.0 4.0 0.0 1.0 13.0 7.0 101.0 43.0 8.0 1.0 65.0 0.0 0.0 0.0 0.0 0.0 6.0 131.0 131.0 2.0 0.0 0.0 0.0 0.0 11.0 131.0 88.0 1.0 0.0 0.0 0.0 4.0 23.0 47.0 1.0 0.0 0.0 0.0 71.0 54.0 23.0 5.0 97.0 55.0 10.0 0.0 0.0 0.0 7.0 113.0 25.0 52.0 51.0 0.0 0.0 0.0 16.0 119.0 46.0 33.0 8.0 0.0 0.0 1.0 2.0 25.0 7.0 1.0 0.0 0.0 41.0 32.0 2.0 2.0";
	v = v.replace(" ", "+");
	System.out.println(v);
	WebResource resource = client.resource("http://localhost:8080/LeafNodeWebService/search?param1="+v);
	/*MultivaluedMap queryParams = new MultivaluedMapImpl();
	queryParams.add("param1", v);*/
	
	ClientResponse res = resource.get(ClientResponse.class);
	if(res.getStatus() == 200){
		String output = res.getEntity(String.class);
		//System.out.println(output);
	}
	
	
	}

}

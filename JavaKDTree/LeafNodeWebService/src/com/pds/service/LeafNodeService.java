package com.pds.service;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Scanner;
import java.util.zip.GZIPInputStream;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;

	@Path("/")
	public class LeafNodeService {
		public static KDTreeNode root = null;
		public  LeafNodeService() throws FileNotFoundException, IOException{
			if(root!= null){
				System.out.println("tree has been build before");
				return;				
			}
			ArrayList<vectorObject> vectors = new ArrayList<vectorObject>();
			String target_dir = "/leafnodedata/";
	        File dir = new File(target_dir);
	        File[] files = dir.listFiles();
	        for(File f:files){
	        	if(f.isFile()){
	        		System.out.println("Reading File "+f.getName());
	        		vectors.addAll(ReadFile(f));
	        	}
	        }
	        //vectorObject first = vectors.get(0);
			KDTreeNode node = new KDTreeNode();
			root = node;
			node.setList(vectors);
			LinkedList<KDTreeNode> queue =  new LinkedList<KDTreeNode>();
			queue.add(node);
			vectorObject variance = null,mean = null;
			float maxvariance = 0;
			while(!queue.isEmpty())
		 	{
				node = queue.removeFirst();
				mean = node.getMean();
				variance = node.GetMeanVariance(mean);
				maxvariance = 0;
				for(int i =0 ; i< 128 ; i++)
				{
					if(maxvariance < variance.vector[i] ){
						maxvariance = variance.vector[i];
						node.DimensionID = i;
					}
				}
				
				node.split = mean.vector[node.DimensionID];
				if(node.splitNode()){
				queue.add(node.left);
				queue.add(node.right);
				node.list.clear();
				}
			}
		System.out.println(getHeight(root));
		}
		
	
	
	public ArrayList<vectorObject>  ReadFile(File f) throws FileNotFoundException, IOException
	{
		ArrayList<vectorObject> vectors = new ArrayList<vectorObject>();
		if(f.isFile()){
			GZIPInputStream gzip = new GZIPInputStream(new FileInputStream(f));
			BufferedReader br = new BufferedReader(new InputStreamReader(gzip));
			
			Scanner fileScanner = new Scanner(br);
			//System.out.println(fileScanner.hasNextLine());
			while (fileScanner.hasNextLine()){
				//fileScanner.next();
				//fileScanner.next();
				vectorObject object = new vectorObject();
				for(int i =0; i<128; i++)
					object.vector[i] = fileScanner.nextFloat();
				object.setName(fileScanner.nextLine());
				vectors.add(object);
				}
	        	}
		return vectors;
	}
	

	public  String SearchResult(File f) throws FileNotFoundException, IOException{
		ArrayList<vectorObject> vectors ;
		vectors = searchTree(ReadFile(f));
//		Map dictionary = new HashMap<String,int>();

		Map dictionary = new HashMap();
		int val=0;
		for(vectorObject v : vectors){
			if(dictionary.containsKey(v.name)) {
				val = (int) dictionary.get(v.name);
				dictionary.put(v.name, val + 1);
			}else
			{
				System.out.println(" Found vector in file "+v.name);
				dictionary.put(v.name, 1);
			}
		}
		String mostFrequent = "" ; int maxcount = 0,currcount=0;
		for(Object key: dictionary.keySet())
		{
			currcount = (int) dictionary.get(key);
			if(maxcount < currcount){
				maxcount = currcount;
				mostFrequent = (String) key;
			}
		}
		return "hi";

	}
	
	public  int max(int a,int b)
	{
		if(a<b)
			return a;
		return b;
	}
	
	public  int getHeight(KDTreeNode nd){
		if(nd == null)
			return 0;
		if(nd.left == null && nd.right == null)
			return 1;
		return max(getHeight(nd.left),getHeight(nd.right)) + 1;
	}
	
	public  ArrayList<vectorObject> searchTree( ArrayList<vectorObject> imgVectors){
		ArrayList<vectorObject> resultVector = new ArrayList<vectorObject>();
		vectorObject result = new vectorObject();
		/*for(vectorObject v : imgVectors){
			result = searchVector();
			resultVector.add(result);
		}*/
		return resultVector;
		
	}
	
	@GET
	@Path("/search")
	public  String searchVector(@QueryParam("param1") String aa){
		//System.out.println("Inside search");
		KDTreeNode rootself = root;
		aa.replace("+", " ");
		System.out.println(aa);
		vectorObject imgVector = new vectorObject();
		for(int i =0; i<128; i++)
			imgVector.vector[i] = Float.parseFloat( aa.split(" ")[i]);
			
		
		
		while(root.left!= null || root.right != null){
		if(imgVector.vector[root.DimensionID] < root.split)
			if(root.left != null)
				root = root.left;
			else 
				root = root.right;
		else 
			if(root.right != null)	
				root = root.right;
			else
				root= root.left;
		}
		String result = root.list.get(0).name;
		root = rootself;
		//System.out.println(result);
		return result;
	}

}      

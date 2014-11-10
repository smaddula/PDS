package com.pds;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Scanner;
import java.util.zip.GZIPInputStream;

public class buildTree1 {

	public static ArrayList<vectorObject>  ReadFile(File f) throws FileNotFoundException, IOException
	{
		ArrayList<vectorObject> vectors = new ArrayList<vectorObject>();
		if(f.isFile()){
			InputStreamReader gzip = new InputStreamReader(new FileInputStream(f));
			BufferedReader br = new BufferedReader(gzip);
			
			Scanner fileScanner = new Scanner(br);
			while (fileScanner.hasNextLine()){
				fileScanner.next();
				fileScanner.next();
				
				vectorObject object = new vectorObject();
				for(int i =0; i<128; i++){
					object.SetValueAtDimension(i, fileScanner.nextFloat());
				}
				object.setName(fileScanner.nextLine().replace(")", ""));
				vectors.add(object);
				}
	        	}
		return vectors;
	}
	
	
	public static void main(String args[]) throws IOException{
		
		ArrayList<vectorObject> vectors = new ArrayList<vectorObject>();
		
		String target_dir = "C:/test_dir/diroutput/4/";
        File dir = new File(target_dir);
        File[] files = dir.listFiles();
        for(File f:files){
        	if(f.isFile()){
        		System.out.println("Reading File "+f.getName());
        		vectors.addAll(ReadFile(f));
        		//System.out.println("file read");
        	}
        }
		KDTreeNode1 node = new KDTreeNode1();
		KDTreeNode1 root = node;
		node.setList(vectors);
		LinkedList<KDTreeNode1> queue =  new LinkedList<KDTreeNode1>();
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
				if(maxvariance < variance.GetValueAtDimension(i) ){
					maxvariance = variance.GetValueAtDimension(i);
					node.DimensionID = i;
				}
			}
			
			node.split = mean.GetValueAtDimension( node.DimensionID);
			if(node.splitNode()){
			queue.add(node.left);
			queue.add(node.right);
			/*if(prevqueuesize==queue.size())
				count++;
			else
				count=0;
			System.out.println(node.split + " " + node.DimensionID + " queue :"+ queue.size() );
			if(count==100)
				break;*/
			node.list.clear();
			//prevqueuesize = queue.size();
			}
		}
		//queue.clear();
		System.out.println("search result "+SearchResult(new File("C:/test_dir/diroutput/8/input.txt"), root)); 
		//vectorObject res = searchVector(root,first);
		System.out.println(getHeight(root));
	}
	
	public static String SearchResult(File f, KDTreeNode1 root) throws FileNotFoundException, IOException{
		ArrayList<vectorObject> vectors ;
		vectors = searchTree(root, ReadFile(f));
//		Map dictionary = new HashMap<String,int>();

		Map<String,Integer> dictionary = new HashMap<String,Integer>();
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
		return mostFrequent;

	}
	
	public static int max(int a,int b)
	{
		if(a>b)
			return a;
		return b;
	}
	
	public static int getHeight(KDTreeNode1 nd){
		if(nd == null)
			return 0;
		if(nd.left == null && nd.right == null)
			return 1;
		return max(getHeight(nd.left),getHeight(nd.right)) + 1;
	}
	
	public static ArrayList<vectorObject> searchTree(KDTreeNode1 root, ArrayList<vectorObject> imgVectors){
		ArrayList<vectorObject> resultVector = new ArrayList<vectorObject>();
		vectorObject result = new vectorObject();
		for(vectorObject v : imgVectors){
			result = searchVector(root,v);
			resultVector.add(result);
		}
		return resultVector;
		
	}
	
	public static vectorObject searchVector(KDTreeNode1 root, vectorObject imgVector){
		while(root.left!= null || root.right != null){
		if(imgVector.GetValueAtDimension( root.DimensionID) < root.split)
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
		if(root.list.size()==1)
			return root.list.get(0);
		float minDistance = Float.MAX_VALUE;
		float distance;
		vectorObject closestVec = root.list.get(0);
		for(vectorObject v : root.list){
			distance = imgVector.GetEucledeanDistance(v);
			if(distance < minDistance){
				minDistance = distance;
				closestVec = v;
			}
		}
		return closestVec;
	}
}


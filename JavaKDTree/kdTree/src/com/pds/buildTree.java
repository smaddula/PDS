package com.pds;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Scanner;
import java.util.stream.Collectors;
import java.util.zip.GZIPInputStream;

public class buildTree {

	static int numReturns = 5;
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
		KDTreeNode node = new KDTreeNode();
		KDTreeNode root = node;
		node.setList(vectors);
		LinkedList<KDTreeNode> queue =  new LinkedList<KDTreeNode>();
		queue.add(node);
		vectorObject variance = null,mean = null;
		float maxvariance = 0;
		while(!queue.isEmpty())
	 	{
			node = queue.removeFirst();
			if(node.list.size()<15)
				continue;
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
	
	public static String SearchResult(File f, KDTreeNode root) throws FileNotFoundException, IOException{
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
	
	public static int getHeight(KDTreeNode nd){
		if(nd == null)
			return 0;
		if(nd.left == null && nd.right == null)
			return 1;
		return max(getHeight(nd.left),getHeight(nd.right)) + 1;
	}
	
	public static ArrayList<vectorObject> searchTree(KDTreeNode root, ArrayList<vectorObject> imgVectors){
		ArrayList<vectorObject> resultVector = new ArrayList<vectorObject>();
		for(vectorObject v : imgVectors){
			resultVector.addAll(searchVector(root,v));
		}
		return resultVector;
		
	}
	
	public static ArrayList<vectorObject> searchVector(KDTreeNode root, vectorObject imgVector){
		LinkedList<KDTreeNode> queue =  new LinkedList<KDTreeNode>();
		queue.add(root);
		KDTreeNode node;
		ArrayList<KDTreeNode> LeavesToSearch = new ArrayList<KDTreeNode>();
		while(!queue.isEmpty())
		{
			node = queue.removeFirst();
			if(node == null)
				continue;
			if(node.left == null && node.right == null){
				LeavesToSearch.add(node);
				continue;
			}
			if(imgVector.GetValueAtDimension( node.DimensionID) <= Math.ceil( node.split))
				queue.add(root.left);

			if(imgVector.GetValueAtDimension( node.DimensionID) >= Math.floor( node.split))
				queue.add(root.right);
		}
		
		PriorityQueue<DistanceVectorTuple> pqueue = new PriorityQueue<DistanceVectorTuple>(new Comparator<DistanceVectorTuple>(){
			public int compare(DistanceVectorTuple lft , DistanceVectorTuple rgt){
				if(lft.EucledianDistance < rgt.EucledianDistance) return 1;
				if (lft.EucledianDistance == rgt.EucledianDistance) return 0;
				return -1;
			}
		} 
		);
		
		DistanceVectorTuple t ;
		for(KDTreeNode k: LeavesToSearch){
			for(vectorObject v : k.list){
				t = new DistanceVectorTuple();
				t.EucledianDistance = imgVector.GetEucledeanDistance(v);
				t.vec = v;
				pqueue.add(t);
				if(pqueue.size() > numReturns) pqueue.poll();
			}
		}
		
		ArrayList<vectorObject> rtn = new ArrayList<vectorObject>() ;
		
		while(!pqueue.isEmpty())
			rtn.add(pqueue.poll().vec);
		return rtn;
	}
}


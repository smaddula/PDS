package com.pds.service;


import java.util.ArrayList;

public class KDTreeNode {
	public ArrayList<vectorObject> list ;
	public float split;
	public int DimensionID;
	public KDTreeNode left;
	public KDTreeNode right;
	
	public ArrayList<vectorObject> getList() {
		return list;
	}
	public void setList(ArrayList<vectorObject> list) {
		this.list = list;
	}
	public float getSplit() {
		return split;
	}
	public void setSplit(float split) {
		this.split = split;
	}
	public int getDimensionID() {
		return DimensionID;
	}
	public void setDimensionID(int dimensionID) {
		DimensionID = dimensionID;
	}
	public KDTreeNode getLeft() {
		return left;
	}
	public void setLeft(KDTreeNode left) {
		this.left = left;
	}
	public KDTreeNode getRight() {
		return right;
	}
	public void setRight(KDTreeNode right) {
		this.right = right;
	}
	
	public vectorObject getMean(){
		vectorObject v = new vectorObject();
		
		for(int i =0;i<128;i++){
			v.vector[i] = 0;
			for(int j= 0;j<list.size();j++)
				v.vector[i]= ((	v.vector[i]*j)/(j+1)) +  (list.get(j).vector[i]/(j+1));
		}
		return v;
	}
	
	public vectorObject GetMeanVariance(vectorObject mean)
	{
		vectorObject v = new vectorObject();
		float deviation;
		for(int i =0;i<128;i++){
			v.vector[i] = 0;
			
			for(int j= 0;j<list.size();j++)
			{
				deviation = list.get(j).vector[i] - mean.vector[i];
				v.vector[i] = ((v.vector[i]*j)/(j+1)) +  (deviation*deviation/(j+1));
			}
		}
		return v;		
	}
	
	public boolean splitNode(){
		if(list.size()>1){
		
		left = new KDTreeNode();
		right = new KDTreeNode();
		ArrayList<vectorObject> leftList = new ArrayList<vectorObject>();
		ArrayList<vectorObject> rightList = new ArrayList<vectorObject>();
		
		for(vectorObject vec : list){
			if(vec.vector[DimensionID] < split)
				leftList.add(vec);
			else
				rightList.add(vec);
		}
		left.setList(leftList);
		right.setList(rightList);
		
		return true;
	}
		else
			return false;
	}
	
}

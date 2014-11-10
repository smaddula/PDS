package com.pds;

import java.util.ArrayList;

public class KDTreeNode1 {
	public ArrayList<vectorObject> list ;
	public float split;
	public int DimensionID;
	public KDTreeNode1 left;
	public KDTreeNode1 right;

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
	public KDTreeNode1 getLeft() {
		return left;
	}
	public void setLeft(KDTreeNode1 left) {
		this.left = left;
	}
	public KDTreeNode1 getRight() {
		return right;
	}
	public void setRight(KDTreeNode1 right) {
		this.right = right;
	}
	
	public vectorObject getMean(){
		vectorObject v = new vectorObject();
		
		for(int i =0;i<128;i++){
			v.SetValueAtDimension(i,(float) 0.0);
			for(int j= 0;j<list.size();j++)
				v.SetValueAtDimension(i,  ((	v.GetValueAtDimension(i)*j)/(j+1)) +  (list.get(j).GetValueAtDimension(i)/(j+1)));
		}
		return v;
	}
	
	public vectorObject GetMeanVariance(vectorObject mean)
	{
		vectorObject v = new vectorObject();
		float deviation;
		for(int i =0;i<128;i++){
			v.SetValueAtDimension(i, 0) ;
			
			for(int j= 0;j<list.size();j++)
			{
				deviation = list.get(j).GetValueAtDimension(i) - mean.GetValueAtDimension(i);
				v.SetValueAtDimension(i, ((v.GetValueAtDimension(i)*j)/(j+1)) +  (deviation*deviation/(j+1)));
			}
		}
		return v;		
	}
	
	public boolean splitNode(){
		if(list.size()>1){
		
		left = new KDTreeNode1();
		right = new KDTreeNode1();
		ArrayList<vectorObject> leftList = new ArrayList<vectorObject>();
		ArrayList<vectorObject> rightList = new ArrayList<vectorObject>();
		
		for(vectorObject vec : list){
			if(vec.GetValueAtDimension( DimensionID) < split)
				leftList.add(vec);
			else
				rightList.add(vec);
		}
		left.setList(leftList);
		right.setList(rightList);
		if(list.size() == left.list.size()){
			left.list.clear();
			return false;
		}if(list.size() == right.list.size()){
			left.list.clear();
			return false;
		}
		return true;
	}
		else
		return false;
	}
	

	
}

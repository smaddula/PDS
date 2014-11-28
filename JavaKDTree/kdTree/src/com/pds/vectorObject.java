package com.pds;


public class vectorObject {
	private float vector[] = new float[128];
	String name;
	
	public float GetValueAtDimension(int i){
		return vector[i];
	}
	
	public void SetValueAtDimension( int i, float val){
		vector[i] = val;
	}
	
	public float[] getObject() {
		return vector;
	}
	public void setObject(float[] object) {
		this.vector = object;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public float GetEucledeanDistance(vectorObject vec1 ){
		float distance = 0;
		for(int i =0 ; i< 128;i++){
			distance = distance + (vector[i]-vec1.vector[i])*(vector[i]-vec1.vector[i]);
		}
		return (float) Math.sqrt(distance);
	}
}

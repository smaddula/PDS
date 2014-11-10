package com.pds.service;


public class vectorObject {
	float vector[] = new float[128];
	String name;
	
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
}

// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      AsyncControlCharMap.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

import java.util.Arrays;

public class AsyncControlCharMap {

    private boolean[] map;

    public AsyncControlCharMap() {
        // Default map 0xFFFFFFFF
        this.map = new boolean[32];
        Arrays.fill(this.map, true);
    }

    public AsyncControlCharMap(boolean[] map) {
        this.setACCM(map);
    }

    public boolean isInACCM(int dbyte) {
        return ((dbyte < 0x20) && (this.map[dbyte & 0x1F]));
    }

    public void setACCM(boolean[] map) {
        if(map.length != 32) {
            throw new IllegalArgumentException("Invalid map length (!=32)");
        }
        this.map = map;
    }

    public void addCharToMap(int index) {
        if(index >= 32) {
            throw new IllegalArgumentException(
                    "Valid index ranges are 0-31");
        }
        this.map[index] = true;
    }

    public void remCharFromMap(int index) {
        if(index >= 32) {
            throw new IllegalArgumentException(
                    "Valid index ranges are 0-31");
        }
        this.map[index] = false;
    }

    public void clearMap() {
        for(int i = 0; i < 32; i++)
            this.map[i] = false;
    }

    public String toString() {
        String msg = "";
        for(int i = 31; i >= 0; i--) {
            if((i + 1) % 8 == 0 && i != 31) {
                msg += "_";
            }
            msg += map[i] ? "1" : "0";
        }
        return msg;
    }
}
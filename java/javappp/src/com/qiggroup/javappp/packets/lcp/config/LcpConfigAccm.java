// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigAccm.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;


/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpConfigAccm extends LcpConfigOption {

    public static final int TYPE = 0x02;

    private final AsyncControlCharMap map;

    public LcpConfigAccm(boolean[] map) {
        this.map = new AsyncControlCharMap(map);
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.config.LcpConfigOption#generate()
     */
    @Override
    public int[] generate() {
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public String toString() {
        return ("<ACCM Config: " + map.toString() + ">");
    }

    /**
     * @return the map
     */
    public AsyncControlCharMap getMap() {
        return map;
    }

}

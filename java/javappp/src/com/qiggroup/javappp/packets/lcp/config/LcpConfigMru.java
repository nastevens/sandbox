// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigMru.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

/**
 * <code>LcpConfigOption</code> for encapsulating the Maximum-Receive-Unit (MRU)
 * LCP configure option code.
 * 
 * @author Tyler Schloesser <tschloesser@qiggroup.com>
 */
public class LcpConfigMru extends LcpConfigOption {

    public static final int TYPE = 1;
    public static final int LENGTH = 4;
    private int mru;

    /**
     * TODO: (Document constructor)
     */
    public LcpConfigMru(int mru) {
        this.mru = mru;
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.config.LcpConfigOption#generate()
     */
    @Override
    public int[] generate() {
        
        int[] data = new int[LENGTH];
        data[0] = TYPE;
        data[1] = LENGTH;

        data[2] = (mru >> 8) & 0xFF;
        data[3] = mru & 0xFF;

        return data;
    }

    @Override
    public String toString() {
        return String.format("<MRU Config Value %04x>", mru);
    }

}

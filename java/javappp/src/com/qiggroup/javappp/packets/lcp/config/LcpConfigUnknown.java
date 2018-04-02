// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigUnknown.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

/**
 * <code>LcpConfigOption</code> for encapsulating LCP Configure option codes
 * that aren't understood.
 * 
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpConfigUnknown extends LcpConfigOption {

    private int type;
    private int[] data;

    /**
     * Construct new <code>LcpConfigUnknown</code> with raw data
     * <code>data</code>
     */
    public LcpConfigUnknown(int[] data, int type) {
        this.data = data;
        this.type = type;
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpConfigOption#generate()
     */
    @Override
    public int[] generate() {
        return this.data;
    }

    /**
     * @see java.lang.Object#toString()
     */
    @Override
    public String toString() {
        return String.format("<Unknown LCP Config Type %02x>", this.type);
    }

}

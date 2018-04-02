// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigMruFactory.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

import com.qiggroup.javappp.packets.lcp.LcpPacketFactory;

/**
 * Factory to create <code>LcpConfigOption</code>s for encapsulating the
 * Maximum-Receive-Unit (MRU) LCP configure option code.
 * 
 * @author Tyler Schloesser <tschloesser@qiggroup.com>
 */
public class LcpConfigMruFactory extends LcpPacketFactory.ConfigFactory {

    /**
     * TODO: (Document constructor)
     */
    public LcpConfigMruFactory(LcpPacketFactory parent) {
        parent.super(LcpConfigMru.TYPE);        
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketFactory.ConfigFactory#create(int[])
     * 
     * @author Tyler Schloesser <tschloesser@qiggroup.com>
     */
    @Override
    public LcpConfigOption create(final int[] data) {
        int mru;
        mru = data[1];
        mru |= (data[0] << 8);
        System.out.println("length: " + data.length);
        System.out.println("MRU" + Integer.toHexString(mru) + " data0: " + Integer.toHexString(data[0]) + " data1: " + Integer.toHexString(data[1]));
        
        return new LcpConfigMru(mru);
    }
}
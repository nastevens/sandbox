// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigAccmFactory.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;


import com.qiggroup.javappp.packets.lcp.LcpPacketFactory;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpConfigAccmFactory extends LcpPacketFactory.ConfigFactory {

    public LcpConfigAccmFactory(LcpPacketFactory parent) {
        parent.super(LcpConfigAccm.TYPE);
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketFactory.ConfigFactory#create(int[])
     */
    @Override
    public LcpConfigOption create(int[] data) {

        boolean[] map = new boolean[32];

        // Create one large int out of data
        int full = (data[3] << 24) | (data[2] << 16) | (data[1] << 8)
                | (data[0]);

        // Iterate over all bytes to create map
        int mask = 0x01;
        for(int i = 0; i < 32; i++) {
            map[i] = ((full & mask) != 0);
            mask <<= 1;
        }

        return new LcpConfigAccm(map);
    }

}

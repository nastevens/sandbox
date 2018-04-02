// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigMagicNumFactory.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

import com.qiggroup.javappp.packets.lcp.LcpPacketFactory;

/**
 * Factory to create <code>LcpConfigOption</code>s for encapsulating the
 * Magic-Number LCP configure option code.
 * 
 * @author Tyler Schloesser <tschloesser@qiggroup.com>
 */
public class LcpConfigMagicNumFactory extends LcpPacketFactory.ConfigFactory {

    /**
     * TODO: (Document constructor)
     */
    public LcpConfigMagicNumFactory(LcpPacketFactory parent) {
        parent.super(LcpConfigMagicNum.TYPE);
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketFactory.PacketFactory#create(int[])
     */
    @Override
    public LcpConfigOption create(final int[] data) {

        int magic_number;
        magic_number = data[3];
        magic_number |= (data[2] << 8);
        magic_number |= (data[1] << 16);
        magic_number |= (data[0] << 24);

        return new LcpConfigMagicNum(magic_number);

    }

}

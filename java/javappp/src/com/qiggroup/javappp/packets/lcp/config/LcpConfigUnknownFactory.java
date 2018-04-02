// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigUnknownFactory.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

import com.qiggroup.javappp.packets.lcp.LcpPacketFactory;

/**
 * Factory to create <code>LcpConfigOption</code>s for encapsulating LCP
 * Configure option codes that aren't understood.
 * 
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpConfigUnknownFactory extends LcpPacketFactory.ConfigFactory {

    private int type;

    /**
     * Construct <code>LcpConfigUnknownFactory</code> and register it with the
     * <code>LcpPacketFactory</code> as the handler for unknown config option
     * codes.
     */
    public LcpConfigUnknownFactory(LcpPacketFactory parent, int type) {
        parent.super(type);
        this.type = type;
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketFactory.ConfigFactory#create(int[])
     */
    @Override
    public LcpConfigOption create(int[] data) {
        return new LcpConfigUnknown(data, this.type);
    }

}

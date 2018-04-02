// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpPacketUnknownFactory.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp;

import com.qiggroup.javappp.packets.Packet;

/**
 * Factory to create <code>LcpPacketUnknown</code>s for encapsulating LCP
 * packets whose type codes aren't understood.
 * 
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpPacketUnknownFactory extends LcpPacketFactory.PacketFactory {

    private int code;

    /**
     * Construct <code>LcpPacketUnknownFactory</code> and register it with the
     * <code>LcpPacketFactory</code> as the handler for the unknown LCP type.
     */
    public LcpPacketUnknownFactory(LcpPacketFactory parent, int code) {
        parent.super(code);
        this.code = code;
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketFactory.ConfigFactory#create(int[])
     */
    @Override
    public Packet create(int[] data, int id) {
        return new LcpPacketUnknown(data, this.code, id);
    }

}

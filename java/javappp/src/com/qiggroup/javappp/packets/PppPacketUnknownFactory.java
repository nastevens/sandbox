// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      PppPacketUnknownFactory.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets;


/**
 * Factory to create <code>PppPacketUnknown</code>s for encapsulating PPP
 * packets whose protocol codes aren't understood.
 * 
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class PppPacketUnknownFactory extends PppParser.PacketFactory {

    private final int protocol;

    /**
     * Construct <code>PppPacketUnknownFactory</code> and register it with the
     * <code>PppParser</code> as the handler for unknown PPP protocols.
     */
    public PppPacketUnknownFactory(PppParser parent, int protocol) {
        parent.super(protocol);
        this.protocol = protocol;
    }

    /**
     * @see com.qiggroup.javappp.packets.PppParser.PacketFactory#create(int[])
     */
    @Override
    public Packet create(int[] data) {
        return new PppPacketUnknown(data, this.protocol);
    }

}

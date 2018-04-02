// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      PppPacketUnknown.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets;


/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class PppPacketUnknown extends Packet {
    
    private final int protocol;
    private final int[] data;

    /**
     * Construct a new Packet with raw data <code>data</code> and protocol
     * <code>protocol</code>.
     */
    public PppPacketUnknown(int[] data, int protocol) {
        this.protocol = protocol;
        this.data = data;
        System.err.printf("Received unknown PPP packet %02x\n", protocol);
    }

    /**
     * @see com.qiggroup.javappp.packets.Packet#generate()
     */
    @Override
    public int[] generate() {
        // TODO Auto-generated method stub
        return null;
    }

    /**
     * @return the protocol
     */
    public int getProtocol() {
        return protocol;
    }

    /**
     * @return the data
     */
    public int[] getData() {
        return data;
    }

    /**
     * @see java.lang.Object#toString()
     */
    @Override
    public String toString() {
        return String.format("<Unknown PPP Protocol %02x>", this.protocol);
    }

    /**
     * @see com.qiggroup.javappp.packets.Packet#accept(com.qiggroup.javappp.packets.PacketVisitor)
     */
    @Override
    public void accept(PacketVisitor visitor) {
        // TODO Auto-generated method stub

    }

}

// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpPacketConfigure.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp;

import com.qiggroup.javappp.packets.Packet;
import com.qiggroup.javappp.packets.PacketVisitor;

/**
 * <code>Packet</code> for encapsulating LCP codes that aren't understood.
 * 
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpPacketUnknown extends Packet implements LcpPacket {
    
    private int code;
    private int id;
    private int[] data;
    
    /**
     * Construct a new Packet with raw data <code>data</code>.
     */
    public LcpPacketUnknown(final int[] data, final int code, final int id) {
        this.data = data;
        this.code = code;
        this.id = id;
    }
    
    /**
     * @see com.qiggroup.javappp.packets.Packet#generate()
     */
    public int[] generate() {
        // TODO: Recreate packet with code, length, and identifier
        return null;
    }

    /**
     * @see java.lang.Object#toString()
     */
    @Override
    public String toString() {
        return String.format("<Unknown LCP Code %02x>", this.code);
    }

    /**
     * @return the code
     */
    public int getCode() {
        return this.code;
    }

    /**
     * @return the id
     */
    public int getId() {
        return this.id;
    }

    /**
     * @return the data
     */
    public int[] getData() {
        return this.data;
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacket#accept(com.qiggroup.javappp.packets.lcp.LcpPacketVisitor)
     */
    @Override
    public void accept(LcpPacketVisitor visitor) {
        // TODO Auto-generated method stub

    }

    /**
     * @see com.qiggroup.javappp.packets.Packet#accept(com.qiggroup.javappp.packets.PacketVisitor)
     */
    @Override
    public void accept(PacketVisitor visitor) {
        // TODO Auto-generated method stub

    }
}

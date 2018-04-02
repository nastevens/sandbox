// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpPacketTerminateAck.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpPacketTerminateAck extends LcpPacketTerminate implements
        LcpPacket {

    public LcpPacketTerminateAck(int identifier, int[] data) {
        super(identifier, data);
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketTerminate#accept(com.qiggroup.javappp.packets.lcp.LcpPacketVisitor)
     */
    @Override
    public void accept(LcpPacketVisitor visitor) {
        visitor.visit(this);
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketTerminate#generate()
     */
    @Override
    public int[] generate() {
        // TODO Auto-generated method stub
        return null;
    }

    /**
     * @see java.lang.Object#toString()
     */
    @Override
    public String toString() {
        return this.formatLcpString("ACK");
    }

}

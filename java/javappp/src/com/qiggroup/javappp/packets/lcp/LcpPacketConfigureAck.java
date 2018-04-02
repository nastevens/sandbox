// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpPacketConfigureAck.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpPacketConfigureAck extends LcpPacketConfigure {

    public static final int code = 0x02;

    public LcpPacketConfigureAck(final int identifier) {
        super(identifier);
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketConfigure#generate()
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

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketConfigure#accept(com.qiggroup.javappp.packets.lcp.LcpPacketVisitor)
     */
    @Override
    public void accept(LcpPacketVisitor visitor) {
        visitor.visit(this);
    }
}

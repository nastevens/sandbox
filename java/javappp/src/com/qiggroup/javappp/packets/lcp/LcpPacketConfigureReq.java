// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpPacketConfigureReq.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpPacketConfigureReq extends LcpPacketConfigure {

    public static final int code = 0x01;

    public LcpPacketConfigureReq(final int identifier) {
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
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketConfigure#toString()
     */
    @Override
    public String toString() {
        return this.formatLcpString("REQ");
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketConfigure#accept(com.qiggroup.javappp.packets.lcp.LcpPacketVisitor)
     */
    @Override
    public void accept(LcpPacketVisitor visitor) {
        visitor.visit(this);
    }
}

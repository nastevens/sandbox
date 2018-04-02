// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpPacketTerminate.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp;

import com.qiggroup.javappp.packets.Packet;
import com.qiggroup.javappp.packets.PacketVisitor;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public abstract class LcpPacketTerminate extends Packet implements LcpPacket {

    private final int identifier;
    private final int[] data;

    protected LcpPacketTerminate(final int identifier, final int[] data) {
        this.identifier = identifier;
        this.data = data;
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacket#accept(com.qiggroup.javappp.packets.lcp.LcpPacketVisitor)
     */
    @Override
    public abstract void accept(LcpPacketVisitor visitor);

    /**
     * @see com.qiggroup.javappp.packets.Packet#generate()
     */
    @Override
    public abstract int[] generate();

    /**
     * @see com.qiggroup.javappp.packets.Packet#accept(com.qiggroup.javappp.packets.PacketVisitor)
     */
    @Override
    public void accept(PacketVisitor visitor) {
        visitor.visit(this);
    }

    protected String formatLcpString(String codeString) {
        return String.format("<LCP TERMINATE %s|ID %02x />\n", codeString,
                this.identifier);
    }

    /**
     * @return the identifier
     */
    public int getIdentifier() {
        return identifier;
    }

    /**
     * @return the data
     */
    public int[] getData() {
        return data;
    }

}

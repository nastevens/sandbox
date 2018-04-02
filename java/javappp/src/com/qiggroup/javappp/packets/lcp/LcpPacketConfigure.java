// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpPacketConfigure.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp;

import java.util.ArrayList;
import java.util.List;

import com.qiggroup.javappp.packets.Packet;
import com.qiggroup.javappp.packets.PacketVisitor;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigOption;

/**
 * Encapsulates an LCP Configure REQUEST/ACK/NAK/REJECT packet.
 * 
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public abstract class LcpPacketConfigure extends Packet implements LcpPacket {
    
    /** List of LcpConfigOptions in this Configure packet. Use List as
     *  configuration options must stay in the order they were received */
    private List<LcpConfigOption> configOptions;
    
    private final int identifier;
    
    /**
     * Construct a new LcpPacketConfigure with identifier
     * <code>identifier</code> in the range 0-255.
     */
    public LcpPacketConfigure(final int identifier) {
        this.identifier = identifier;
        configOptions = new ArrayList<LcpConfigOption>();
    }
    
    /**
     * Add an <code>LcpConfigOption</code> to this packet.
     */
    public void addConfigOption(LcpConfigOption option) {
        this.configOptions.add(option);
    }
    
    /**
     * Return the List of <code>LcpConfigOption</code>s in this packet.
     */
    public List<LcpConfigOption> getConfigOptions() {
        return this.configOptions;
    }

    /**
     * Set the List of <code>LcpConfigOption</code>s in this packet.
     */
    public void setConfigOptions(List<LcpConfigOption> options) {
        this.configOptions = options;
    }

    /**
     * @return the identifier
     */
    public int getIdentifier() {
        return identifier;
    }

    /**
     * Generate byte representation of this packet.
     * 
     * @see com.qiggroup.javappp.packets.Packet#generate()
     */
    public abstract int[] generate();

    /**
     * @see java.lang.Object#toString()
     */
    @Override
    public abstract String toString();

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacket#accept(com.qiggroup.javappp.packets.lcp.LcpPacketVisitor)
     */
    @Override
    public abstract void accept(LcpPacketVisitor visitor);

    /**
     * @see com.qiggroup.javappp.packets.Packet#accept(com.qiggroup.javappp.packets.PacketVisitor)
     */
    @Override
    public void accept(PacketVisitor visitor) {
        visitor.visit(this);
    }

    protected String formatLcpString(String codeString) {
        String msg = String.format("<LCP CONFIG %s|ID %02x>\n", codeString,
                this.identifier);
        for(LcpConfigOption option : this.configOptions) {
            msg += "    " + option.toString() + "\n";
        }
        msg += "</LCP CONFIG " + codeString + ">\n";
        return msg;
    }
}

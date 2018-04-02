// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      PppPacketEventVisitor.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets;

import com.qiggroup.javappp.packets.ipcp.IpcpPacket;
import com.qiggroup.javappp.packets.ipcp.IpcpPacketVisitor;
import com.qiggroup.javappp.packets.lcp.LcpPacket;
import com.qiggroup.javappp.packets.lcp.LcpPacketVisitor;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class PppPacketEventVisitor implements PacketVisitor {

    private LcpPacketVisitor lcpVisitor = null;
    private IpcpPacketVisitor ipcpVisitor = null;

    public PppPacketEventVisitor() {
    }

    /**
     * @see com.qiggroup.javappp.packets.PacketVisitor#visit(com.qiggroup.javappp.packets.lcp.LcpPacket)
     */
    @Override
    public void visit(LcpPacket packet) {
        if(this.lcpVisitor != null) {
            packet.accept(this.lcpVisitor);
        }
    }

    /**
     * @see com.qiggroup.javappp.packets.PacketVisitor#visit(com.qiggroup.javappp.packets.ipcp.IpcpPacket)
     */
    @Override
    public void visit(IpcpPacket packet) {
        if(this.ipcpVisitor != null) {
        // TODO Auto-generated method stub
        }

    }

    /**
     * @return the lcpVisitor
     */
    public LcpPacketVisitor getLcpVisitor() {
        return lcpVisitor;
    }

    /**
     * @param lcpVisitor
     *            the lcpVisitor to set
     */
    public void setLcpVisitor(LcpPacketVisitor lcpVisitor) {
        this.lcpVisitor = lcpVisitor;
    }

    /**
     * @return the ipcpVisitor
     */
    public IpcpPacketVisitor getIpcpVisitor() {
        return ipcpVisitor;
    }

    /**
     * @param ipcpVisitor
     *            the ipcpVisitor to set
     */
    public void setIpcpVisitor(IpcpPacketVisitor ipcpVisitor) {
        this.ipcpVisitor = ipcpVisitor;
    }

}

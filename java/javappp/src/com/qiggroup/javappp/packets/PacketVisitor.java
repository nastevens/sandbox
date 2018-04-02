// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      PacketVisitor.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets;

import com.qiggroup.javappp.packets.ipcp.IpcpPacket;
import com.qiggroup.javappp.packets.lcp.LcpPacket;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public interface PacketVisitor {

    void visit(LcpPacket packet);

    void visit(IpcpPacket packet);

}

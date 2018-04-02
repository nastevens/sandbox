// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpPacket.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public interface LcpPacket {
    void accept(LcpPacketVisitor visitor);
}

// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpPacketVisitor.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public interface LcpPacketVisitor {

    void visit(LcpPacketConfigureReq packet);

    void visit(LcpPacketConfigureAck packet);

    void visit(LcpPacketConfigureNak packet);

    void visit(LcpPacketConfigureRej packet);

    void visit(LcpPacketTerminateReq packet);

    void visit(LcpPacketTerminateAck packet);

    void visit(LcpPacketUnknown packet);

}

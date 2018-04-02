// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      PppStateMachine.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.protocol.ppp;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.qiggroup.javafsm.api.Memento;
import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javappp.frame.Frame;
import com.qiggroup.javappp.frame.FrameEventListener;
import com.qiggroup.javappp.packets.Packet;
import com.qiggroup.javappp.packets.PppPacketEventVisitor;
import com.qiggroup.javappp.packets.PppParser;
import com.qiggroup.javappp.packets.lcp.LcpPacketConfigureAck;
import com.qiggroup.javappp.packets.lcp.LcpPacketConfigureNak;
import com.qiggroup.javappp.packets.lcp.LcpPacketConfigureRej;
import com.qiggroup.javappp.packets.lcp.LcpPacketConfigureReq;
import com.qiggroup.javappp.packets.lcp.LcpPacketTerminateAck;
import com.qiggroup.javappp.packets.lcp.LcpPacketTerminateReq;
import com.qiggroup.javappp.packets.lcp.LcpPacketUnknown;
import com.qiggroup.javappp.packets.lcp.LcpPacketVisitor;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigAccm;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigOption;
import com.sun.istack.internal.logging.Logger;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class PppStateMachine implements FrameEventListener,
 LcpPacketVisitor {

    private PppParser parser;
    private PppStates states;
    private PppPacketEventVisitor pppVisitor;
    private Memento memento;
    private StateMachine stateMachine;
    private List<LcpConfigOption> wantOptions;
    private List<LcpConfigOption> rcvdOptions;
    private int lastId;
    private int rcvdId;
    private static Logger logger = Logger.getLogger(PppStateMachine.class);

    // TODO: Combine this with the PppStates class
    public PppStateMachine() {
        this.parser = new PppParser();
        this.states = new PppStates(this);
        this.memento = this.states.createMemento();
        this.pppVisitor = new PppPacketEventVisitor();
        this.pppVisitor.setLcpVisitor(this);
        this.stateMachine = states.getStateMachine();
        this.wantOptions = new ArrayList<LcpConfigOption>();
        boolean[] map = new boolean[32];
        Arrays.fill(map, false);
        this.wantOptions.add(new LcpConfigAccm(map));
        this.lastId = -1;
    }

    /**
     * @see com.qiggroup.javappp.frame.FrameEventListener#frameReceived(com.qiggroup.javappp.frame.Frame)
     */
    @Override
    public void frameReceived(Frame f) {
        Packet pkt = this.parser.parse(f.getDataPayload());
        pkt.accept(this.pppVisitor);
    }

    public void open() {
        this.states.getStateMachine().fireEvent(this.memento, PppEvents.OPEN);
    }

    public void close() {
        this.states.getStateMachine().fireEvent(this.memento, PppEvents.CLOSE);
    }

    public void lowerUp() {
        this.states.getStateMachine().fireEvent(this.memento, PppEvents.UP);
    }

    public void lowerDown() {
        this.states.getStateMachine().fireEvent(this.memento, PppEvents.DOWN);
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketVisitor#visit(com.qiggroup.javappp.packets.lcp.LcpPacketConfigureReq)
     */
    @Override
    public void visit(LcpPacketConfigureReq packet) {
        this.rcvdOptions = packet.getConfigOptions();
        this.rcvdId = packet.getIdentifier();
        if(packet.getConfigOptions().equals(this.wantOptions)) {
            this.stateMachine.fireEvent(memento, PppEvents.RCR_PLUS);
        } else {
            this.stateMachine.fireEvent(memento, PppEvents.RCR_MINUS);
        }
        System.out.print(packet.toString());
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketVisitor#visit(com.qiggroup.javappp.packets.lcp.LcpPacketConfigureAck)
     */
    @Override
    public void visit(LcpPacketConfigureAck packet) {
        this.stateMachine.fireEvent(memento, PppEvents.RCA);
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketVisitor#visit(com.qiggroup.javappp.packets.lcp.LcpPacketConfigureNak)
     */
    @Override
    public void visit(LcpPacketConfigureNak packet) {
        this.stateMachine.fireEvent(memento, PppEvents.RCN);
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketVisitor#visit(com.qiggroup.javappp.packets.lcp.LcpPacketConfigureRej)
     */
    @Override
    public void visit(LcpPacketConfigureRej packet) {
        this.stateMachine.fireEvent(memento, PppEvents.RCN);
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketVisitor#visit(com.qiggroup.javappp.packets.lcp.LcpPacketUnknown)
     */
    @Override
    public void visit(LcpPacketUnknown packet) {
        this.stateMachine.fireEvent(memento, PppEvents.RUC);
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketVisitor#visit(com.qiggroup.javappp.packets.lcp.LcpPacketTerminateReq)
     */
    @Override
    public void visit(LcpPacketTerminateReq packet) {
        this.stateMachine.fireEvent(memento, PppEvents.RTR);
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketVisitor#visit(com.qiggroup.javappp.packets.lcp.LcpPacketTerminateAck)
     */
    @Override
    public void visit(LcpPacketTerminateAck packet) {
        this.stateMachine.fireEvent(memento, PppEvents.RTA);
    }

    public void thisLayerUp() {

    }

    public void thisLayerDown() {

    }

    public void thisLayerStarted() {

    }

    public void thisLayerFinished() {

    }

    public void initRestartCount() {

    }

    public void zeroRestartCount() {

    }


    public void sendConfigureReq() {
        LcpPacketConfigureReq pkt = new LcpPacketConfigureReq(this.lastId);
        pkt.setConfigOptions(this.wantOptions);
        logger.info("Sending packet:\n" + pkt.toString());
    }

    public void sendConfigureAck() {
        LcpPacketConfigureReq pkt = new LcpPacketConfigureReq(this.rcvdId);
        pkt.setConfigOptions(this.rcvdOptions);
        logger.info("Sending packet:\n" + pkt.toString());
    }

    public void sendConfigureNak() {

    }

    public void sendTerminateReq() {

    }

    public void sendTerminateAck() {

    }

    public void sendCodeReject() {

    }

    public void sendEchoReply() {

    }

}

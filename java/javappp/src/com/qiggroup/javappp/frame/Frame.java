package com.qiggroup.javappp.frame;

import java.util.Arrays;

import com.qiggroup.javappp.packets.lcp.config.AsyncControlCharMap;

/**
 * Implements an interface to a frame sent or received over a PPP HDLC-like
 * framing channel.
 * 
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class Frame {

    private static final int ESC_VALUE = 0x7d;
    private static final int ESC_MASK = 0x20;
    private static final int FLAG_VALUE = 0x7e;
    private static final int GOODFCS16 = 0xf0b8;
    private static final int FCS16TABLE[] = { 0x0000, 0x1189, 0x2312, 0x329b,
            0x4624, 0x57ad, 0x6536, 0x74bf, 0x8c48, 0x9dc1, 0xaf5a, 0xbed3,
            0xca6c, 0xdbe5, 0xe97e, 0xf8f7, 0x1081, 0x0108, 0x3393, 0x221a,
            0x56a5, 0x472c, 0x75b7, 0x643e, 0x9cc9, 0x8d40, 0xbfdb, 0xae52,
            0xdaed, 0xcb64, 0xf9ff, 0xe876, 0x2102, 0x308b, 0x0210, 0x1399,
            0x6726, 0x76af, 0x4434, 0x55bd, 0xad4a, 0xbcc3, 0x8e58, 0x9fd1,
            0xeb6e, 0xfae7, 0xc87c, 0xd9f5, 0x3183, 0x200a, 0x1291, 0x0318,
            0x77a7, 0x662e, 0x54b5, 0x453c, 0xbdcb, 0xac42, 0x9ed9, 0x8f50,
            0xfbef, 0xea66, 0xd8fd, 0xc974, 0x4204, 0x538d, 0x6116, 0x709f,
            0x0420, 0x15a9, 0x2732, 0x36bb, 0xce4c, 0xdfc5, 0xed5e, 0xfcd7,
            0x8868, 0x99e1, 0xab7a, 0xbaf3, 0x5285, 0x430c, 0x7197, 0x601e,
            0x14a1, 0x0528, 0x37b3, 0x263a, 0xdecd, 0xcf44, 0xfddf, 0xec56,
            0x98e9, 0x8960, 0xbbfb, 0xaa72, 0x6306, 0x728f, 0x4014, 0x519d,
            0x2522, 0x34ab, 0x0630, 0x17b9, 0xef4e, 0xfec7, 0xcc5c, 0xddd5,
            0xa96a, 0xb8e3, 0x8a78, 0x9bf1, 0x7387, 0x620e, 0x5095, 0x411c,
            0x35a3, 0x242a, 0x16b1, 0x0738, 0xffcf, 0xee46, 0xdcdd, 0xcd54,
            0xb9eb, 0xa862, 0x9af9, 0x8b70, 0x8408, 0x9581, 0xa71a, 0xb693,
            0xc22c, 0xd3a5, 0xe13e, 0xf0b7, 0x0840, 0x19c9, 0x2b52, 0x3adb,
            0x4e64, 0x5fed, 0x6d76, 0x7cff, 0x9489, 0x8500, 0xb79b, 0xa612,
            0xd2ad, 0xc324, 0xf1bf, 0xe036, 0x18c1, 0x0948, 0x3bd3, 0x2a5a,
            0x5ee5, 0x4f6c, 0x7df7, 0x6c7e, 0xa50a, 0xb483, 0x8618, 0x9791,
            0xe32e, 0xf2a7, 0xc03c, 0xd1b5, 0x2942, 0x38cb, 0x0a50, 0x1bd9,
            0x6f66, 0x7eef, 0x4c74, 0x5dfd, 0xb58b, 0xa402, 0x9699, 0x8710,
            0xf3af, 0xe226, 0xd0bd, 0xc134, 0x39c3, 0x284a, 0x1ad1, 0x0b58,
            0x7fe7, 0x6e6e, 0x5cf5, 0x4d7c, 0xc60c, 0xd785, 0xe51e, 0xf497,
            0x8028, 0x91a1, 0xa33a, 0xb2b3, 0x4a44, 0x5bcd, 0x6956, 0x78df,
            0x0c60, 0x1de9, 0x2f72, 0x3efb, 0xd68d, 0xc704, 0xf59f, 0xe416,
            0x90a9, 0x8120, 0xb3bb, 0xa232, 0x5ac5, 0x4b4c, 0x79d7, 0x685e,
            0x1ce1, 0x0d68, 0x3ff3, 0x2e7a, 0xe70e, 0xf687, 0xc41c, 0xd595,
            0xa12a, 0xb0a3, 0x8238, 0x93b1, 0x6b46, 0x7acf, 0x4854, 0x59dd,
            0x2d62, 0x3ceb, 0x0e70, 0x1ff9, 0xf78f, 0xe606, 0xd49d, 0xc514,
            0xb1ab, 0xa022, 0x92b9, 0x8330, 0x7bc7, 0x6a4e, 0x58d5, 0x495c,
            0x3de3, 0x2c6a, 0x1ef1, 0x0f78 };

    // private enum StateEnum {
    // WAIT_FOR_START,
    // WAIT_FOR_ADDRESS,
    // READ_ADDRESS_ESCAPE,
    // WAIT_FOR_CONTROL,
    // READ_CONTROL_ESCAPE,
    // READ_DATA,
    // READ_ESCAPE
    // }

    private int maxUnits;
    private int[] data;
    private int dataPtr;
    private boolean acfcEnabled;
    private int fcsLength;
    private AsyncControlCharMap accm;

    /**
     * <p>
     * Construct a frame with the given settings.
     * 
     * <p>
     * Note that maxUnits must include overhead bytes (2 for the address field
     * and control field if Address-Control-Field-Compression is not enabled,
     * 2/4 for the Frame-Checksum-Field, and at least 1 data byte).
     * 
     * @param maxUnits
     * @throws IllegalArgumentException
     *             if maxUnits is less than required min.
     */
    public Frame(int maxUnits, boolean acfcEnabled, int fcsLength,
            AsyncControlCharMap accm) throws IllegalArgumentException {

        int headerLength = acfcEnabled ? 0 : 2;

        if(!(fcsLength == 2 || fcsLength == 4))
            throw new IllegalArgumentException("Invalid fcsLength");

        if(maxUnits < (1 + headerLength + fcsLength))
            throw new IllegalArgumentException("Invalid maxUnits size");

        if(accm == null)
            throw new IllegalArgumentException("Invalid ACCM");

        this.maxUnits = maxUnits;
        this.data = new int[maxUnits];
        this.dataPtr = 0;
        this.acfcEnabled = acfcEnabled;
        this.fcsLength = fcsLength;
        this.accm = accm;
    }

    /**
     * Construct an empty frame using default values:
     * <ul>
     * <li>Max Units = 1500</li>
     * <li>ACFC Disabled</li>
     * <li>FCS Length = 2</li>
     * </ul>
     */
    public Frame() {
        this(1500, false, 2, new AsyncControlCharMap());
    }

    /**
     * Add a byte value to the Frame's payload. Note that the value of
     * <code>payloadByte</code> is silently truncated to the range (0-255).
     * 
     * @throws IndexOutOfBoundsException
     *             if payload exceeds maxUnits available to the Frame.
     */
    public void addPayload(int payloadByte) throws IndexOutOfBoundsException {

        if(this.dataPtr >= this.maxUnits)
            throw new IndexOutOfBoundsException("Payload exceeds maxUnits "
                    + "available to Frame");

        this.data[this.dataPtr++] = (payloadByte & 0xFF);
    }

    /**
     * Add an array of raw byte values to the Frame's payload. Note that the
     * values of <code>payloadBytes</code> are silently truncated to the range
     * (0-255).
     * 
     * @throws IndexOutOfBoundsException
     *             if payload exceeds maxUnits available to the Frame.
     */
    public void addPayload(int[] payloadBytes) throws IndexOutOfBoundsException {

        if((this.dataPtr + payloadBytes.length) >= this.maxUnits)
            throw new IndexOutOfBoundsException("Payload exceeds max units "
                    + "available to Frame");

        for(int dbyte : payloadBytes) {
            this.data[this.dataPtr++] = (dbyte & 0xFF);
        }
    }

    /**
     * Returns the address of the Frame.
     * 
     * @return <code>address</code> if valid; <code>-1</code> otherwise.
     */
    public int getAddress() {
        if(!this.acfcEnabled && this.dataPtr > 0) {
            return data[0];
        } else {
            return -1;
        }
    }

    /**
     * Sets the address of the Frame. If ACFC is enabled does nothing.
     * 
     * @param address
     *            Byte value of address field (truncated to 0-255).
     */
    public void setAddress(int address) {
        if(!this.acfcEnabled) {
            this.data[0] = (address & 0xff);
        }
    }

    /**
     * Returns the control field of the Frame.
     * 
     * @return <code>control</code> if valid; <code>-1</code> otherwise.
     */
    public int getControl() {
        if(!acfcEnabled && this.dataPtr > 1) {
            return this.data[1];
        } else {
            return -1;
        }
    }

    /**
     * Sets the control field of the Frame. If ACFC is enabled does nothing.
     * 
     * @param address
     *            Byte value of control field (truncated to 0-255).
     */
    public void setControl(int control) {
        if(!this.acfcEnabled) {
            this.data[0] = (control & 0xff);
        }
    }

    /**
     * Calculates the fast Frame Checksum as described in section C.2 of
     * RFC-1662.
     * 
     * @return 16-bit unsigned frame check sum
     */
    private int calcFrameChecksum16() {
        int fcs = 0xFFFF;
        for(int i = 0; i < this.dataPtr; i++) {
            if(this.data[i] == ESC_VALUE) {
                fcs = lookupFrameChecksum(fcs, this.data[++i] ^ ESC_MASK);
            } else {
                fcs = lookupFrameChecksum(fcs, this.data[i]);
            }
        }
        return (fcs & 0xFFFF);
    }

    /**
     * Calculates a single round of the fast Frame Checksum
     */
    private static int lookupFrameChecksum(int fcs, int dbyte) {
        return ((fcs >>> 8) ^ FCS16TABLE[(fcs ^ dbyte) & 0xFF]);
    }

    /**
     * Evaluates frame data to determine if this object contains a valid data
     * frame
     * 
     * @return True if frame is valid
     */
    public boolean isValid() {

        if(!this.dataContainsErrors()) {
            if(this.fcsLength == 2) {
                return (this.calcFrameChecksum16() == GOODFCS16);
            } else if(this.fcsLength == 4) {
                throw new UnsupportedOperationException();
            }
        }

        return false;
    }

    /**
     * Runs common checks for errors in the frame data stream
     * 
     * @return true if data contains errors
     */
    private boolean dataContainsErrors() {

        boolean escFlag = false;

        for(int i = 0; i < this.dataPtr; i++) {

            // Look for FLAGS in data - a single one indicates an error and
            // causes us to discard the frame
            if(this.data[i] == FLAG_VALUE) {
                return true;
            }

            // Look for more than one escape character in a row - this also
            // indicates an error
            if(this.data[i] == ESC_VALUE) {
                if(escFlag) {
                    return true;
                } else {
                    escFlag = true;
                }
            } else {
                escFlag = false;
            }
        }

        return false;
    }

    /**
     * Returns the data payload of the frame (i.e. data with escape characters
     * removed). If the frame is not complete or is not valid returns an empty
     * array.
     */
    public int[] getDataPayload() {

        // Verify that data is valid
        if(!this.isValid())
            return new int[0];

        // Replace special characters and characters in ACCM
        int readPtr = 0;
        int writePtr = 0;
        int[] payload = Arrays.copyOf(this.data, this.dataPtr);
        while(readPtr < (this.dataPtr)) {
            if(payload[readPtr] == ESC_VALUE) {
                payload[writePtr++] = payload[++readPtr] ^ ESC_MASK;
                readPtr++;
            } else if(this.accm.isInACCM(payload[readPtr])) {
                readPtr++;
            } else {
                payload[writePtr++] = payload[readPtr++];
            }
        }
        return Arrays.copyOfRange(payload, this.acfcEnabled ? 0 : 2, writePtr
                - this.fcsLength);
    }
}

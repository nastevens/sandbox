package com.qiggroup.javappp.protocol;

import java.util.EventListener;

public interface LinkEventListener extends EventListener {

    void linkLowerUp();

    void linkLowerDown();

    void linkOpen();

    void linkClose();

    void linkTimeout();

    void linkRcvdData();
}

package com.bitcurry.wherever.model;

/**
 * Created by nickstevens on 4/9/14.
 */
public class Rsvp {

    public static enum RsvpType {
        ACCEPT, TENTATIVE, DECLINE
    }

    private RsvpType type;
    private User user;
}

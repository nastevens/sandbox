package com.bitcurry.wherever.model;

import java.util.Date;
import java.util.List;

/**
 *
 */
public class Meal {

    public static enum Visibility {
        GROUP, ALL, CUSTOM
    }

    public static enum MealState {
        OPEN, CANCELLED
    }

    private Date date;
    private Visibility visibility;
    private User owner;
    private List<Vote> votes;
    private MealState state;
}


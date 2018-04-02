package com.bitcurry.wherever.model;


import org.hibernate.annotations.GenericGenerator;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;
import java.net.URL;

/**
 *
 */


@Entity
@Table(name="locations")
public class Location {

    private Long id;
    private String name;
    private URL businessUrl;
    private URL yelpUrl;

    public Location() { }

    public Location(String name, URL businessUrl, URL yelpUrl) {
        this.name = name;
        this.businessUrl = businessUrl;
        this.yelpUrl = yelpUrl;
    }

    @Id
    @GeneratedValue
    public Long getId() {
        return id;
    }

    private void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Column(name="business_url")
    public URL getBusinessUrl() {
        return businessUrl;
    }

    public void setBusinessUrl(URL businessUrl) {
        this.businessUrl = businessUrl;
    }

    @Column(name="yelp_url")
    public URL getYelpUrl() {
        return yelpUrl;
    }

    public void setYelpUrl(URL yelpUrl) {
        this.yelpUrl = yelpUrl;
    }
}

package com.demoblaze.api;

import com.intuit.karate.junit5.Karate;

public class ApiRunner {

    @Karate.Test
    Karate testAll() {
        return Karate.run().relativeTo(getClass());
    }

    @Karate.Test
    Karate testSignup() {
        return Karate.run("signup/signup").relativeTo(getClass());
    }

    @Karate.Test
    Karate testLogin() {
        return Karate.run("login/login").relativeTo(getClass());
    }
}


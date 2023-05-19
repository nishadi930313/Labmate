package com.example.myapplication;

import com.google.gson.annotations.SerializedName;

public class ApiResponse {

    @SerializedName("code")
    private int code;

    @SerializedName("message")
    private String message;

    @SerializedName("result")
    private String result;

    public int getCode() {
        return code;
    }

    public String getMessage() {
        return message;
    }

    public String getResult() {
        return result;
    }
}

package com.example.myapplication;

import retrofit2.Call;
import retrofit2.http.POST;

public interface MyApiService {
    @POST("/user/response")
    Call<ApiResponse> sendRequest();
}

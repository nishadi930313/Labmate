package com.example.mylogin;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class LoginActivity extends AppCompatActivity {

    private EditText et_email, et_pwd;
    private ServiceApi service;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        et_email = (EditText) findViewById(R.id.login_et_email);
        et_pwd = (EditText) findViewById(R.id.login_et_pwd);
        service = RetrofitClient.getClient().create(ServiceApi.class);

        Button btn_login = (Button) findViewById(R.id.login_btn_login);
        Button btn_join = (Button) findViewById(R.id.login_btn_join);

        btn_login.setOnClickListener(v -> attemptLogin());
        btn_join.setOnClickListener(view -> {
            Intent intent = new Intent(getApplicationContext(), JoinActivity.class);
            Log.e("JoinActivity", "JoinActivity");
            startActivity(intent);
        });
    }


    private void attemptLogin() {
        et_email.setError(null);
        et_pwd.setError(null);

        String email = et_email.getText().toString();
        String pwd = et_pwd.getText().toString();

        if (email.isEmpty()) {
            et_email.setError("Empty Email");
            et_email.requestFocus();
            return;
        }

        if (pwd.isEmpty()) {
            et_pwd.setError("Empty Password");
            et_pwd.requestFocus();
            return;
        }

        startLogin(new LoginData(email, pwd));
    }

    private void startLogin(LoginData data) {
        //Toast.makeText(LoginActivity.this, "startLogin", Toast.LENGTH_SHORT).show();
        service.userLogin(data).enqueue(new Callback<LoginResponse>() {
            @Override
            public void onResponse(Call<LoginResponse> call, Response<LoginResponse> response) {
                LoginResponse result = response.body();
                Toast.makeText(LoginActivity.this, result.getMessage(), Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onFailure(Call<LoginResponse> call, Throwable t) {
                Toast.makeText(LoginActivity.this, "Login Error", Toast.LENGTH_SHORT).show();
                Log.e("Login Error", t.getMessage());
            }
        });
    }
}
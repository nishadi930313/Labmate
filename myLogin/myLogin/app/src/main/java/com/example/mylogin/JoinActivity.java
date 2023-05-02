package com.example.mylogin;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class JoinActivity extends AppCompatActivity {

    private EditText et_name, et_email, et_pwd;
    private ServiceApi service;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_join);

        et_name = (EditText) findViewById(R.id.join_et_name);
        et_email = (EditText) findViewById(R.id.join_et_email);
        et_pwd = (EditText) findViewById(R.id.join_et_pwd);
        service = RetrofitClient.getClient().create(ServiceApi.class);

        Button btn_join = (Button) findViewById(R.id.join_btn_join);

        btn_join.setOnClickListener(v -> attemptJoin());


    }

    private void attemptJoin() {
        et_name.setError(null);
        et_email.setError(null);
        et_pwd.setError(null);

        String name = et_name.getText().toString();
        String email = et_email.getText().toString();
        String pwd = et_pwd.getText().toString();

        if (name.isEmpty()) {
            et_name.setError("Empty Name");
            et_name.requestFocus();
            return;
        }

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

        startJoin(new JoinData(name, email, pwd));

    }

    private void startJoin(JoinData data) {
        service.userJoin(data).enqueue(new Callback<JoinResponse>() {
            @Override
            public void onResponse(Call<JoinResponse> call, Response<JoinResponse> response) {
                JoinResponse result = response.body();
                Toast.makeText(JoinActivity.this, result.getMessage(), Toast.LENGTH_SHORT).show();

                if (result.getCode() == 200) {
                    finish();
                }
            }

            @Override
            public void onFailure(Call<JoinResponse> call, Throwable t) {
                Toast.makeText(JoinActivity.this, "Join Error", Toast.LENGTH_SHORT).show();
                Log.e("Join Error", t.getMessage());
            }
        });
    }

}

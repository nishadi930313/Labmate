package com.example.myapplication;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import com.example.myapplication.R;
import com.example.myapplication.ApiResponse;
import com.example.myapplication.MyApiService;
import com.example.myapplication.R;
import com.example.myapplication.RetrofitClient;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;

public class MainActivity extends AppCompatActivity {

    private Button button;
    private MyApiService apiService;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Retrofit 인스턴스 생성
        Retrofit retrofit = RetrofitClient.getClient();
        // MyApiService 인터페이스를 사용하여 API 호출
        apiService = retrofit.create(MyApiService.class);

        button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // 서버에 요청 보내기
                sendRequestToServer();
            }
        });
    }

    private void sendRequestToServer() {
        // 서버 API 호출
        Call<ApiResponse> call = apiService.sendRequest();

        call.enqueue(new Callback<ApiResponse>() {
            @Override
            public void onResponse(Call<ApiResponse> call, Response<ApiResponse> response) {
                if (response.isSuccessful()) {
                    ApiResponse apiResponse = response.body();
                    // 응답 처리
                    if (apiResponse != null) {
                        String result = apiResponse.getMessage();
                        Toast.makeText(MainActivity.this, "서버 응답: " + result, Toast.LENGTH_SHORT).show();
                        TextView text1 = findViewById(R.id.textView9);
                        text1.setText(result);


                    }
                } else {
                    Toast.makeText(MainActivity.this, "서버 응답 실패", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<ApiResponse> call, Throwable t) {
                Toast.makeText(MainActivity.this, "요청 실패: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}
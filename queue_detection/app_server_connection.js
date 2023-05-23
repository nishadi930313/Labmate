const mysql = require('mysql');
const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.set("port", port);
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(port, () => {
    console.log('Server Runnning...');
});

const connection = mysql.createConnection({
    host: "muc.cyzbfaoq6z0b.eu-north-1.rds.amazonaws.com",
    user: "admin",
    database: "example",
    password: "mucadmin",
    port: 3306
});

app.post('/user/join', (req, res) => {
    console.log(req.body);
    const userEmail = req.body.userEmail;
    const userPwd = req.body.userPwd;
    const userName = req.body.userName;

    const sql = 'INSERT INTO Users (UserEmail, UserPwd, UserName) VALUES (?, ?, ?)';
    const params = [userEmail, userPwd, userName];

    connection.query(sql, params, (err, result) => {
        let resultCode = 404;
        let message = 'Error occured';

        if (err) {
            console.log(err);
        } else {
            resultCode = 200;
            message = 'User created!';
            console.log(message);
        }

        res.json({
            'code': resultCode,
            'message': message
        });
    });
});

app.post('/user/login', (req, res) => {
    const userEmail = req.body.userEmail;
    const userPwd = req.body.userPwd;
    const sql = 'select * from Users where UserEmail = ?';

    connection.query(sql, userEmail, (err, result) => {
        let resultCode = 404;
        let message = 'Error occured';

        if (err) {
            console.log(err);
        } else {
            if (result.length === 0) {
                resultCode = 204;
                message = 'Id does not exist';
            } else if (userPwd !== result[0].UserPwd) {
                resultCode = 204;
                message = 'Incorrect password';
            } else {
                resultCode = 200;
                message = 'Login Success! Welcome ' + result[0].UserName;
            }
            console.log(message);
        }

        res.json({
            'code': resultCode,
            'message': message,
        });
    })
});

// retreives most recent inference result of number of people in queue from RDS Inferences table (returns -1 if an error occurs)
app.post('/inference', (req, res) => {
        const sql = 'SELECT numpeople FROM Inferences ORDER BY dt DESC LIMIT 1';
        connection.query(sql, function (err, result)  {
                let resultCode = 404;
                let numpeople = -1;
                if (err) {
                        console.log(err);
                } else {
                        if (result.length === 0) {
                                resultCode = 204;

                                numpeople = -1;
                        } else {
                                resultCode = 200;
                                numpeople = result[0].numpeople;
                        }
                }
                console.log('number of people retrieved:', numpeople);
                res.json({
                        'code': resultCode,
                        'numpeople': numpeople,
                });
        })
});

const {PythonShell } = require('python-shell');
        const scriptPath = 'random_int.py';
        const options = {
                pythonPath:'python3'
        };
    
app.post('/user/response', (req, res) => {
        let resultCode = 404;
        var message = 'Response from the server';
        message="Inference testing";
//
        //message =Math.random();
        const {PythonShell} = require('python-shell');
        const scriptPath = 'print.py';
        const options = {
                pythonPath:'python3'
        };
        console.log("this is before running the python script");
        PythonShell.run(scriptPath,options, (err,results) => {
                if(err) {
                        console.error(err);
                        return;
                }

                message=results[0];
                console.log(message);
                console.log("this is during running the python script");
        })
        console.log("this is after running the python script");
        /*var spawn=require('child_process').spawn;
        const result=spawn('py',['./print.py']);
        result.stdout.on('data',function(data) {
                console.log(data.toString());
        });
        result.stderr.on('data',function(data) {
                console.og(data.toString());
        })
        message=data.toString();
*/      console.log(message);
        res.json({
                'code':resultCode,
                'message': message,
        });
});

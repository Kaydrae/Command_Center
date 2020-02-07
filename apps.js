var app = require('express');
var app1 = app();
var http = require('http').Server(app1);
var io = require('socket.io')(http);


app1.use(app.static(__dirname));

app1.get('/', function(req, res) {
    res.sendFile(__dirname + '/index.html');
});

io.on('connection', function (socket) {
    console.log('A user connected');
});

http.listen(3000, function() {
    console.log('listening on localhost:3000');
});
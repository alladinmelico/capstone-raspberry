$(document).ready(function(){
    const socket = io.connect('http://localhost:5000')
    socket.on("connect", function () {
        console.log('connect...')
      socket.emit("my event", { data: "I'm connected!" })
    })
    
    socket.on('after connect', function(msg){
        console.log('After connect', msg);
    });

    socket.on('my response', function(msg){
       console.log('After connect', msg);
    });
})

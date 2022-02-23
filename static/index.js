$(document).ready(function () {
  const profile = document.querySelector("#profile")
  const schoolId = document.querySelector("#school-id")
  const username = document.querySelector("#username")
  const startTime = document.querySelector("#start-time")
  const endTime = document.querySelector("#end-time")
  const socket = io.connect('http://localhost:5000')
  
  socket.on('connect', function() {
      console.log('connect...')
      socket.emit('my event', {data: 'connected'})
  })
  
  socket.on('after connect', function(msg) {
      console.log('after connect', msg)
  })
  
  socket.on('my response', function(msg) {
      console.log('my response', msg)
  })
})

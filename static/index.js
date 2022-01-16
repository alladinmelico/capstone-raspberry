$(document).ready(function () {
  const profile = document.querySelector("#profile")
  const schoolId = document.querySelector("#school-id")
  const username = document.querySelector("#username")
  const startTime = document.querySelector("#start-time")
  const endTime = document.querySelector("#end-time")
  setInterval(() => {
    fetch("/check")
      .then((response) => response.json())
      .then((data) => console.log('data', data))
      .catch(error => {
        console.error('Error:', error);
      });
  }, 100)
})

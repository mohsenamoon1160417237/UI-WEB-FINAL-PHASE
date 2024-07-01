let csrfToken = document.cookie.split("csrftoken=")[1].split(";")[0]

const loginForm = document.getElementById('loginForm');

loginForm.addEventListener('submit', function(event) {
  event.preventDefault();

  const username2 = document.getElementById('username2').value;
  const password2 = document.getElementById('password2').value;
    const data = {
      username: username2,
      password: password2
    }

    const jsonData = JSON.stringify(data);
    const xhr = new XMLHttpRequest();

    xhr.open('POST', 'http://127.0.0.1:8000/login/');

    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);

    xhr.send(jsonData);

    xhr.onload = () => {
      if (xhr.status === 200) {
          // The request was successful
        console.log('Data sent successfully');
        window.location.href = "http://127.0.0.1:8000/";
      } else {
          // The request failed
        console.error('Error sending data');
      }
    };
});
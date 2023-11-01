document.getElementById("list-clear").addEventListener("click", function () {
    fetch('/cart/delete/', {
      method: 'DELETE'
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log(data);
      window.location.reload();
    }) 
    .catch(error => console.error('Error:', error));
  })
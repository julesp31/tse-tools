// Target the buttons and the container
const textContainer = document.querySelector('.text-container');
const heroBanner = document.querySelector('.hero');
const btnOne = document.querySelector('.btn-one');
const btnTwo = document.querySelector('.btn-two');

// Add click event listeners
btnOne.addEventListener('click', () => {
  textContainer.style.marginLeft = '250px'; // Move the text container
  textContainer.style.marginRight = '10px';
  heroBanner.style.marginLeft = '240px';
});

btnTwo.addEventListener('click', () => {
  textContainer.style.marginLeft = '10px'; // Reset the text container
  heroBanner.style.marginLeft = '0px';
});

document.getElementById("generate-btn").addEventListener("click", function () {
  const inputText = document.getElementById("input-text").value;

  fetch("/process", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text: inputText })
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById("output-text").value = JSON.stringify(data, null, 2);

      // Trigger the focus event on the output textarea to move the label
      const outputTextarea = document.getElementById("output-text");
      outputTextarea.focus();

      // Keep the label and border in the moved position
      const outputArea = document.querySelector('.output-area');
      outputArea.classList.add('focused');  // Add a class to indicate focus state
    })
    .catch(error => {
      console.error("Error:", error);
    });
});



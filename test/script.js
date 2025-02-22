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
  
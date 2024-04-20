const imageContainer = document.querySelector('.image-container');
const prevBtn = document.querySelector('.prev');
const nextBtn = document.querySelector('.next');
let currentImage = 0;

function showImage() {
  imageContainer.style.transform = `translateX(-${currentImage * 100}%)`;
}

prevBtn.addEventListener('click', () => {
  currentImage--;
  if (currentImage < 0) {
    currentImage = imageContainer.children.length - 1; 
  }
  showImage();
});

nextBtn.addEventListener('click', () => {
  currentImage++;
  if (currentImage >= imageContainer.children.length) {
    currentImage = 0; 
  }
  showImage();
});

showImage(); // Показать первое изображение при загрузке
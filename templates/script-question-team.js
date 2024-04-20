const modal = document.getElementById('modal');
const openModalBtn = document.getElementById('openModal');
const closeBtn = document.getElementsByClassName('close')[0];

openModalBtn.addEventListener('click', function() {
  modal.style.display = 'block';
});

closeBtn.addEventListener('click', function() {
  modal.style.display = 'none';
});

window.addEventListener('click', function(event) {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
});

const form = document.getElementById('questionForm');
form.addEventListener('submit', function(event) {
  event.preventDefault();
  
  // Добавьте здесь код для обработки отправки формы, например отправку данных на сервер
});
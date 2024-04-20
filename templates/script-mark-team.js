const openPopupBtn = document.getElementById('openPopupBtn');
const evaluationPopup = document.getElementById('evaluationPopup');

openPopupBtn.addEventListener('click', () => {
  evaluationPopup.style.display = 'block';
});

function closePopup() {
  evaluationPopup.style.display = 'none';
}

const evaluationForm = document.getElementById('evaluationForm');
evaluationForm.addEventListener('submit', (e) => {
  e.preventDefault();
  
  const design = parseInt(evaluationForm.elements.design.value);
  const usability = parseInt(evaluationForm.elements.usability.value);
  const coding = parseInt(evaluationForm.elements.coding.value);
  
  // Логика для обработки оценок
  
  closePopup();
});


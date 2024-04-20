// Получаем элемент input по его ID
const emailInput = document.getElementById('email');

// Функция для проверки корректности адреса электронной почты
function validateEmail(email) {
    // Регулярное выражение для проверки email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Добавляем обработчик события "input" к элементу input
emailInput.addEventListener('input', function() {
    // Получаем введенный email
    const email = emailInput.value;

    // Проверяем email на корректность
    if (validateEmail(email)) {
        // Если email корректный, делаем что-то (например, показываем сообщение об успехе)
        console.log('Email введен корректно.');
        emailInput.style.borderColor = 'green';
    } else {
        // Если email некорректный, показываем сообщение об ошибке
        console.log('Некорректный адрес электронной почты.');
        emailInput.style.borderColor = 'red';
    }
});

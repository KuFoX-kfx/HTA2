function previewImage(event) {
    const image = document.getElementById('profileImage');
    image.src = URL.createObjectURL(event.target.files[0]);
}

function saveChanges() {
    const teamName = document.getElementById('teamName').value;
    const teamInfo = document.getElementById('teamInfo').value;
    const teamMembers = document.getElementById('teamMembers').value;
    const newPassword = document.getElementById('password').value;

    // Здесь можно отправить данные на сервер для сохранения или обработки
    console.log('Название команды:', teamName);
    console.log('Информация о команде:', teamInfo);
    console.log('Участники команды:', teamMembers);
    console.log('Новый пароль:', newPassword);

    alert('Изменения сохранены успешно!');
}

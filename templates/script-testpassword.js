function checkPasswordStrength(password) {
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecialChar = /[^A-Za-z0-9]/.test(password);

    if (hasUppercase && hasLowercase && hasNumber && hasSpecialChar) {
        return 'Пароль сильный';
    } else {
        return 'Пароль должен содержать хотя бы одну заглавную букву, строчную букву, цифру и специальный символ';
    }
}


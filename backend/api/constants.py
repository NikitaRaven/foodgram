NOT_DICT_INGREDIENT: str = 'Каждый ингредиент должен быть словарем.'
NO_KEYS: str = 'Каждый ингредиент должен содержать ключи id и amount.'
BELOW_ZERO: str = 'Количество должно быть больше 0.'
ABOVE_MAX: str = 'Введена слишком большая величина.'
DUPLICATE_ID: str = 'У некоторых ингредиентов обнаружен одинаковый id:'
MAX_AMOUNT: int = 2147483647

SHOPPING_CONTENT: str = 'attachment; filename="ingredients.txt"'
NOT_FOUND_FAVORITE: str = 'Рецепт не является избанным.'
NOT_FOUND_SHOPPING: str = 'Рецепт не найден в корзине для покупок.'

SUB_YOURSELF: str = 'Нельзя подписаться на самого себя.'

SUB_NOT_FOUND: str = 'Подписка не найдена.'

INVALID_USERNAME: str = (
    'В имени пользователя допускаются буквы алфафвита, цифры и @, ., +.'
)
DUPLICATE_USERNAME: str = 'Пользователь с таким именем уже есть.'
COMMON_PASSWORDS: set[str] = {
    '123456', 'password', '123456789', '12345678', '12345', '1234567',
    'qwerty', 'abc123', 'football', 'monkey', 'letmein', '111111', 'iloveyou',
    'admin', 'welcome', '123123', 'qwerty123', '1q2w3e4r', 'password1'
}
PASSWORD_USERNAME: str = 'Пароль должен быть непохож на юзернейм.'
PASSWORD_LENGTH: int = 8
SHORT_PASSWORD: str = 'В пароле должно быть как минимум 8 символов.'
TOO_COMMON: str = (
    'Пароль не может быть одним из широко распространённых паролей.'
)
ONLY_DIGITS: str = 'Пароль не может состоять только из цифр.'
INVALID_PASSWORD: str = 'Введенный пароль не верен.'
SAME_PASSWORD: str = 'Новый пароль не должен совпадать с текущим.'

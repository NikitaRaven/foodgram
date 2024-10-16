TAG_NAME_LENGTH: int = 32
VERBOSE_NAME_TAG: str = 'название'
VERBOSE_SLUG_TAG: str = 'слаг'
TAG_VERBOSE: str = 'тэг'
TAG_VERBOSE_PLURAL: str = 'тэги'

INGREDIENT_NAME_LENGTH: int = 128
INGREDIENT_UNIT_LENGTH: int = 64
VERBOSE_NAME_INGREDIENT: str = 'название'
VERBOSE_UNIT_INGREDIENT: str = 'единица измерения'
INGREDIENT_VERBOSE: str = 'ингредиент'
INGREDIENT_VERBOSE_PLURAL: str = 'ингредиенты'

RECIPE_NAME_LENGTH: int = 256
RECIPE_TIME_MIN: int = 1
RECIPE_TIME_MAX: int = 2147483647
RECIPE_LINK_LENGTH: int = 4
VERBOSE_AUTHOR_RECIPE: str = 'автор'
VERBOSE_INGREDIENTS_RECIPE: str = 'ингредиенты'
VERBOSE_TAGS_RECIPE: str = 'тэги'
VERBOSE_IMAGE_RECIPE: str = 'изображение'
VERBOSE_NAME_RECIPE: str = 'название'
VERBOSE_TEXT_RECIPE: str = 'описание'
VERBOSE_TIME_RECIPE: str = 'время приготовления'
VERBOSE_LINK_RECIPE: str = 'короткая ссылка'
VERBOSE_DATE_RECIPE: str = 'дата создания рецепта'
RECIPE_VERBOSE: str = 'рецепт'
RECIPE_VERBOSE_PLURAL: str = 'рецепты'
TIME_LOW: str = (
    f'Время приготовления должно быть не менее {RECIPE_TIME_MIN} минуты.'
)
TIME_HIGH: str = (
    f'Время приготовления не может превышать {RECIPE_TIME_MAX} минут.'
)

RI_AMOUNT_MIN: int = 1
RI_AMOUNT_MAX: int = 2147483647
VERBOSE_RECIPE_RI: str = 'рецепт'
VERBOSE_INGREDIENT_RI: str = 'ингредиент'
VERBOSE_AMOUNT_RI: str = 'количество'
RI_VERBOSE: str = 'рецепт-ингредиент'
RI_VERBOSE_PLURAL: str = 'рецепты-ингредиенты'
AMOUNT_LOW: str = f'Количество должно быть не менее {RI_AMOUNT_MIN}.'
AMOUNT_HIGH: str = f'Количество не может превыфшать {RI_AMOUNT_MAX}.'

VERBOSE_USER_FAVORITE: str = 'пользователь'
VERBOSE_RECIPE_FAVORITE: str = 'рецепт'
FAVORITE_VERBOSE: str = 'избранный рецепт'
FAVORITE_VERBOSE_PLURAL: str = 'избранные рецепты'

ADMIN_NO_INGREDIENTS: str = 'Необходимо добавить хотя бы один ингредиент.'

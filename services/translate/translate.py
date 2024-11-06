def transliterate_text(text):
    transliteration_map = {
        'Ў': 'O\'', 'Қ': 'Q', 'Ғ': 'G\'', 'Ш': 'SH', 'Ч': 'CH', 'Ҳ': 'H',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO', 'Ж': 'J',
        'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
        'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'X', 'Ц': 'TS',
        'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'YU',
        'Я': 'YA'
    }

    def transliterate(text):
        result = ''
        for char in text:
            result += transliteration_map.get(char, char)
        return result

    return transliterate(text)

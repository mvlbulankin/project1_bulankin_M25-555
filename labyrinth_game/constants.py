SINE_MULTIPLIER = 12.9898
HASH_MULTIPLIER = 43758.5453
EVENT_PROBABILITY = 10
EVENT_TYPES = 3
DAMAGE_MODULO = 10
DAMAGE_THRESHOLD = 3

COMMANDS = {
    'go <direction>': 'перейти в направлении (north/south/east/west)',
    'look': 'осмотреть текущую комнату',
    'take <item>': 'поднять предмет',
    'use <item>': 'использовать предмет из инвентаря',
    'inventory': 'показать инвентарь',
    'solve': 'попытаться решить загадку в комнате',
    'quit': 'выйти из игры',
    'help': 'показать это сообщение',
}

ROOMS = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта...',
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': ('Большой зал с эхом. '
                        'По центру стоит пьедестал с запечатанным сундуком.'),
        'exits': {'south': 'entrance', 'west': 'library', 'north': 'treasure_room'},
        'items': [],
        'puzzle': (('На пьедестале надпись: '
                    '"Назовите число, которое идет после девяти". '
                    'Введите ответ цифрой или словом.'), '10')
    },
    'trap_room': {
          'description': ('Комната с хитрой плиточной поломкой. '
                          'На стене видна надпись: "Осторожно — ловушка".'),
          'exits': {'west': 'entrance'},
          'items': ['rusty_key'],
          'puzzle': (('Система плит активна. '
                      'Чтобы пройти, назовите слово "шаг" три раза подряд '
                      '(введите "шаг шаг шаг")'), 'шаг шаг шаг')
    },
    'library': {
          'description': ('Пыльная библиотека. '
                          'На полках старые свитки. '
                          'Где-то здесь может быть ключ от сокровищницы.'),
          'exits': {'east': 'hall', 'north': 'armory'},
          'items': ['ancient book'],
          'puzzle': (('В одном свитке загадка: '
                      '"Что растет, когда его съедают?" (ответ одно слово)'),
                      'резонанс')
    },
        'armory': {
          'description': ('Старая оружейная комната. '
                          'На стене висит меч, рядом — небольшая бронзовая шкатулка.'),
          'exits': {'south': 'library'},
          'items': ['sword', 'bronze box'],
          'puzzle': None
    },
    'treasure_room': {
          'description': ('Комната, на столе большой сундук. '
                          'Дверь заперта — нужен особый ключ.'),
          'exits': {'south': 'hall'},
          'items': ['treasure_chest'],
          'puzzle': (('Дверь защищена кодом. Введите код '
                      '(подсказка: это число пятикратного шага, 2*5= ? )'), '10')
    },
    'secret_chamber': {
        'description': ('Тайная комната с древними рунами на стенах. '
                        'Здесь тихо и загадочно.'),
        'exits': {'south': 'treasure_room'},
        'items': ['treasure_key'],
        'puzzle': ('Руны шепчут: "Сколько углов у круга?" (ответ цифрой)', '0')
    },
    'dungeon': {
        'description': ('Темница с цепями и скелетами. '
                        'Кажется, здесь были заключены узники.'),
        'exits': {'east': 'library'},
        'items': ['old map'],
        'puzzle': None
    }
}

import math

from .constants import (
    DAMAGE_MODULO,
    DAMAGE_THRESHOLD,
    EVENT_PROBABILITY,
    EVENT_TYPES,
    HASH_MULTIPLIER,
    ROOMS,
    SINE_MULTIPLIER,
)


def pseudo_random(seed, modulo):
    '''Generate a pseudo-random integer between 0 and modulo-1 using sine function.'''
    x = math.sin(seed * SINE_MULTIPLIER) * HASH_MULTIPLIER
    frac = x - math.floor(x)
    return math.floor(frac * modulo)


def trigger_trap(game_state):
    '''Trigger a trap event that may cause loss of items or game over.'''
    print('Ловушка активирована! Пол стал дрожать...')
    inventory = game_state['player_inventory']
    steps = game_state['steps_taken']
    if inventory:
        modulo = len(inventory)
        idx = pseudo_random(steps, modulo)
        lost_item = inventory.pop(idx)
        print(f'Вы потеряли: {lost_item}')
    else:
        damage = pseudo_random(steps, DAMAGE_MODULO)
        if damage < DAMAGE_THRESHOLD:
            print('Вы не смогли выбраться... Игра окончена.')
            game_state['game_over'] = True
        else:
            print('Вы уцелели, но это было близко.')


def random_event(game_state):
    '''Trigger a random event after moving to a new room.'''
    steps = game_state['steps_taken']
    if pseudo_random(steps, EVENT_PROBABILITY) == 0:
        event_type = pseudo_random(steps + 1, EVENT_TYPES)
        current_room = game_state['current_room']
        inventory = game_state['player_inventory']
        if event_type == 0:
            print('Вы нашли монетку на полу!')
            ROOMS[current_room]['items'].append('coin')
        elif event_type == 1:
            print('Вы слышите шорох в темноте...')
            if 'sword' in inventory:
                print('Вы отпугнули существо мечом!')
        elif event_type == 2:
            if current_room == 'trap_room' and 'torch' not in inventory:
                print('Опасность! Ловушка срабатывает из-за темноты.')
                trigger_trap(game_state)


def describe_current_room(game_state):
    '''Describe the current room, including items, exits, and puzzles.'''
    room_name = game_state['current_room']
    room = ROOMS[room_name]
    print(f'== {room_name.upper()} ==')
    print(room['description'])
    if room['items']:
        print('Заметные предметы:')
        for item in room['items']:
            print(f' - {item}')
    print('Выходы:', ', '.join(room['exits'].keys()))
    if room['puzzle']:
        print('Кажется, здесь есть загадка (используйте команду solve).')


def solve_puzzle(game_state, get_input):
    '''Attempt to solve the puzzle in the current room.'''
    current_room = game_state['current_room']
    puzzle = ROOMS[current_room]['puzzle']
    if not puzzle:
        print('Загадок здесь нет.')
        return
    question, answer = puzzle
    print(question)
    user_answer = get_input('Ваш ответ: ')
    correct = False
    if answer == '10':
        correct = user_answer in ['10', 'десять']
    else:
        correct = user_answer == answer
    if correct:
        print('Верно! Вы решили загадку.')
        ROOMS[current_room]['puzzle'] = None
        inventory = game_state['player_inventory']
        if current_room == 'hall':
            if 'treasure_key' not in inventory:
                inventory.append('treasure_key')
                print('Вы получили treasure_key как награду.')
        elif current_room == 'library':
            if 'rusty_key' not in inventory:
                inventory.append('rusty_key')
                print('Вы получили rusty_key как награду.')
    else:
        print('Неверно. Попробуйте снова.')
        if current_room == 'trap_room':
            trigger_trap(game_state)


def attempt_open_treasure(game_state, get_input):
    '''Attempt to open the treasure chest in the treasure room.'''
    current_room = game_state['current_room']
    if current_room != 'treasure_room':
        return
    items = ROOMS[current_room]['items']
    inventory = game_state['player_inventory']
    if 'treasure_key' in inventory:
        print('Вы применяете ключ, и замок щёлкает. Сундук открыт!')
        if 'treasure_chest' in items:
            items.remove('treasure_chest')
        print('В сундуке сокровище! Вы победили!')
        game_state['game_over'] = True
        return
    response = get_input('Сундук заперт. Ввести код? (да/нет): ')
    if response == 'да':
        puzzle = ROOMS[current_room]['puzzle']
        if puzzle:
            question, answer = puzzle
            print(question)
            code = get_input('Введите код: ')
            correct = False
            if answer == '10':
                correct = code in ['10', 'десять']
            else:
                correct = code == answer
            if correct:
                print('Верно! Сундук открыт.')
                if 'treasure_chest' in items:
                    items.remove('treasure_chest')
                print('В сундуке сокровище! Вы победили!')
                game_state['game_over'] = True
            else:
                print('Неверный код.')
        else:
            print('Нет загадки для кода.')
    else:
        print('Вы отступаете от сундука.')


def show_help(commands):
    '''Display the list of available commands.'''
    print('\nДоступные команды:')
    for cmd, desc in commands.items():
        print(f'{cmd.ljust(16)} - {desc}')

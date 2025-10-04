from .constants import ROOMS
from .utils import describe_current_room, random_event


def get_input(prompt='> '):
    '''Get user input with handling for interruptions.'''
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print('\nВыход из игры.')
        return 'quit'


def show_inventory(game_state):
    '''Display the player's inventory.'''
    inventory = game_state['player_inventory']
    if inventory:
        print('Ваш инвентарь:')
        for item in inventory:
            print(f' - {item}')
    else:
        print('Инвентарь пуст.')


def move_player(game_state, direction):
    '''Move the player to a new room in the given direction.'''
    current_room = game_state['current_room']
    if direction in ROOMS[current_room]['exits']:
        target_room = ROOMS[current_room]['exits'][direction]
        inventory = game_state['player_inventory']
        if target_room == 'treasure_room':
            if 'rusty_key' not in inventory:
                print('Дверь заперта. Нужен ключ, чтобы пройти дальше.')
                return
            else:
                print(
                    'Вы используете найденный ключ, '
                    'чтобы открыть путь в комнату сокровищ.'
                )
        game_state['current_room'] = target_room
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
        random_event(game_state)
    else:
        print('Нельзя пойти в этом направлении.')


def take_item(game_state, item_name):
    '''Allow the player to take an item from the current room.'''
    if item_name == 'treasure_chest':
        print('Вы не можете поднять сундук, он слишком тяжелый.')
        return
    current_room = game_state['current_room']
    items = ROOMS[current_room]['items']
    if item_name in items:
        game_state['player_inventory'].append(item_name)
        items.remove(item_name)
        print(f'Вы подняли: {item_name}')
    else:
        print('Такого предмета здесь нет.')


def use_item(game_state, item_name):
    '''Use an item from the player's inventory.'''
    inventory = game_state['player_inventory']
    if item_name not in inventory:
        print('У вас нет такого предмета.')
        return
    if item_name == 'torch':
        print('Стало светлее. Теперь вы видите лучше.')
    elif item_name == 'sword':
        print('Вы чувствуете себя увереннее с мечом в руках.')
    elif item_name == 'bronze box':
        if 'rusty_key' not in inventory:
            inventory.append('rusty_key')
            print('Вы открыли шкатулку и нашли rusty_key.')
        else:
            print('Шкатулка пуста.')
    else:
        print('Вы не знаете, как использовать этот предмет.')

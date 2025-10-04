#!/usr/bin/env python3
from .constants import COMMANDS
from .player_actions import get_input, move_player, show_inventory, take_item, use_item
from .utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command_line):
    '''Process the user's command.'''
    parts = command_line.split()
    if not parts:
        return
    command = parts[0]
    arg = ' '.join(parts[1:]) if len(parts) > 1 else None

    match command:
        case 'go':
            if arg:
                move_player(game_state, arg)
            else:
                print('Куда идти? Укажите направление.')
        case 'north' | 'south' | 'east' | 'west':
            move_player(game_state, command)
        case 'look':
            describe_current_room(game_state)
        case 'take':
            if arg:
                take_item(game_state, arg)
            else:
                print('Что взять? Укажите предмет.')
        case 'use':
            if arg:
                if (
                    arg == 'treasure_chest'
                    and game_state['current_room'] == 'treasure_room'
                ):
                    attempt_open_treasure(game_state, get_input)
                else:
                    use_item(game_state, arg)
            else:
                print('Что использовать? Укажите предмет.')
        case 'inventory':
            show_inventory(game_state)
        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state, get_input)
            else:
                solve_puzzle(game_state, get_input)
        case 'help':
            show_help(COMMANDS)
        case 'quit' | 'exit':
            game_state['game_over'] = True
            print('Игра завершена.')
        case _:
            print('Неизвестная команда. Используйте help для списка команд.')


def main():
    '''Main game loop.'''
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0,
    }
    print('Добро пожаловать в Лабиринт сокровищ!')
    describe_current_room(game_state)
    while not game_state['game_over']:
        command = get_input('> ')
        process_command(game_state, command)


if __name__ == '__main__':
    main()

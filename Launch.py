'''
Launcher for Cici
'''

import os
import json
import sys
import time

enclosing_dir = os.path.dirname(os.path.realpath(__file__))
config_f_name = [f'{enclosing_dir}/config.example.json', f'{enclosing_dir}/config.json']
if not os.path.exists(config_f_name[0]):
    print('Could not find config template at ./config.example.json')
    print('Exiting...')
    sys.exit(1)


with open(config_f_name[0], 'r+') as config_f:
    config = json.load(config_f)


if __name__ == '__main__':
    if os.path.exists(f'{enclosing_dir}/.firstboot'):
        print('Hi! It seems like this is the first time you\'re launching Cici. Would you like to start the interactive installation script? [Y/n]')
        if input().lower().startswith('y'):
            os.system('clear')
            print('Cici interactive installation script')

            config['bot_token'] = input('\n\nYour discord token:\n')
            if input('\nCici\'s prefix will be set to "cc!". Would you like to change that? [y/N]\n').lower().startswith('y'):
                config['prefix_list'] = [input('\nCustom prefix:\n')]
            if input('\nThe default embed color for Cici is 3092790. Would you like to change that? [y/N]\n').lower().startswith('y'):
                config['embed_color'] = [input('\nEmbed color:\n')]

            os.remove(config_f_name[1]) if os.path.exists(config_f_name[1]) else False
            with open(config_f_name[1], 'w') as config_f:
                json.dump(config, config_f, indent=4)

            os.remove(f'{enclosing_dir}/.firstboot')
            if input('\nCici is now setup and ready for deployment. Would you like to run Cici now? [Y/n]\n').lower().startswith('y'):
                os.system('clear')
                print(f'Required dependencies will now be automatically installed using {sys.executable} -m pip \n\n')
                time.sleep(3)
                os.system(f'sudo -H {sys.executable} -m pip install -r requirements.txt; {sys.executable} {enclosing_dir}/Core.py')
    else:
        from Core import start_cici
        start_cici()

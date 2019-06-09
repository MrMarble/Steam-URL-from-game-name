import json
import os
import sys
import requests


def createSet(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def progressBar(value, endvalue, bar_length=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rGenerando URLs: [{0}] {1}%".format(
        arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()


def downloadGameList():
    print('No se ha encontrado la lista de juegos.')
    print('Descargando...')
    r = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    if r.status_code is 200:
        _games = r.json()['applist']['apps']
        games = {}
        for _game in _games:
            games[_game['name'].upper()] = _game['appid']
        with open('gameList.json', 'w', encoding='UTF-8') as gameList:
            json.dump(games, gameList)
            print('Lista Actualizada!')
        return True
    else:
        print('Ha ocurrido un error obteniendo la lista de juegos')
        return False


def compareGames(steamGames):
    if os.path.isfile('games.txt'):
        with open('games.txt', 'rt') as gameFile:
            userGames = createSet(gameFile.read().splitlines())
        detectados = len(userGames)
        print(detectados, 'Juegos detectados')
        with open('gameURLs.txt', 'w') as result:

            print('1º Obteniendo Comparaciones Completas...')
            for percent, gameName in enumerate(userGames):
                progressBar(percent, detectados)
                gameName = gameName.upper().strip()
                if gameName in steamGames:
                    result.write(
                        f'https://store.steampowered.com/app/{steamGames[gameName]}\t{gameName}\n')
            progressBar(detectados, detectados)

            print('\n2º Obteniendo Comparaciones Parciales...')
            result.write(
                '\n\n-----------------------------PARCIALES-----------------------------\n\n')
            for percent, gameName in enumerate(userGames):
                progressBar(percent, detectados)
                for _gameName in steamGames:
                    if _gameName.startswith(gameName.upper().strip()):
                        result.write(
                            f'https://store.steampowered.com/app/{steamGames[_gameName]}\t{_gameName}\n')
            progressBar(detectados, detectados)

        print('\nURLs listas!')
    else:
        print('No se encuentra el archivo games.txt')


def main():
    if os.path.isfile('gameList.json'):
        with open('gameList.json', 'r') as gameList:
            try:
                games = json.load(gameList)
            except Exception:
                if downloadGameList():
                    main()
        compareGames(games)

    else:
        downloadGameList()
        main()


if __name__ == '__main__':
    main()

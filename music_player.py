import sys
import argparse
import socket
import os
import configparser
import shutil

home = os.path.expanduser('~')
config_path = home + '/.config/music_player.conf'


def main():
    p = argparse.ArgumentParser(description='Send command for Music Player\n\tConfig file path = "~/.conf/music_player.conf"',
                                usage='If you didn\'t set host and port, Program get host and port from config file.')
    p.add_argument('--target', '-t', help='select Music Player Target')
    p.add_argument('--reset', help='Reset config file.', action='store_true')
    p.add_argument('COMMAND', nargs=argparse.REMAINDER,
                   help='Commands for Music Player')
    a = p.parse_args()

    if a.reset:
        if (os.path.isfile(config_path)):
            os.remove(config_path)
        shutil.copy('music_player.conf', config_path)
        print("Reset config file.")
        sys.exit(0)

    if len(a.COMMAND) < 1:
        print("Arg error.\n\t-h or --help - show help")
        sys.exit(3)
    conf = configparser.ConfigParser()
    if not os.path.isfile(config_path):
        shutil.copy('music_player.conf', config_path)
    conf.read(config_path)

    if a.target is not None:
        if not conf.has_section(a.target):
            print("Target isn't in the config file.")
            sys.exit(2)
        host, port = get_target(conf, a.target)
    host, port = get_target(conf)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(' '.join(a.COMMAND).encode('UTF-8'))
        data = s.recv(1024)
        print(repr(data))


def get_target(conf: configparser.ConfigParser, target=None) -> (str, int):
    if not conf.has_section('main'):
        cerr()
    if not (conf.has_option('main', 'default_target') and conf.has_option('main', 'default_port')):
        cerr()
    target = target or conf.get('main', 'default_target')
    if not conf.has_section(target):
        cerr()
    if not conf.has_option(target, 'host'):
        cerr()
    host = conf.get(target, 'host')
    if conf.has_option(target, 'port'):
        port = conf.get(target, 'port')
    else:
        port = conf.get('main', 'default_port')
    return host, int(port)


def cerr():
    print("Config Format Error.\n\tIf you want reset config file, run command with '--reset.'")
    sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Usage:
    new_ser_hz.py <username> [options]

Options:
    --sudo
"""

from __future__ import print_function

import os

from docopt import docopt as docoptinit

REGION = '{{region}}'


class User:
    def __init__(self, name):
        self.name = name

    def exec_by_user(self, cmd):
        os.system("su {} bash -c '{}' ".format(self.name, cmd))

    @property
    def zshrc(self):
        return '/home/{}/.zshrc'.format(self.name)

    def add_zshrc(self, line):
        if not os.path.isfile(self.zshrc):
            self.exec_by_user('touch ' + self.zshrc)
        f = open(self.zshrc).read()
        if line not in f:
            print('add', line, 'to bashrc')
            open(self.zshrc, 'a').write(line + '\n')

    def create_first(self):
        if REGION == 'alihz':
            os.environ['http_proxy'] = 'http://local.alihz-proxy.qbtrade.org:3128'
            os.environ['HTTP_PROXY'] = 'http://local.alihz-proxy.qbtrade.org:3128'
            os.environ['https_proxy'] = 'http://local.alihz-proxy.qbtrade.org:3128'
            os.environ['HTTPS_PROXY'] = 'http://local.alihz-proxy.qbtrade.org:3128'

        print('going to print env')
        os.system('env')
        os.system('echo \'{}:{}\' | chpasswd'.format(self.name, self.name))
        os.system('useradd -m {}'.format(self.name))
        # if docopt['--sudo']:
        os.system('usermod -aG sudo {}'.format(self.name))
        os.system('usermod -aG docker {}'.format(self.name))
        os.system('chsh -s /usr/bin/zsh {}'.format(self.name))

        self.add_zshrc('# put your own config into ~/.zshrc.local This script will be overwrite by some other script')
        self.add_zshrc('source /home/zshrc')

        self.exec_by_user('bash /opt/bin/pyenv-installer')
        if REGION == 'alihz':
            self.exec_by_user('mkdir ~/.pyenv/cache -p')
            self.exec_by_user('sudo cp /opt/Python-3.6.1.tar.xz ~/.pyenv/cache')
        self.exec_by_user('source ~/.zshrc && pyenv install 3.6.1')

        # oh my zsh
        self.exec_by_user('/opt/bin/oh-my-zsh.sh')


def init_once():
    if REGION == 'alihz':
        os.environ['http_proxy'] = 'http://local.alihz-proxy.qbtrade.org:3128'
        os.environ['HTTP_PROXY'] = 'http://local.alihz-proxy.qbtrade.org:3128'
        os.environ['https_proxy'] = 'http://local.alihz-proxy.qbtrade.org:3128'
        os.environ['HTTPS_PROXY'] = 'http://local.alihz-proxy.qbtrade.org:3128'
    os.system('mkdir -p /opt/bin')
    cmd = 'wget -O /opt/bin/pyenv-installer ' \
          ' https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer'
    os.system(cmd)
    os.system('chmod +x /opt/bin/pyenv-installer')

    cmd = 'wget -O /opt/bin/oh-my-zsh.sh ' \
          'https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh'
    os.system(cmd)
    os.system('chmod +x /opt/bin/oh-my-zsh.sh')

    cmd = 'wget -O /opt/Python-3.6.1.tar.xz https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tar.xz'
    os.system(cmd)


if __name__ == '__main__':

    if int(os.geteuid()) != 0:
        print('root is required')
        exit(1)
    docopt = docoptinit(__doc__)
    if docopt['<username>'] == 'init':
        init_once()
    else:
        u = User(docopt['<username>'])
        u.create_first()

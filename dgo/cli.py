# coding: utf-8
"""Console script for dgo."""
import sys
import os
import click
import requests

@click.group()
def main(args=None):
    return 0


@main.command()
@click.argument(u'local_file_path', type=click.File('rb'))
def upload(local_file_path):
    u"""
    Temporary upload a file.
    Then can download it later.
    But not guarantee when to delete from the server.
    So do not upload your importance file here.
    """
    ret = requests.post('http://tmp.daimon.cc:10080/upload', files={
        'file': local_file_path
    })
    click.secho('wget %s' % (ret.text.split(':', 1)[1].strip()), fg='cyan')
    return 0


@main.command()
@click.argument(u'url')
def wget(url):
    u"""wget with usual params."""
    cmd = "wget --content-disposition \"%s\"" % url
    os.system(cmd)


@main.command()
def pipconf():
    u"""创建pip 配置文件，使用国内镜像
    """
    pip_conf_file_content = """
[global]
index-url=https://mirrors.aliyun.com/pypi/simple/
trusted-host=
    mirrors.daimon.cc
    mirrors.cloud.tencent.com
    mirrors.aliyun.com
"""
    with open('/etc/pip.conf', 'w') as fout:
        fout.write(pip_conf_file_content)
    click.secho(u'/etc/pip.conf 文件创建成功', fg='green')


@main.command()
def pypirc():
    u"""pypirc配置文件"""
    pypirc_path = os.path.expanduser('~/.pypirc')
    if os.path.exists(pypirc_path):
        click.secho(u'~/.pypirc 文件已经存在', fg='red')
        return 1

    content = """
[distutils]
index-servers =
    pypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: %s
password: %s
"""
    username = click.prompt('username in pypi: ')
    password = click.prompt('password in pypi: ', hide_input=True)
    content = content % (username, password)
    with open(pypirc_path, 'w') as fout:
        fout.write(content)
    click.secho(u'~/.pypirc 生成完毕。', fg='green')


@main.command()
def goenv():
    u"""go 国内镜像"""
    content = u"""
go env -w GO111MODULE=on
go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct
# go 官方
# go env -w  GOPROXY=https://goproxy.io,direct
"""
    click.secho(content, fg='cyan')


@main.command()
@click.option(u'--input', u'-i', u'input_path', help=u'输入文件路径')
def enc(input_path):
    u"""加密。如果提供了 input_path，则对指定文件加密。否则从 stdin 读数"""
    extra = ""
    if input_path:
        extra = u'-in "%s" -out "%s.enc"' % (input_path, input_path)
    salt_key = click.prompt(u'请输入Key: ', hide_input=True)
    cmd = u'openssl aes-256-cbc -k %s -a -md md5 -base64 %s' % (salt_key, extra)
    os.system(cmd)


@main.command()
@click.option(u'--input', u'-i', u'input_path', help=u'输入文件路径')
def dec(input_path):
    u"""解密。如果提供了 input_path，则对指定文件解密。否则从 stdin 读数"""
    extra = ""
    if input_path:
        extra = u'-in "%s" -out "%s.dec"' % (input_path, input_path)
    salt_key = click.prompt(u'请输入Key: ', hide_input=True)
    cmd = u'openssl aes-256-cbc -k %s -a -md md5 -base64 -d %s' % (salt_key, extra)
    os.system(cmd)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

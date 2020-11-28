# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-06-30 17:32:56
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-28 02:05:13
# @Description  : 读取并验证配置
'''

from os import getcwd, path

import toml

from .log import get_logger

logger = get_logger('Config')
default_path = path.join(getcwd(), 'config.toml')


def get_config(cpath: str = default_path) -> dict:
    '''
    读取并验证配置

    参数:
        [path]:配置文件路径,默认为config.toml
    返回:
        dict:验证过的配置字典,如果读取出错则返回None
    '''
    try:
        logger.info('开始读取配置')
        raw_cfg = dict(toml.load(cpath))
        cfg = verify_config(raw_cfg)
        logger.info('配置验证通过')
        return (cfg)

    except FileNotFoundError:
        logger.error(f'配置文件[{cpath}]不存在')
        with open(cpath, 'w+', encoding='utf-8') as f:
            toml.dump(verify_config({}), f)
        logger.error('已生成默认配置,请重新运行程序')

    except ValueError as e:
        logger.error(f'配置文件验证失败[{e}]')


def verify_config(cfg: dict) -> dict:
    '''
    验证配置

    参数:
        cfg:配置字典
    返回:
        dict:验证过的配置字典,剔除错误的和不必要的项目
    '''
    other = __verify_other(cfg.get('other', {}))

    itad = __verify_itad(cfg.get('itad', {}))
    if not itad['token'] and cfg:
        raise ValueError('未设置API token,可以自行申请或者使用文档中的公共token')

    net = __verify_net(cfg.get('net', {}))

    output = __verify_output(cfg.get('output', {}))

    vcfg = {'other': other, 'itad': itad,
            'net': net, 'output': output}

    return (vcfg)


def __verify_other(other: dict) -> dict:
    '''
    验证other节
    '''
    wait_screen = bool(other.get('wait_screen', True))
    other = {'wait_screen': wait_screen}
    return (other)


def __verify_itad(itad: dict) -> dict:
    '''
    验证itad节
    '''
    token = itad.get('token', '')
    region = itad.get('region', 'cn')
    country = itad.get('country', 'CN')
    symbol = itad.get('currency_symbol', '¥')
    itad = {'token': token,
            'region': region,
            'country': country,
            'currency_symbol': symbol}
    return (itad)


def __verify_net(net: dict) -> dict:
    '''
    验证net节
    '''
    proxy = net.get('proxy', None)
    p = {"http://": proxy, "https://": proxy} if proxy else None
    net = {'proxy': p}
    return (net)


def __verify_output(output: dict) -> dict:
    '''
    验证output节
    '''
    markdown = bool(output.get('markdown', True))
    xlsx = bool(output.get('xlsx', True))
    json = bool(output.get('json', False))

    output = {'markdown': markdown,
              'xlsx': xlsx, 'json': json}
    return (output)

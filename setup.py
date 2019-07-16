# coding=utf-8
"""Install pyiqfeed into your library path."""

from setuptools import setup
from setuptools import setup, find_packages
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))
 
with open('requirements.txt') as fp:
    install_requires = fp.read()
 
def install_deps():
    default = open('requirements.txt', 'r').readlines()
    new_pkgs = []
    links = []
    for resource in default:
        if 'git+https' in resource:
            array = resource.split("@")
            tag = array[-1]
            lib = array[-2].split("/")[-1].split(".")[-2]
            pkg = lib + "==" + tag
            links.append(resource.strip() + "#egg=" + lib + "-" + tag)
            new_pkgs.append(pkg)
        else:
            new_pkgs.append(resource.strip())
    return new_pkgs, links
 
pkgs, new_links = install_deps()
 
setup(
    name='ds-pyiqfeed',
    version='0.1',
    description='Handles connections to IQFeed, the market data feed by DTN',
    url='https://github.com/DS-DataMining/pyiqfeed/',
    author='Mujezinovic Ajdin',
    author_email='ajdin.m@gmail.com',
    packages=find_packages(),  # Required
    zip_safe=False,
    install_requires=['numpy', 'pandas'],
    dependency_links=new_links,)

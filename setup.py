# -*- coding: utf-8 -*-
# @Author  : LG

from setuptools import setup, find_packages


def get_version():
    from IDAT import __version__
    return __version__


setup(
    name="idat",
    version=get_version(),
    author="yatengLG",
    author_email="yatenglg@qq.com",
    description="Object Detection Annotation Tool.",
    long_description="Object Detection Annotation Tool.",
    url="https://github.com/yatengLG/IDAT",

    keywords=["pip", "idat", "object detection"],
    license="MIT Licence",

    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('IDAT', ['IDAT/default.yaml']),
        ('IDAT/ui', ['IDAT/ui/zh_CN.ts', 'IDAT/ui/en.ts', 'IDAT/ui/zh_CN.qm']),
    ],
    platforms="any",

    python_requires=">=3.6",                            # python 版本要求
    install_requires=[
        'imgviz',
        'pyqt5',
        'pyyaml'
    ],
    classifiers=[
        "Intended Audience :: Developers",  # 目标用户:开发者
        "Intended Audience :: Science/Research",  # 目标用户:学者
        'Development Status :: 5 - Production/Stable',
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "console_scripts": [
            "idat=IDAT.main:main",
        ],
    },
)

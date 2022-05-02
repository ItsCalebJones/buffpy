from setuptools import setup


requires_list = [
    "certifi==2019.3.9",
    "chardet==3.0.4",
    "colorama==0.4.1",
    "coverage==4.5.3",
    "httpretty==0.9.6",
    "idna==2.8",
    "mock==3.0.5",
    "nose==1.3.7",
    "rauth==0.7.3",
    "requests==2.22.0",
    "six==1.12.0",
]


setup(
    name="buffpy",
    version="3.0",
    platforms="any",
    description="Python library for Buffer App",
    author="Vlad Temian",
    author_email="vladtemian@gmail.com",
    url="https://github.com/vtemian/buffpy",
    packages=["buffpy", "buffpy.managers", "buffpy.models"],
    include_package_data=True,
    install_requires=requires_list,
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ]
)

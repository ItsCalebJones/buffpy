from setuptools import setup


requires_list = [
    "colorama==0.4.1",
    "rauth==0.7.3",
    "requests==>=2.25,<3",
    "six",
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
        "Programming Language :: Python :: 3.10",
    ]
)

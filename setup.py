from setuptools import setup

setup(
    name="imaper",
    version="0.0.1",
    author="Dan Horrigan",
    author_email="dhorrigan@ag.com",
    description=("IMAP made easy."),
    packages=["imaper"],
    install_requires=[
        "IMAPClient==0.10.2",
    ],
    classifiers=[
        "Topic :: Utilities",
    ],
)

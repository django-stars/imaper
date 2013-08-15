from setuptools import setup

setup(
    name="imaper",
    version="1.0.0",
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

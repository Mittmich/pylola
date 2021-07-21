import setuptools

setuptools.setup(
    name="pylola",
    version="0.1",
    author="Michael Mitter",
    author_email="michael_mitter@hotmail.com",
    description="python implementation of LOLA",
    long_description_content_type="",
    packages=setuptools.find_packages(),
    install_requires=[
        "bioframe==0.2.1",
        "scipy==1.5.2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
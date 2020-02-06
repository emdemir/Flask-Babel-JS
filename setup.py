import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent
README = (HERE/"README.md").read_text()

setup(
    name="Flask-Babel-JS",
    version="1.0.0",
    url="https://github.com/emdemir/Flask-Babel-JS/",
    license="BSD",
    author="Efe Mert Demir",
    author_email="efemertdemir@hotmail.com",
    description="Flask extension to add Flask-Babel translations in JS",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["flask_babel_js"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=[
        "Flask",
        "flask-babel"
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

from setuptools import setup


with open('README.md') as fp:
    long_description = fp.read()

setup(
    name='Flask-ZeroRPC',
    version='0.1',
    download_url='https://github.com/lixm/flask-zerorpc/',
    license='BSD',
    author='comyn',
    author_email='me@xueming.li',
    description='ZeroPC for Flask',
    long_description=long_description,
    py_modules=['flask_zerorpc'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'zerorpc',
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

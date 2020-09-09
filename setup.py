from setuptools import setup

setup(
    name='Your Application',
    version='1.0',
    long_description=__doc__,
    packages=['yourapplication'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'boto3==1.14.57',
        'botocore==1.17.57',
        'cffi==1.14.2',
        'click==7.1.2',
        'cryptography==2.9.2',
        'docutils==0.15.2',
        'Flask==1.1.2',
        'Flask-SocketIO==4.3.1',
        'itsdangerous==1.1.0',
        'Jinja2==2.11.2',
        'jmespath==0.10.0',
        'jwt==1.0.0',
        'MarkupSafe==1.1.1',
        'pycparser==2.20',
        'PyMySQL==0.10.0',
        'python-dateutil==2.8.1',
        'python-engineio==3.13.2',
        'python-socketio==4.6.0',
        's3transfer==0.3.3',
        'six==1.15.0',
        'SQLAlchemy==1.3.19',
        'urllib3==1.25.10',
        'Werkzeug==1.0.1'
    ]
)
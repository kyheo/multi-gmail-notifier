from setuptools import setup, find_packages

setup(
    name = "multigmailnotifier",
    version = "0.2",
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'multigmailnotifier = multigmailnotifier.run:main',
            ], 
        },    
    include_package_data = True,
    author = "Martin Marrese",
    author_email = "marrese@gmail.com",
    description = "GMail new email checker",
    #long_description=read('README'),
    install_requires = ['feedparser',
                        #'python-notify',
                        #'python-indicate',
                        #'pygobject',
                        ]
)

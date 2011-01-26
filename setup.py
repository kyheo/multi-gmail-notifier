from setuptools import setup, find_packages

setup(
    name = "multi-gmail-notifier",
    version = "0.2",
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'multi-gmail-notifier = multi-gmail-notifier.run:main',
            ], 
        },    
    test_suite = "multi-gmail-notifier.test",
    include_package_data = True,
    author = "Martin Marrese",
    author_email = "marrese@gmail.com",
    description = "GMail new email checker",
    #long_description=read('README'),
    install_requires = ['python-notify',
                        'python-indicate',
                        'python-gobject',
                        ]
)

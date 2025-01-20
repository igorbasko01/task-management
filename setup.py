from setuptools import setup, find_packages

setup(
    name='task-cli',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'python-frontmatter',
        'PyYAML',
    ],
    entry_points={
        'console_scripts': [
            'task=task_cli.main:cli'
        ]
    }
)
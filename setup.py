from setuptools import setup, find_packages

version = {}
with open('task_cli/version.py') as f:
    exec(f.read(), version)

setup(
    name='task-cli',
    version=version['__version__'],
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
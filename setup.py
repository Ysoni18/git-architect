from setuptools import setup, find_packages

setup(
    name="git-architect",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["main"], 
    install_requires=[
        "click>=8.1.0",
        "GitPython>=3.1.0",
        "langchain-core>=0.3.0",
        "langchain-ollama>=1.1.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        'console_scripts': [
            'git-architect=main:analyze',
        ],
    },
)
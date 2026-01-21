from setuptools import setup, find_packages

setup(
    name="ai-nexus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0",
        "click>=8.0",
        "requests>=2.31.0",
        "paramiko>=3.0.0",
    ],
    entry_points={
        'console_scripts': [
            'ai-nexus=ai_nexus.cli:main',
        ],
    },
    python_requires='>=3.8',
    author="holmgren100",
    description="Universal AI Collaboration Platform",
)

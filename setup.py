import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'click==7.1.2',
    'humanize==2.4.0',
    'iso8601==0.1.12',
    'requests==2.24.0',
]
setuptools.setup(
    name="reposearch",
    version="0.0.1",
    author="jan",
    author_email="stuff@kwoh.de",
    description="a small cli tool to search for repositories across different platforms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/puhoy/reposearch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,

    # enables the use of MANIFEST.in
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'reposearch = reposearch.main:search'
        ]
    }
)

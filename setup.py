from setuptools import setup, find_packages

setup(
    name='newsclipse',
    version='0.1',
    description="An IDE for news makers.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords='influence journalism ddj entities',
    author='',
    author_email='canvaside@groups.google.com',
    url='http://canvas.aljazeera.com',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points={},
    tests_require=[]
)

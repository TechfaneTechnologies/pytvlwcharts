import setuptools

setuptools.setup(
    name='pytvlwcharts',
    version='0.0.1',
    description=
    "An Experimental Python Wrapper For Tradingview's Lightweight-Charts To Be Used In Notebook Environments.",
    long_description=open('README.md', 'r', encoding='utf8').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/TechfaneTechnologies/pytvlwcharts',
    project_urls={
        "Bug Tracker": "https://github.com/TechfaneTechnologies/pytvlwcharts/issues"
    },
    license='MIT License',
    packages=['pytvlwcharts'],
    install_requires=['apischema', 'jinja2', 'absl-py', 'pandas', 'numpy'],
)

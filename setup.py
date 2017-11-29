from distutils.core import setup

setup(
    name='parsl_dav_vis',
    packages=['dag_vis'],
    version='0.1',  # Ideally should be same as your GitHub release tag varsion
    description='DAG visualization code to be run from Jupyter notebooks to visualize data flow dependency graphs of workflows',
    author='Ben Glick',
    author_email='glick@lclark.edu',
    url='https://github.com/benhg/parsl-dag-vis',
    download_url='download link you saved',
    keywords=['parsl', 'jupyter', 'visualization'],
    classifiers=[],
)

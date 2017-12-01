from distutils.core import setup

setup(
    name='parsl_dag_vis',
    packages=['dag_vis'],
    version='0.1.2',
    description='DAG visualization code to be run from Jupyter notebooks to visualize data flow dependency graphs of workflows',
    author='Ben Glick',
    author_email='glick@lclark.edu',
    license='Apache 2.0',
    url='https://github.com/benhg/parsl-dag-vis',
    download_url='https://github.com/benhg/parsl-dag-vis/archive/v0.1-alpha.zip',
    keywords=['parsl', 'jupyter', 'visualization',
              'Workflows', 'Scientific computing'],
    install_requires=[
        'parsl',
        'jupyter',
        'ipython'
    ],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6', ],
)

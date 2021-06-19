from setuptools import setup, find_packages


setup(
    name='jhe921-movie-prediction',
    version='0.1.0',
    description="Project for predicting which actors may have said a movie line.",
    url='https://github.com/jhe921/movie_prediction',
    author='Corey Fyock',
    author_email='coreyfyock@gmail.com',
    packages=find_packages(
        include=['movie_prediction', 'movie_prediction.*'],
    ),
    python_requires='>=python3.7',
    install_requires=[
        'seaborn', 'transformers', 'pandas', 'umap-learn'
    ]
)
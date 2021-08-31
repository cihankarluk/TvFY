from setuptools import setup

setup(
    name="TvFY",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    url="https://github.com/cihankarluk/TvFY.git",
    description="TvFY is simply app for chill.",
    author="Cihan Karluk",
    author_email="cihankarluk@gmail.com",
    install_requires=[
        "Django==3.2.5",
        "python-dotenv==0.19.0",
        "psycopg2-binary==2.9.1",
        "django-rest-framework==0.1.0",
        "requests==2.24.0",
        "beautifulsoup4==4.9.3",
        "backoff==1.11.1",
        "pre-commit==2.10.0",
        "model-bakery==1.3.2",
        "django-extensions==3.1.3",
        "aiohttp==3.7.4",
    ],
    python_requires=">=3.8.0",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
    ],
)

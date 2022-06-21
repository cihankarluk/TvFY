from setuptools import setup, find_packages

setup(
    name="TvFY",
    use_scm_version=True,
    setup_requires=["setuptools_scm", "setuptools"],
    url="https://github.com/cihankarluk/TvFY.git",
    description="TvFY is simply app for chill.",
    packages=find_packages(include=["tvfy*"]),
    author="Cihan Karluk",
    author_email="cihankarluk@gmail.com",
    install_requires=[
        # DJANGO
        "django==4.0.4",
        "djangorestframework==3.13.1",
        "django-filter==22.1",
        "django-environ==0.9.0",
        "django-rest-framework==0.1.0",
        "django-extensions==3.1.3",
        "pytest-django==4.5.2",
        "django-click==2.3.0",
        "model-bakery==1.3.2",
        "django-allauth==0.51.0",
        "djangorestframework-simplejwt==5.2.0",
        "dj-rest-auth==2.2.4",

        # DATABASE
        "psycopg2==2.9.3",

        # OTHERS
        "python-dotenv==0.19.0",
        "requests==2.24.0",
        "beautifulsoup4==4.9.3",
        "backoff==2.0.1",
        "pre-commit==2.10.0",
        "aiohttp==3.7.4",
        "drf-yasg",
        "coverage",
    ],
    python_requires=">=3.9.0",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
    ],
)

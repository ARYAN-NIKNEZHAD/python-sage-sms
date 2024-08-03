from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="python_sage_sms",
    version="0.1.0",
    author="Mohammad Fotouhi",
    author_email="mohammad@sageteam.org",
    description="A Python client library for managing BigBlueButton connections and operations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sageteamorg/python-sage-sms",
    projcet_urls={
        "Documentation": "https://python-sage-sms.readthedocs.io/en/latest/",
        "Issues": "https://github.com/sageteamorg/python-sage-sms/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
)

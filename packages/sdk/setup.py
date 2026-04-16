from setuptools import setup, find_packages

setup(
    name="grasp-sdk",
    version="0.1.0",
    description="Python SDK for the GRASP Grasp Reliability & Safety Platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="GRASP Team",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.27.0",
        # pydantic is not strictly needed for the SDK models since we use dataclasses,
        # but the prompt mentioned httpx and pydantic as the only dependencies.
        # We'll stick to dataclasses for the models to stay lightweight.
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

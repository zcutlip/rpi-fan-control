from setuptools import find_packages, setup

about = {}
with open("src/fancontrol/__about__.py") as fp:
    exec(fp.read(), about)

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(name=about["__title__"],
      version=about["__version__"],
      description=about["__summary__"],
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Zachary Cutlip",
      author_email="uid000@gmail.com",
      url="TBD",
      license="MIT",
      package_dir={"": "src"},
      packages=find_packages(where="src"),
      entry_points={
          'console_scripts': ['rpi-fancontrol=fancontrol.main:main'], },
      python_requires='>=3.10',
      # only install RPi.GPIO if we're on Linux
      # otherwise dev-reqs.txt will cause FakeRPi to be installed
      install_requires=['RPi.GPIO;sys_platform=="linux"'],
      package_data={},
      )

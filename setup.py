from setuptools import setup,find_packages;

setup(
	name="AberothIncendium",
	#versioning scheme: major.minor 
	#versioning scheme developement: major.minor ['.dev' yymmdd]
	version="0.1.dev180310",
	description="An API to intercept and analyse the network communication of the game Aberoth",
	url="https://github.com/0xJonas/AberothIncendium",
	author="Delphi1024",
	author_email="delphi1024@gmail.com",
	packages=find_packages("src"),
	package_dir={"":"src"},
	python_requires=">=3",
	package_data={"incendium":["launcher/ParamLauncher.jar"]}
);
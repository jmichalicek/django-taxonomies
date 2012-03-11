from setuptools import setup

files = ['taxonomy/*']
dependencies = ['mock>=0.7.2']
setup(name = "django-taxonomies",
      version = "0.0.1",
      description = "A django app to provide taxonomy data for any models",
      author = "Justin Michalicek",
      author_email = "jmichalicek@gmail.com",
      url = "https://github.com/jmichalicek/django-taxonomies",
      packages = ['taxonomy', 'taxonomy.templatetags'],
      #'package' package must contain files (see list above)
      package_data = {'taxonomy' : files },
      install_requires = dependencies,
      #'runner' is in the root.
      #scripts = ["runner"],
      long_description = """Really long text here.""" 
      #
      #This next part it for the Cheese Shop, look a little down the page.
      #classifiers = []     
) 

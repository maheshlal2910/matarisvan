from distutils.core import setup

setup(name='bulbs_garnish',
      version='0.1',
      description='A DSL to write scripts that hit a URL and get data. It also allows you to specify relations between the data. Use with Bulbs_Garnish or something that exposes similar interface.',
      author='Mahesh Lal',
      author_email='mahesh.2910@gmail.com',
      py_modules=['matarisvan.operations', 'matarisvan.operation_graph.entities', 'matarisvan.operation_graph.data_operations']
     )

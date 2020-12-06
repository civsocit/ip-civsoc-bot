from setuptools import setup


setup(name='ip-civsoc-bot',
      version='0.2.0',
      packages=['ip_bot'],
      entry_points={
          'console_scripts': [
              'ip-bot = ip_bot.main:main'
          ]
      })

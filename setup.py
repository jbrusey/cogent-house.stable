from distutils.core import setup

setup(name='ch-base',
      version='1.0',
      description='CogentHouse base station logger',
      author='James Brusey, Ross Wilkins',
      author_email='james.brusey@gmail.com',
      packages=['cogent',
                'cogent.base',
                'cogent.base.model',
                'cogent.report',
                'cogent.node'],
      package_data={'cogent.base' : ['Calibration/*.csv']},
      data_files=[('/etc/init', ['etc/ch-sf.conf', 'etc/ch-base.conf']),
                  ('/etc/cron.daily', ['etc/ch-daily-email']),
                  ('/etc/apache2/sites-available', ['etc/cogent-house']),
                  ('/var/www/cogent-house', ['www/index.py']),
                  ('/var/www/scripts', ['www/scripts/datePicker.js']),
                  ('/var/www/style', ['www/style/ccarc.css'])
                  ]
      )

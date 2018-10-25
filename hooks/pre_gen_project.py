import re
import sys


MODULE_REGEX = r'^[_a-z][_a-z0-9]+$'

slug = '{{ cookiecutter.slug }}'

if not re.match(MODULE_REGEX, slug):
    print('ERROR: %s is not a valid slug, underscores and lowercase only' % slug)
    # exits with status 1 to indicate failure
    sys.exit(1)
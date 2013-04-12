# packages.zip is a ZIP archive that contains the bigpackage directory
# and this source file (bigmodule.py).  It's included here under the
# UNUSED_packages directory so you can see what's in it.  The app
# itself doesn't use the UNUSED_packages, and imports this module
# directly from the ZIP archive.

def get_message():
    return '<p>You have called the get_message() function.</p>'

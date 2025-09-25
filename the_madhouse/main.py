"""
Test description for this module
"""

import sys

from app import DevLauncher, ProdLauncher

if __name__ == "__main__":
    if "--dev" in sys.argv:
        app = DevLauncher()
        app.run()
    elif "--prod" in sys.argv:
        app = ProdLauncher()
        app.run()
    else:
        print(
            """=== WARNING ===
Flask didn't start.
Make sure to launch the app with the proper command.
=== WARNING ==="""
        )

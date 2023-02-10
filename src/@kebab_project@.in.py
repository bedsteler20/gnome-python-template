import os
import sys
import signal
import locale
import gettext


VERSION = '@VERSION@'
pkgdatadir = '@pkgdatadir@'
localedir = '@localedir@'
sourceroot = '@sourceroot@'


def start_debugger():
    print("Running in debug mode")
    try:
        import debugpy
        import json
    except ImportError:
        print("Unable to locate debugpy package can't start debugger")
        return
    
    debug_options = {
        "type": "python",
        "request": "attach",
        "connect": {"host": "localhost", "port": 5678},
        "pathMappings": [{
            "localRoot": os.path.join(sourceroot, 'src'),
            "remoteRoot": os.path.join(pkgdatadir, "@snake_project@")
        }],
        "justMyCode": True,
    }

    debugpy.listen(debug_options["connect"]["port"])
    os.system(
        f"xdg-open 'vscode://fabiospampinato.vscode-debug-launcher/launch?args={json.dumps(debug_options)}'")
    print("Waiting for debugger connection ...")
    debugpy.wait_for_client()
    print("Debugger connected!")


sys.path.insert(1, pkgdatadir)
signal.signal(signal.SIGINT, signal.SIG_DFL)
locale.bindtextdomain('@kebab_project@', localedir)
locale.textdomain('@kebab_project@')
gettext.install('@kebab_project@', localedir)

if os.environ.get("DEBUG_MODE") == "1":
    start_debugger()

if __name__ == '__main__':
    import gi
    gi.require_version('Gtk', '4.0')

    from gi.repository import Gio
    resource = Gio.Resource.load(os.path.join(
        pkgdatadir, '@kebab_project@.gresource'))
    resource._register()

    from @snake_project@.backend import main
    sys.exit(main.main(VERSION))

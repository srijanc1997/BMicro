def main():
    import os
    import sys
    from pathlib import Path

    # Prefer local bmlab when present (sibling of BMicro repo), so that
    # development changes in bmlab are used instead of the installed package.
    _this_file = Path(__file__).resolve()
    _bmicro_root = _this_file.parent.parent  # .../BMicro
    _bmlab_local = _bmicro_root.parent / "bmlab"
    if _bmlab_local.is_dir() and (_bmlab_local / "bmlab").is_dir():
        _path_insert = str(_bmlab_local.parent)
        if _path_insert not in sys.path:
            sys.path.insert(0, _path_insert)

    from importlib import resources
    import logging

    from PyQt6 import QtGui, QtWidgets

    from bmicro.gui.main import BMicro
    from bmicro._version import version as __version__
    """
    Starts the BMicro application and handles its life cycle.
    """
    app = QtWidgets.QApplication(sys.argv)
    # set window icon
    ref = resources.files('bmicro') / 'img'
    with resources.as_file(ref) as imdir:
        icon_path = os.path.join(imdir, "icon.png")
        app.setWindowIcon(QtGui.QIcon(icon_path))

    window = BMicro()
    window.show()

    for arg in sys.argv:
        if arg == '--version':
            print(__version__)
            QtWidgets.QApplication.processEvents()
            sys.exit(0)
        elif arg.startswith('--log='):
            log_level = arg[6:]
            logging.basicConfig(level=log_level)

    if sys.argv[-1].endswith('.h5'):
        window.open_file(sys.argv[-1])

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

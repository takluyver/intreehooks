Load a PEP 517 backend from within the source tree.

In `PEP 517 <https://www.python.org/dev/peps/pep-0517/>`_, package building
backends are not loaded from the source of the package being built. This
prevents accidentally shadowing your build system, but some packages, like
build tools, want to act as their own backend.

``intreehooks`` is a shim to work around this, so that a source tree can be
built by itself. To use it, write a pyproject.toml like this:

.. code-block:: ini

    [build-system]
    requires = ["intreehooks"]  # + any other packages required to build
    build-backend = "intreehooks:loader"

    [tool.intreehooks]
    build-backend = "flit.buildapi"  # Import path of your real backend


from typeguard.importhook import install_import_hook

# MUST be before import of any modules, owned by project
install_import_hook(('pydicates',))

import sys

# base settings
import settings.components.base  # noqa
import settings.components.email  # noqa
import settings.components.pubsub  # noqa
import settings.components.redis  # noqa
from settings.utils import flatten_module_attributes

flatten_module_attributes(
    module=sys.modules[__name__],
    imports=list(sys.modules.keys()),
    prefix="settings.",
)

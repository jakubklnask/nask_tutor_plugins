"""
NASK Hide Menu Items
Hides default header menus and learner dashboard sidebar widgets.
"""
from tutor import hooks
from tutormfe.hooks import PLUGIN_SLOTS

PLUGIN_SLOTS.add_items([
    # Hide learner dashboard sidebar
    (
        "learner-dashboard",
        "org.openedx.frontend.learner_dashboard.widget_sidebar.v1",
        """
        {
          op: PLUGIN_OPERATIONS.Hide,
          widgetId: 'default_contents',
        }"""
    ),
    # Hide desktop main menu
    (
        "all",
        "org.openedx.frontend.layout.header_desktop_main_menu.v1",
        """
        {
          op: PLUGIN_OPERATIONS.Hide,
          widgetId: 'default_contents',
        }"""
    ),
    # Hide mobile main menu
    (
        "all",
        "org.openedx.frontend.layout.header_mobile_main_menu.v1",
        """
        {
          op: PLUGIN_OPERATIONS.Hide,
          widgetId: 'default_contents',
        }"""
    ),
])

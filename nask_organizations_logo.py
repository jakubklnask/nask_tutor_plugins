"""
NASK Organization Logo Plugin
Shows organization logo based on user email domain.
"""
from tutor import hooks
from tutormfe.hooks import PLUGIN_SLOTS

LOGO_COMPONENT_JS = """
const IMAGES = {
  PESA: 'https://raw.githubusercontent.com/jakubklnask/openedx-nask-static-assets/refs/heads/nask-custom/logo_pesa_smaller.png',
  ZUS: 'https://raw.githubusercontent.com/jakubklnask/openedx-nask-static-assets/refs/heads/nask-custom/logo_zus.png',
  NASK: 'https://raw.githubusercontent.com/jakubklnask/openedx-nask-static-assets/refs/heads/nask-custom/NASK_logo_RGB_KOLOR.svg',
  DEFAULT: null,
};

const PHRASE_TO_IMAGE = {
  'pesa': IMAGES.PESA,
  'zus': IMAGES.ZUS,
  'nask': IMAGES.NASK,
};

const getImageForEmail = (email) => {
  if (!email) return IMAGES.DEFAULT;
  const emailLower = email.toLowerCase();
  for (const [phrase, imageUrl] of Object.entries(PHRASE_TO_IMAGE)) {
    if (emailLower.includes(phrase.toLowerCase())) {
      return imageUrl;
    }
  }
  return IMAGES.DEFAULT;
};

const user = window.getAuthenticatedUser ? window.getAuthenticatedUser() : null;
const imageUrl = getImageForEmail(user?.email);

if (!imageUrl) return null;

return (
  <div style={{ textAlign: 'center' }}>
    <img 
      src={imageUrl} 
      alt="User logo" 
      style={{ height: '40px', width: 'auto' }}
    />
  </div>
);
"""

PLUGIN_SLOTS.add_items([
    (
        "all",
        "org.openedx.frontend.layout.header_desktop_secondary_menu.v1",
        f"""
        {{
          op: PLUGIN_OPERATIONS.Insert,
          widget: {{
            id: 'custom_secondary_menu_component',
            type: DIRECT_PLUGIN,
            RenderWidget: () => {{
              {LOGO_COMPONENT_JS}
            }},
          }},
        }}
        """
    ),
])

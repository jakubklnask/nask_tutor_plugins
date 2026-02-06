from tutormfe.hooks import PLUGIN_SLOTS

NO_COURSES_JSX = """
<div 
  className="p-5 text-center bg-white border rounded-3" 
  style={{ 
    marginTop: '2rem', 
    boxShadow: '0 4px 12px rgba(0,0,0,0.08)', 
    borderColor: '#e0e0e0' 
  }}
>
  <p className="lead mb-3 text-dark" style={{ fontWeight: '500', fontSize: '1.25rem' }}>
    Nie jesteś zapisany na żadne kursy.
  </p>
  <p className="text-muted" style={{ fontSize: '1.1rem' }}>
    Skontaktuj się z pomocą 
    <a 
      href="mailto:przykladowy_support@mail.com" 
      style={{ 
        color: '#1B3961', 
        fontWeight: 'bold', 
        textDecoration: 'none', 
        marginLeft: '8px' 
      }}
    >
      przykladowy_support@mail.com
    </a>
  </p>
</div>
"""

PLUGIN_SLOTS.add_items([
    # KROK 1: Ukrywamy domyślną treść edX (odpowiednik keepDefault: false)
    (
        "learner-dashboard",
        "org.openedx.frontend.learner_dashboard.no_courses_view.v1",
        """
        {
          op: PLUGIN_OPERATIONS.Hide,
          widgetId: 'default_contents',
        }
        """
    ),
    # KROK 2: Wstawiamy nowy, biały widok
    (
        "learner-dashboard",
        "org.openedx.frontend.learner_dashboard.no_courses_view.v1",
        f"""
        {{
          op: PLUGIN_OPERATIONS.Insert,
          widget: {{
            id: 'nask_custom_no_courses_view',
            type: DIRECT_PLUGIN,
            priority: 50,
            RenderWidget: () => (
              {NO_COURSES_JSX}
            ),
          }},
        }}
        """
    ),
])
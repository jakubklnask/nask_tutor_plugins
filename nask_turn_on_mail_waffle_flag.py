from tutor import hooks

PYTHON_SCRIPT = '''
from lms.djangoapps.bulk_email.models import BulkEmailFlag

# Używamy update_or_create, co jest najbezpieczniejszą metodą w skryptach init
# Jeśli rekord o pk=1 nie istnieje, zostanie stworzony. Jeśli istnieje - zaktualizowany.
# Wysoki klucz, gdyby istnialy juz flagi to doda nowa na koncu nadpisujac wszytskie poprzednie
# Inaczej tylko zaktualizowalo by ta o pk#1 a jest ryzyko ze jakas o np. pk2 by wtedy byla zczytywana
# jako aktualna
obj, created = BulkEmailFlag.objects.update_or_create(
    pk=100, 
    defaults={
        'enabled': True,
        'require_course_email_auth': False
    }
)

status = "stworzona" if created else "zaktualizowana"
print(f"+++ Flaga BulkEmailFlag została {status} (bez przypisania użytkownika).")
'''

BASH_COMMAND = f"""
echo "++++++ Konfiguracja Bulk Email (Safe Mode)..."

cat << 'EOF' | ./manage.py lms shell
{PYTHON_SCRIPT}
EOF
"""

hooks.Filters.CLI_DO_INIT_TASKS.add_item(
    ("lms", BASH_COMMAND)
)

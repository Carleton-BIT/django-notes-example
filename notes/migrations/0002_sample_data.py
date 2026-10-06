from django.db import migrations

SAMPLE = [
    {
        'course_code': 'ITEC 4012',
        'title': 'Web Application Frameworks',
        'description': 'Django, HTMX and deploying to a production server.',
        'notes': [
            ('Models and relationships',
             'A ForeignKey on Note points at Notebook, so one notebook has many notes.\n\n'
             'Use related_name to read them from the other side: notebook.notes.all()'),
            ('HTMX search',
             'hx-get sends the search box value to the server and hx-target swaps the '
             'returned HTML into the page. The view returns only the list when request.htmx is set.'),
            ('Deployment checklist',
             '1. Merge the pull request into main\n2. Watch the GitHub Action finish\n'
             '3. Check the site, then read the logs with journalctl if something is wrong'),
        ],
    },
    {
        'course_code': 'BIT 2008',
        'title': 'Multimedia Data Management',
        'description': 'SQL queries, joins and database design.',
        'notes': [
            ('Joins', 'An INNER JOIN keeps rows that match in both tables. A LEFT JOIN keeps every row '
                      'of the left table and fills the missing columns with NULL.'),
            ('GROUP BY', 'Every selected column must be in the GROUP BY clause or inside an aggregate '
                         'function such as COUNT, SUM or AVG.'),
        ],
    },
]


def load_sample_data(apps, schema_editor):
    Notebook = apps.get_model('notes', 'Notebook')
    Note = apps.get_model('notes', 'Note')
    for item in SAMPLE:
        notebook = Notebook.objects.create(
            course_code=item['course_code'], title=item['title'], description=item['description'])
        for title, body in item['notes']:
            Note.objects.create(notebook=notebook, title=title, body=body)


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_sample_data, migrations.RunPython.noop),
    ]

from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Check database connection and list tables'

    def handle(self, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                # Get list of all tables
                cursor.execute("""
                    SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE = 'BASE TABLE'
                """)
                tables = cursor.fetchall()
                
                self.stdout.write(self.style.SUCCESS('Successfully connected to database'))
                self.stdout.write('Existing tables:')
                for table in tables:
                    self.stdout.write(f'- {table[0]}')
                
                # Check if our specific table exists
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME = 'chatbot_api_trainingdata'
                """)
                exists = cursor.fetchone()[0]
                if exists:
                    self.stdout.write(self.style.SUCCESS('chatbot_api_trainingdata table exists'))
                else:
                    self.stdout.write(self.style.ERROR('chatbot_api_trainingdata table does not exist'))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Database error: {str(e)}')) 
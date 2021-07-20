The test data uses the Faker module. 
Therefore, there is a possibility of an error such as:

 sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint.

Restart the test to resolve the error.
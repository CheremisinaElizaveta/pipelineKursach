import psycopg2
import datetime
from testapp.settings import DATABASES


def get_dump(host, port, username, password, db_name, output_file):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            dbname=db_name
        )
        
        cursor = conn.cursor()

        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)

        tables = cursor.fetchall()

        with open(output_file, "w", encoding="utf-8") as f:
            for table in tables:
                table_name = table[0]
                cursor.copy_expert(f"COPY {table_name} TO STDOUT WITH CSV HEADER;", f)

        cursor.close()
        conn.close()

        print(f"Backup created successfully and saved as {output_file}")

    except Exception as e:
        raise Exception(f"Can't create dump: {e}")


def make_backup():
    config = DATABASES['default']

    format_date = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
    output_file = f"backup_{format_date}.sql"

    get_dump(config['HOST'], config['PORT'], config['USER'], config['PASSWORD'], config['NAME'], output_file)


if __name__ == "__main__":
    print("Making backup...")
    make_backup()
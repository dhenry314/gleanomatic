from datetime import datetime, timedelta

startTime = datetime.combine(datetime.today() - timedelta(1), datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': startTime,
    'email': ['dhenry@mohistory.org'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
}

sources = {
        "frbstl": {
            "name":"Federal Reserve Bank of St. Louis",
            "sets": {
                "fraser": {
                     "OAISource":"https://fraser.stlouisfed.org/oai",
                     "OAIMetaDataPrefix":"mods"
                }
            }
        },
        "umsl": {
            "name": "University of Missouri - St. Louis",
            "sets": {
                "dl": {
                     "OAISource":"http://dl.mospace.umsystem.edu/umsl/oai2",
                     "OAIMetaDataPrefix":"mods"
                }
            }
        },
        "umkc": {
            "name": "University of Missouri- Kansas City",
            "sets": {
                "dl": {
					"OAISource":"http://dl.mospace.umsystem.edu/umkc/oai2",
					"OAIMetaDataPrefix":"mods"
                }
            }
        }
}

import os
import pyodbc
import redis


class BaseSetting:
    debug = os.getenv("DJANGO_SETTING_DEBUG", False)


class Terraform:
    # DEBUG FALSE
    terraform_base_path = os.getenv("TERRAFORM_BASE_PATH", "/opt/terraform/")
    terraform_resources_path = os.getenv("TERRAFORM_RESOURCES_PATH", "/opt/terraform_resources/")
    terraform_queue_path = os.getenv("TERRAFORM_QUEUE_PATH", "/opt/terraform_queue/queue.json")
    terraform_log_path = os.getenv("TERRAFORM_LOG_PATH", "/opt/terraform_log/logs.json")

    # DEBUG TRUE
    local_terraform_base_path = os.getenv("LOCAL_TERRAFORM_BASE_PATH", "./terraform/")
    loca_terraform_resources_path = os.getenv("LOCA_TERRAFORM_RESOURCES_PATH", "./terraform_resources/")
    local_terraform_queue_path = os.getenv("LOCAL_TERRAFORM_QUEUE_PATH", "./terraform_queue/queue.json")
    local_terraform_log_path = os.getenv("LOCAL_TERRAFORM_LOG_PATH", "./terraform_log/logs.json")

    delay = int(os.getenv("TERRAFORM_DELAY", 10))


class UTM:
    utm_path = os.getenv("UTM_PATH", "172.24.1.33:1443")
    utm_token = os.getenv("UTM_TOKEN", "75c3qpdG4QnG58jb1zpw996b36zyzH")

    # utm_path = os.getenv("UTM_PATH", "172.20.26.148")
    # utm_token = os.getenv("UTM_TOKEN", "17dfhsz6t4N80yxq60q7fcny30Qmng")

    utm_user = os.getenv("UTM_USER", "admin")
    utm_password = os.getenv("UTM_PASSWORD", "123456aA")

    utm_interfaces_api = os.getenv("UTM_INTERFACES_API", 'api/v2/cmdb/system/interface')
    utm_services_api = os.getenv("UTM_SERVICES_API", 'api/v2/cmdb/firewall.service/custom')
    utm_interfaces_path = f'https://{utm_path}/{utm_interfaces_api}'


class Database:
    db_name = os.getenv("LANSWEEPER_DB_NAME", "lansweeperdb")
    host = os.getenv("LANSWEEPER_DB_HOST", "s2-asset-srv")
    port = int(os.getenv("LANSWEEPER_DB_PORT", 1433))
    user = os.getenv("LANSWEEPER_DB_USER", "Automation")
    password = os.getenv("LANSWEEPER_DB_PASSWORD", '2wsx3edc@WSX#EDC')
    odbc_driver = pyodbc.drivers()[0]


class LDAP:
    server_name = os.getenv("LDAP_SERVER_NAME", 'DC01.asax.local')
    server_ip = os.getenv("LDAP_SERVER_IP", '172.20.28.41')
    password = os.getenv("LDAP_PASSWORD", 'pYt8FggTaqvyD%hU')
    username = os.getenv("LDAP_USER_NAME", 'UTMAuto_ACC')
    bind_user = os.getenv("LDAP_BIND_USER",
        'CN=UTM Auto Service Account,OU=Service Account;OU=Users,OU=ASAX Objects,DC=asax,DC=local')
    groups_dn = os.getenv("LDAP_GROUPS_DN", 'OU=UTM ACCESS,OU=Groups,OU=ASAX Objects,DC=asax,DC=local')


class Celery:
    celery_broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379")
    celery_result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")


class Redis:
    host = os.getenv("REDIS_HOST", "localhost")
    port = os.getenv("REDIS_PORT", 6379)
    db = os.getenv("REDIS_DB", 1)
    queue_name = os.getenv("REDIS_QUEUE_NAME", "utm_queue")
    redis_client = redis.Redis(host=host, port=port, db=db)
    redis_cache_location = os.getenv("REDIS_CACHE_LOCATION", "redis://localhost:6379/2")


class ElasticSearch:
    host = os.getenv("ELASTIC_HOST", "http://st-log-elk")
    port = os.getenv("ELASTIC_PORT", 9200)
    index = os.getenv("ELASTIC_INDEX", 'utm_automation_log')
    pipeline = os.getenv("ELASTIC_PIPELINE", 'DateChanger')
    api_key = os.getenv("ELASTIC_API_KEY", 'NzJYMWZJMEJMT2dZcnQ5Ri1lUTQ6dTE0MDZQSk1SbkMyeG5NUWMzQjNvQQ==')


class RabbitMQ:
    # host = os.getenv("RABBITMQ_HOST", "http://st-log-elk")
    host = os.getenv("RABBITMQ_HOST", "172.28.33.6")
    port = os.getenv("RABBITMQ_PORT", 5672)
    exchange = os.getenv("RABBITMQ_EXCHANGE", 'utm_automation_log')
    routing_key = os.getenv("RABBITMQ_ROUTING_KEY", 'logstash')
    username = os.getenv("RABBITMQ_USERNAME", 'pusheradmin')
    password = os.getenv("RABBITMQ_PASSWORD", '1qaz!QAZ')
    queue_name = os.getenv("RABBITMQ_QUEUE_NAME", 'utm_automation_log')

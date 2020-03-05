import os
import re
from contextlib import contextmanager
from functools import wraps
import random

import environ
from fabric.api import env, cd, prefix, sudo as _sudo, run as _run, hide, task
from fabric.colors import yellow, green, blue, red
from fabric.contrib.files import exists, upload_template, append
from fabric.operations import local, put

REPO_URL = "https://github.com/JimInCO/bishopric_tools.git"
site_name = "bishopric_tools"
venv_name = "bishopric_tools_prod"

conf = environ.Env()
conf.read_env(".env")
env.db_pass = conf("DB_PASS", None)
env.locale = conf("LOCALE", default="en_US.UTF-8")
env.key_filename = conf("SSH_KEY_PATH", None)
env.user = conf("SSH_USER", None)
env.password = conf("SSH_PASS", None)
env.sudo_password = conf("SSH_PASS", None)
env.forward_agent = True
env.proj_name = site_name
env.server_folder = f"/home/{env.user}/{site_name}_django"
env.proj_path = env.server_folder
env.site_folder = f"{env.server_folder}/{site_name}"
env.venv_home = f"{env.server_folder}/envs"
env.venv_path = f"{env.venv_home}/{venv_name}"
env.manage = f"{env.venv_path}/bin/python {env.site_folder}/manage.py"
env.reqs_path = f"{env.site_folder}/requirements/production.txt"
env.short_desc = "bishopric"
env.domains = conf.list("DJANGO_ALLOWED_HOSTS", default=[""])
env.domains_nginx = " ".join(env.domains)

##################
# Template setup #
##################

# Each template gets uploaded at deploy time, only if their
# contents has changed, in which case, the reload command is
# also run.

templates = {
    "nginx": {
        "local_path": "deploy/nginx.conf",
        "remote_path": "/etc/nginx/sites-available/%(proj_name)s.conf",
        "reload_command": "systemctl restart nginx",
    },
    "gunicorn": {
        "local_path": f"deploy/{env.short_desc}.service",
        "remote_path": f"/etc/systemd/system/{env.short_desc}.service",
        "reload_command": f"systemctl restart {env.short_desc}",
    },
    "socket": {
        "local_path": f"deploy/{env.short_desc}.socket",
        "remote_path": f"/etc/systemd/system/{env.short_desc}.socket",
    },
}

######################################
# Context for virtualenv and project #
######################################


@contextmanager
def virtualenv():
    """
    Runs commands within the project's virtualenv.
    """
    with cd(env.venv_path):
        with prefix("source %s/bin/activate" % env.venv_path):
            yield


@contextmanager
def project():
    """
    Runs commands within the project's directory.
    """
    with virtualenv():
        with cd(env.site_folder):
            yield


@contextmanager
def app_project():
    """
    Runs commands within the project's directory.
    """
    with cd(env.venv_home + "/" + env.app_name + "/" + env.app_dir):
        yield


###########################################
# Utils and wrappers for various commands #
###########################################


def _print(output):
    print()
    print(output)
    print()


def print_command(command):
    _print(blue("$ ", bold=True) + yellow(command, bold=True) + red(" ->", bold=True))


def get_latest_source():
    """
    The server will end up with whatever code is currently checked out on your machine (as long as you’ve pushed it up
    to the server. Another common gotcha!). We reset --hard to that commit, which will blow away any current changes
    in the server’s code directory.
    """
    with cd(env.site_folder):
        if exists(".git"):
            run("git fetch")
        else:
            run("git init .")
            run("git config http.sslverify false --local")
            run(f"git remote add origin {REPO_URL}")
            run(f"git fetch")
            run(f"git pull origin master")
        current_commit = local("git log -n 1 --format=%H", capture=True)
        run(f"git reset --hard {current_commit}")


@task
def run(command, show=True):
    """
    Runs a shell comand on the remote server.
    """
    if show:
        print_command(command)
    with hide("running"):
        return _run(command)


@task
def sudo(command, show=True):
    """
    Runs a command as sudo.
    """
    if show:
        print_command(command)
    with hide("running"):
        return _sudo(command)


def log_call(func):
    @wraps(func)
    def logged(*args, **kawrgs):
        header = "-" * len(func.__name__)
        _print(green("\n".join([header, func.__name__, header]), bold=True))
        return func(*args, **kawrgs)

    return logged


def get_templates():
    """
    Returns each of the templates with env vars injected.
    """
    injected = {}
    for name, data in templates.items():
        injected[name] = dict([(k, v % env) for k, v in data.items()])
    return injected


def clean_endlines(s):
    s.replace("\n", "").replace("\r", "").strip()
    return s


def upload_template_and_reload(name, reload=True):
    """
    Uploads a template only if it has changed, and if so, reload a
    related service.
    """
    template = get_templates()[name]
    local_path = template["local_path"]
    if not os.path.exists(local_path):
        project_root = os.path.dirname(os.path.abspath(__file__))
        local_path = os.path.join(project_root, local_path)
    remote_path = template["remote_path"]
    reload_command = template.get("reload_command")
    owner = template.get("owner")
    mode = template.get("mode")
    remote_data = ""
    if exists(remote_path):
        with hide("stdout"):
            remote_data = sudo("cat %s" % remote_path, show=False)
    with open(local_path, "r") as f:
        local_data = f.read()
        # Escape all non-string-formatting-placeholder occurrences of '%':
        local_data = re.sub(r"%(?!\(\w+\)s)", "%%", local_data)
        if "%(db_pass)s" in local_data:
            env.db_pass = db_pass()
        local_data %= env

    if clean_endlines(remote_data) == clean_endlines(local_data):
        return
    upload_template(local_path, remote_path, env, use_sudo=True, backup=False)
    if owner:
        sudo("chown %s %s" % (owner, remote_path))
    if mode:
        sudo("chmod %s %s" % (mode, remote_path))
    if reload_command and reload:
        sudo(reload_command)


def update_dot_env():
    append(".env", "DJANGO_DEBUG_FALSE=y")
    append(".env", f"SITENAME={env.host}")
    current_contents = run("cat .env")
    if "DJANGO_SECRET_KEY" not in current_contents:
        new_secret = "".join(random.SystemRandom().choices("abcdefghijklmnopqrstuvwxyz0123456789", k=50))
        append(".env", f"DJANGO_SECRET_KEY={new_secret}")


def update_static_files():
    manage("collectstatic --noinput")


def db_pass():
    """
    Prompts for the database password if unknown.
    """
    if not env.db_pass:
        env.db_pass = input("Enter the database password: ")
    return env.db_pass


@task
def apt(packages):
    """
    Installs one or more system packages via apt.
    """
    return sudo("apt-get install -y -q " + packages)


@task
def pip(packages):
    """
    Installs one or more Python packages within the virtual environment.
    """
    with virtualenv():
        return sudo(f"pip install {packages}")


def postgres(command):
    """
    Runs the given command as the postgres user.
    """
    show = not command.startswith("psql")
    return run("sudo -u root sudo -u postgres %s" % command, show=show)


@task
def psql(sql, show=True):
    """
    Runs SQL against the project's database.
    """
    out = postgres('psql -c "%s"' % sql)
    if show:
        print_command(sql)
    return out


@task
def backup(filename):
    """
    Backs up the database.
    """
    return postgres("pg_dump -Fc %s > %s" % (env.proj_name, filename))


@task
def python(code, show=True):
    """
    Runs Python code in the project's virtual environment, with Django loaded.
    """
    setup = "import os; os.environ['DJANGO_SETTINGS_MODULE']='config.settings.production';import django;django.setup();"
    full_code = 'python -c "%s%s"' % (setup, code.replace("`", "\\\`"))  # noqa W605
    with project():
        result = run(full_code, show=False)
        if show:
            print_command(code)
    return result


def static():
    """
    Returns the live STATIC_ROOT directory.
    """
    return python("from django.conf import settings;" "print(settings.STATIC_ROOT)", show=False).split("\n")[-1]


@task
def manage(command, settings="config.settings.production"):
    """
    Runs a Django management command.
    """
    return run(f"{env.manage} {command} --settings {settings}")


#########################
# Install and configure #
#########################


@task
@log_call
def install():
    """
    Installs the base system and Python requirements for the entire server.
    """
    locale = f"LC_ALL={env.locale}"
    with hide("stdout"):
        if locale not in sudo("cat /etc/default/locale"):
            sudo("update-locale %s" % locale)
            run("exit")
    sudo("apt-get update -y -q")
    apt("python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl git-all")
    apt("nodejs npm")
    sudo("pip3 install --upgrade pip")
    sudo("pip3 install virtualenv")


@task
@log_call
def create():
    """
    Create a new virtual environment for a project.
    Pulls the project's repo from version control, adds system-level
    configs for the project, and initialises the database with the
    live host.
    """

    # Create the correct folders
    run(f"mkdir -p {env.site_folder}")
    run(f"mkdir -p {env.server_folder}/envs")
    run(f"mkdir -p {env.server_folder}/logs")

    # Create virtualenv
    with cd(env.venv_home):
        if not exists(f"{venv_name}/bin/pip"):
            run(f"virtualenv --python=python3.7 {venv_name}")

    # Get the latest source or create a new repo
    get_latest_source()

    with cd(env.site_folder):
        # Add .env file
        project_root = os.path.dirname(os.path.abspath(__file__))
        put(f"{project_root}/.env", ".")
        sudo(f"chmod 600 .env")
        update_dot_env()

        # Compile and update the js and css files
        run("npm install")
        run("npm run build")

        # Static Files
        update_static_files()

        # Check to see if the database already exists
        if postgres(f"psql -l | grep {env.proj_name} | wc -l") == 0:
            # Create DB and DB user.
            pw = db_pass()
            new_pw = pw.replace("'", "'")
            user_sql = f"CREATE USER {env.proj_name} WITH ENCRYPTED PASSWORD '{new_pw}';"
            psql(user_sql, show=False)
            shadowed = "*" * len(pw)
            print_command(user_sql.replace(f"'{pw}'", f"{shadowed}"))
            psql(f"CREATE DATABASE {env.proj_name} WITH OWNER {env.proj_name};")
            psql(f"ALTER ROLE {env.proj_name} SET client_encoding TO 'utf8';")
            psql(f"ALTER ROLE {env.proj_name} SET default_transaction_isolation TO 'read committed';")
            psql(f"ALTER ROLE {env.proj_name} SET timezone TO 'UTC';")
            psql(f"GRANT ALL PRIVILEGES ON DATABASE {env.proj_name} TO {env.proj_name};")

    # Migrate
    manage("migrate")

    # Set up project.
    with project():
        # Requirements
        if env.reqs_path:
            pip(f"-r {env.reqs_path}")

    # Gunicorn Templates
    upload_template_and_reload("socket", reload=False)
    upload_template_and_reload("gunicorn", reload=False)
    sudo(f"systemctl start {env.short_desc}.socket")
    sudo(f"systemctl enable {env.short_desc}.socket")

    # Ngnix Template
    upload_template_and_reload("nginx")
    nginx_link = f"/etc/nginx/sites-enabled/{env.proj_name}.conf"
    if not exists(nginx_link):
        sudo(f"sudo ln -s /etc/nginx/sites-available/{env.proj_name}.conf {nginx_link}")

    # Firewall
    sudo("ufw allow 'Nginx Full'")

    return True


@task
@log_call
def deploy():
    """
    Deploy latest version of the project.
    Check out the latest version of the project from version control, install new requirements, migrate the database,
    collect any new static assets, and restart gunicorn's work processes for the project.
    """

    with project():
        # Backup the database
        backup("last.db")
        # Backup the static directory
        static_dir = static()
        if exists(static_dir):
            run("tar -cf last.tar %s" % static_dir)
        # Store the last commit
        run("git rev-parse HEAD > last.commit")

        # Get the latest version of the code
        get_latest_source()
        # Update the requirements
        pip(f"-r {env.reqs_path}")
        # Migrate the database
        manage("migrate")
        # Update the static files
        update_static_files()

    # Restart gunicorn process
    sudo(templates["gunicorn"]["reload_command"])

    return True

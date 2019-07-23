from fabric import Connection
from fabric import task

env = {
    'project_name': 'netmesh',
    'path': '/var/www/netmesh',
    'release': 'current',
    'upload_path': 'netmesh',
    'project_folder': 'netmesh',
    'media_folder': 'media',
    'http_server': 'gunicorn_nginx',
    'database': 'postgre'
}


@task
def lab(ctx):
    c = Connection(host='192.168.40.10',
                   user='vagrant',
                   port=22,
                   connect_kwargs={
                       "passphrase": "vagrant"
                   },
                   )
    setup(c)
    upload_tar_from_git(c)
    install_requirements(c)
    install_http_server(c)
    restart_http_server(c)
    install_database(c)
    restart_services(c)


def setup(c):
    print('***Doing setup...***')
    c.sudo('apt update')
    c.sudo('apt install -y python python3-setuptools python3-pip')
    c.sudo('apt install -y unzip')
    c.sudo('apt install -y postgresql libpq-dev')
    c.sudo('apt install -y byobu git supervisor daemontools binutils libproj-dev gdal-bin')
    c.sudo('mkdir -p %(path)s' % env)
    c.sudo('chown -R www-data:www-data %(path)s/' % env)
    c.run('mkdir -p %(upload_path)s' % env)
    c.run('cd %(upload_path)s; mkdir -p releases; mkdir -p packages' % env)


def install_requirements(c):
    print('***Installing pip requirements...***')
    c.sudo('pip3 install -r %(upload_path)s/releases/%(release)s/requirements-dev.txt'
         % env, pty=True)


def upload_tar_from_git(c):
    print('***Upload tar from git***')
    """Create an archive from the current Git master branch
    and upload it.
    """
    # require('release', provided_by=[deploy, setup])
    # with c.local('cd ../%(project_folder)s' % env):
        # UNCOMMENT TO GIT ARCHIVE FROM MASTER
        # local('git archive --format=zip master > %(release)s.zip' % env )
        # local('git archive --format=zip plugins > %(release)s.zip' % env )
    c.local('zip -r %(release)s.zip . ' % env)
    c.local('ls -l')
    c.put('%(release)s.zip' % env, '%(upload_path)s/packages/' % env)
    c.run('mkdir -p %(upload_path)s/releases/%(release)s' % env)
    c.run(
        'cd %(upload_path)s/releases/%(release)s && unzip ../../packages/%(release)s.zip'
        % env, pty=False)
    c.local('rm %(release)s.zip' % env)
    c.sudo('cp -r %(upload_path)s/releases/%(release)s/* %(path)s/' % env)


def install_http_server(c):
    print('***Install HTTP server...***')
    c.sudo('apt-get -y install nginx')
    c.sudo('pip3 install envdir')
    c.sudo('pip3 install gunicorn')
    install_site(c)
    install_gunicorn_nginx_confs(c)


def install_site(c):
    print('***Install site part 1... ***')
    c.sudo('cp -r %(upload_path)s/releases/%(release)s/* %(path)s/' % env)
    media_folder = '%(path)s/%(media_folder)s/' % env
    c.sudo('chown -R www-data:www-data %s' % media_folder)
    # c.sudo('if [ -a /etc/nginx/sites-enabled/default ]; then unlink /etc/nginx/sites-enabled/default; fi' % env)
    c.sudo('unlink /etc/nginx/sites-enabled/default' % env)
    c.sudo('cp %(path)s/deploy/nginx/nginx.conf /etc/nginx/nginx.conf' % env)


def install_gunicorn_nginx_confs(c):
    print('***Installing gunicorn & nginx confs...***')
    c.sudo('cp %(path)s/deploy/gunicorn/gunicorn_start.sh /bin/gunicorn_start.sh' % env)
    c.sudo('chown www-data:www-data /bin/gunicorn_start.sh')
    c.sudo('chmod u+x /bin/gunicorn_start.sh')
    c.sudo('mkdir -p /etc/nginx/sites-enabled/')
    c.sudo('cp %(path)s/deploy/gunicorn/netmesh_nginx.conf '
         '/etc/nginx/sites-enabled/netmesh_nginx.conf'
         % env)
    c.sudo('cp %(path)s/deploy/gunicorn/netmesh_gunicornd.conf '
         '/etc/supervisor/conf.d/netmesh_gunicornd.conf'
         % env)


def install_database(c):
    print('***Install database...***')
    """Create the database tables for all apps in INSTALLED_APPS
    whose tables have not already been created"""
    if env["database"] == 'postgre':
        c.run('sudo -u postgres psql -d template1 -c '
            '"CREATE DATABASE netmesh;" || true')
        c.run('sudo -u postgres psql -d netmesh -c '
            '"CREATE USER netmesh WITH PASSWORD \'netmesh\'; '
            'GRANT ALL PRIVILEGES ON DATABASE netmesh to netmesh;" || true')

    print('***Install django site...***')
    c.sudo('envshell %(path)s/envdir_prod')
    c.sudo('python3 %(path)s/manage.py makemigrations' % env)
    c.sudo('python3 %(path)s/manage.py migrate' % env)
    # c.sudo('python manage.py loaddata netmesh/fixtures/config.json'
    #      % env)
    # cmd = 'echo \"from django.contrib.auth.models import User; ' \
    #       'User.objects.create_superuser(' \
    #       '\'netmesh\', \'netmesh@example.com\', \'netmesh\')\" ' \
    #       '| python manage.py shell'
    # c.sudo(cmd % env)
    c.sudo('echo \"yes\" | sudo python3 %(path)s/manage.py collectstatic' % env)
    # c.sudo('cp -r %(path)s/static/ %(path)s/netmesh/' % env)


def restart_http_server(c):
    c.sudo('service nginx restart', pty=True)


def tune_server(c):
    c.sudo('echo \'fs.file-max=500000\' >> /etc/sysctl.conf' % env)
    # c.sudo('echo \'net.core.somaxconn=128\' >> /etc/sysctl.conf' % env)
    c.sudo('sysctl -p' % env)

    c.sudo('echo \'www-data  soft  nofile  1024\' >> '
         '/etc/security/limits.conf' % env)
    c.sudo('echo \'www-data  hard  nofile  4096\' >> '
         '/etc/security/limits.conf' % env)

def restart_services(c):
    c.sudo('service supervisor restart')
    c.sudo('service nginx restart')

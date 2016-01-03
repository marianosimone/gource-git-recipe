import gravatar
import os
import subprocess
import sys

def safe_makedirs(path):
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

def get_commiters(repo_path):
    log_command = 'git log --pretty=format:"%ae|%an"'
    try:
        result = subprocess.check_output('cd {path} && {log_command}'.format(path=repo_path, log_command=log_command), shell=True)
        return map(lambda line: line.split('|'), set(result.split('\n')))
    except subprocess.CalledProcessError:
        return []

def save_avatars(users, base_path):
    print 'Getting avatars for commiters'
    safe_makedirs(base_path)
    for email, name in users:
        gravatar.download(email, os.path.join(base_path, '{name}.png'.format(name=name)), size=100)

def generate_visualization(repo_path):
    print 'Generating the visualization'
    cd_command = 'cd {repo_path}'.format(repo_path=repo_path)
    gource_command = 'gource --load-config gource.conf --user-image-dir .git/avatars --stop-at-end --o  - '
    output_command = 'ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 1 -threads 0 -bf 0 gource.mp4'
    full_command = '{cd_command} && {gource_command} | {output_command}'.format(cd_command=cd_command, gource_command=gource_command, output_command=output_command)
    print 'Running', full_command
    subprocess.check_output(full_command, shell=True)

if __name__ == '__main__':
    repo_path = os.path.abspath('.')  # TODO: get from args
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        print "{repo_path} doesn't seem to be a git repo".format(repo_path=repo_path)
        sys.exit(1)
    commiters = get_commiters(repo_path)
    if not commiters:
        print "Couldn't find any commiters in repo {repo_path}".format(repo_path=repo_path)
        sys.exit(1)
    save_avatars(commiters, os.path.join(repo_path, '.git', 'avatars'))
    generate_visualization(repo_path)

import os
import glob
import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--update", default=False, help="Update atlantis.yaml")
args = parser.parse_args()

TRUTHY = (1,'1','t','y','yes')

environments_folder = './environments'

base_atlantis_template = """version: 2
projects:
{projects}
"""

atlantis_template = """- name: {name}
  dir: environments/{env}/{app}
  workspace: default
  autoplan:
    when_modified: ["*.tf", secrets.auto.tfvars']
    enabled: true
  apply_requirements: {apply_requirements}
"""

def obj_name(env, app):
  return '{}-{}'.format(env, app)
2


def apply_requirements(env):
    if env in ['prod']:
        return '[approved]'
    return '[]'


def run(atlantis):
    templates = []

    for env in [f.name for f in os.scandir(environments_folder) if f.is_dir()]:
        for app in [f.name for f in os.scandir(os.path.join(environments_folder, env)) if f.is_dir()]:
            #import pdb;pdb.set_trace()
            layer_instance_name = obj_name(env, app)
            # check we dont have it already
            if not any(layer_instance_name for project in atlantis.get('projects', []) if project.get('name') == layer_instance_name):
                templates.append(atlantis_template.format(name=layer_instance_name,
                                                            env=env,
                                                            app=app,
                                                            apply_requirements=apply_requirements(env)))

    return templates

if __name__ == '__main__':
    with open('atlantis.yaml', 'r') as f:
        atlantis = yaml.load(f)

    templates = run(atlantis)
    # add to projects
    [atlantis['projects'].append(yaml.load(item)[0]) for item in templates]
    updated_atlantis_yaml = yaml.dump(atlantis, encoding=None, default_flow_style=False)
    if args.update in TRUTHY:
        print('{}\nUpdating atlanits.yaml with new data\n{}'.format(15*'****', 15*'****'))
        with open('atlantis.yaml', 'w') as f:
            yaml.dump(atlantis, f, encoding=None, default_flow_style=False)
    #atlantis_yaml = base_atlantis_template.format(projects=''.join(templates))
    print(updated_atlantis_yaml)
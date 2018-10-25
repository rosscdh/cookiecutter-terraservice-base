import os
import yaml
"""
├── environments
│   ├── dev
│   │   ├── iam
│   │   │   ├── main.tf
│   │   │   ├── secrets.auto.tfvars
│   │   │   └── terraform.tfvars
│   │   └── network
│   │       ├── main.tf
│   │       ├── secrets.auto.tfvars
│   │       └── terraform.tfvars
│   └── prod
│       ├── iam
│       │   ├── main.tf
│       │   ├── secrets.auto.tfvars
│       │   └── terraform.tfvars
│       └── network
│           ├── main.tf
│           ├── secrets.auto.tfvars
│           └── terraform.tfvars
├── layers
│   ├── iam
│   └── network
└── modules
    ├── subnets
    └── vpc
"""

data = yaml.load("""
layout:
    files:
        environments:
            - README.md
            - main.tf
            - secrets.auto.tfvars
            #- terraform.tfvars  ## not needed as this level implements the config directly
        layers:
            - README.md
            - main.tf
            - variables.tf
            - outputs.tf
        modules:
            - README.md
            - variables.tf
            - main.tf
            - outputs.tf
    environments:
        - dev
    layers:
        - network
    modules:
        - vpc
        - peering
        
""")


ENVS = data.get('layout').get('environments')
LAYERS = data.get('layout').get('layers')
MODULES = data.get('layout').get('modules')

SERVICE_FILES = data.get('layout').get('files').get('environments')
LAYER_FILES = data.get('layout').get('files').get('layers')
MODULE_FILES = data.get('layout').get('files').get('modules')

for env in ENVS:
    for layer in LAYERS:
        print('mkdir -p environments/{env}/{layer}'.format(env=env, layer=layer))
        for f in SERVICE_FILES:
            filename = 'environments/{env}/{layer}/{f}'.format(env=env, layer=layer, f=f)
            if not os.path.exists(filename):
                print('touch {filename}'.format(filename=filename))

for layer in LAYERS:
    print('mkdir -p layers/{layer}'.format(layer=layer))
    for f in LAYER_FILES:
        filename = 'layers/{layer}/{f}'.format(layer=layer, f=f)
        if not os.path.exists(filename):
            print('touch {filename}'.format(filename=filename))

for module in MODULES:
    print('mkdir -p modules/{module}'.format(module=module))
    for f in MODULE_FILES:
        filename = 'modules/{module}/{f}'.format(module=module, f=f)
        if not os.path.exists(filename):
            print('touch {filename}'.format(filename=filename))
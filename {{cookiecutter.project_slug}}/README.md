# {{ cookiecutter.project_name }

landscape layout help you work with terraservices for terraform

* https://www.youtube.com/watch?v=wgzgVm7Sqlk
* https://www.slideshare.net/opencredo/hashidays-london-2017-evolving-your-infrastructure-with-terraform-by-nicki-watt
* https://www.hibri.net/2017/11/13/terraform-for-grownups/


**Example layout**

This layout lets us abstract and reuse layers and control the variables at the environment level

1. *environments* implement *layers*
2. *layers* implement interfaces to *modules*


### Environment - Instances

`Environment instances` allow us to implement an `instance` of a `layer` module with `environment specific configuration`

* **DO NOT** refer to modules directly in the environments layer, rather reference them as `source '../../../layers/module-name'` and then inject the variables at the environment level
* **DO** check that each remote s3 state refers to its own file i.e. `terraform/state/:your-username/:environment/:app_name` - `terraform/state/ross.crawford/dev/atlantis`


### Layers

`Layers` allow us to combine a number of `modules`.

* Think of a situation where we want to interchange a module, we want to be able to reuse the variables defined at this layer for use in the environments
* always abstract the variables for modules into variables.tf; this allows environments to simply make a reference and pass in their specific variables
* **DO NOT** refer to modules directly in the environments layer, rather reference them as `source '../../../layers/module-name'` and then inject the variables. 


### Modules

`Modules` act as normal terraform modules and provide access to the standard concept.

* Place all your custom built modules here


``` bash
├── environments
│   ├── dev
│   │   ├── iam
│   │   │   ├── README.md
│   │   │   ├── main.tf
│   │   │   ├── secrets.auto.tfvars
│   │   │   └── terraform.tfvars
│   │   └── network
│   │       ├── README.md
│   │       ├── main.tf
│   │       ├── secrets.auto.tfvars
│   │       └── terraform.tfvars
│   └── prod
│       ├── iam
│       │   ├── README.md
│       │   ├── main.tf
│       │   ├── secrets.auto.tfvars
│       │   └── terraform.tfvars
│       └── network
│           ├── README.md
│           ├── main.tf
│           ├── secrets.auto.tfvars
│           └── terraform.tfvars
├── layers
│   ├── iam
│   │   ├── README.md
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── variables.tf
│   └── network
│       ├── README.md
│       ├── main.tf
│       ├── outputs.tf
│       └── variables.tf
└── modules
    ├── subnets
    │   ├── README.md
    │   ├── main.tf
    │   ├── outputs.tf
    │   └── variables.tf
    └── vpc
        ├── README.md
        ├── main.tf
        ├── outputs.tf
        └── variables.tf
```


## But but this is allot of work

* Yes, having to go into each environment-service and apply state is painful, but this is why we have [Terrastorm](https://github.com/rosscdh/terrastorm)
* Terrastorm lets you `terrastorm run dev plan iam network someotherservice anotherservice` (`terrastorm run :environment :cmd :service_name|all`)
* That and [Atlantis](https://runatlantis.io) will ensure that we have an auditable state transition thats managed and transparent to all.


### atlantis.py

Setup atlantis to run in the terraserivces layout per service

* run this whenever you add a new **environment** `layer` instance
* it will place that new instance into the atlantis.yaml

``` bash
python atlantis.py                  # preview the atlantis output
python atlantis.py --update y       # update with new values
```


### layout.py

Setup directory structure via yaml file

``` bash
python layout.py         # preview the layout
python layout.py | bash  # make it go
```
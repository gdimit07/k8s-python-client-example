from cmath import e
import os
import yaml
from kubernetes import client,config

config.load_kube_config()

crd_definition = 'crd.yaml'

with client.ApiClient() as api_client:
    api_instance = client.ApiextensionsV1Api(api_client)
    try:
        current_crds = [x['spec']['names']['kind'].lower() for x in api_instance.list_custom_resource_definition().to_dict()['items']]

        if 'exchangerate' not in current_crds:
            print("creating exchangerate definition")
            with open(crd_definition) as data:
                body = yaml.safe_load(data)
            api_instance.create_custom_resource_definition(body)

    except client.rest.ApiException as e:
        if e.status == 409: 
            print("CRD already exists")
        else:
            raise e
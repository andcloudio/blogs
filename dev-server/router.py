""" Create nat router """  

from utils import GlobalComputeUrl

def GenerateConfig(context):
  project = context.env['project']
  name = context.properties['network'] + '-router'
  network = context.properties['network']
  region = context.properties['region']

  resources = [{
    'name': name,
    'type': 'compute.v1.router',
    'properties': {
      'name': name,
      'network': GlobalComputeUrl(project,
                            'networks',
                            network), 
      'region': region,
      'nats': [{
        'name': name + '-nat-config',
        'sourceSubnetworkIpRangesToNat': 'ALL_SUBNETWORKS_ALL_IP_RANGES',
        'natIpAllocateOption': 'AUTO_ONLY',
      }]
    }
  }]

  return {'resources': resources}
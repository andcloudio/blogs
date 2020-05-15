""" Create compute instance """

from utils import GlobalComputeUrl, ZonalComputeUrl, RegionComputeUrl

def GenerateConfig(context):
  project = context.env['project']
  name = '%s-%s' % (project, '-dev-server')
  network = context.properties['network']
  region = context.properties['region']
  subnet = '%s-%s' % (network,region)
  zone = context.properties['zone']
  machineType = context.properties['machineType']
  os = context.properties['os']
  image = context.properties['image']
  tag = context.properties['tag']

  resources = [{
    'name': name,
    'type': 'compute.v1.instance',
    'properties': {
      'name': 'webserver',
      'zone': zone,
      'machineType': ZonalComputeUrl(project,
                                    zone,
                                    'machineTypes',
                                    machineType),
      'networkInterfaces': [{
        'network': GlobalComputeUrl(project,
                                    'networks',
                                    network), 
        'subnetwork': RegionComputeUrl(project,
                            region,
                            'subnetworks',
                            subnet),                     
        }],
      'disks': [{
        'deviceName': name,
        'type': 'PERSISTENT',
        'autoDelete': False,
        'boot': True,
        'initializeParams': {
          'sourceImage': GlobalComputeUrl(os,
                                          'images/family',
                                          image),
          'diskSizeGb': '10',
          },
        }],
      'tags': {
        'items': [
          tag
          ],
        }
      }
    }]

  return {'resources': resources}

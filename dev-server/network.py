""" Create network and subnetworks """  

def GenerateConfig(context):
  name = context.env['name']

  resources = [{
    'name': name,
    'type': 'compute.v1.network',
    'properties': {
      'name': name,
      'autoCreateSubnetworks': False, 
    }
  }]

  for subnet in context.properties['subnets']:
    resources.append({
      'name': '%s-%s' % (name, subnet['region']),
      'type': 'compute.v1.subnetwork',
      'properties': {
        'name': '%s-%s' % (name, subnet['region']),
        'description': 'subnework of %s in %s' % (name, subnet['region']),
        'ipCidrRange': subnet['cidr'],
        'region': subnet['region'],
        'network': '$(ref.%s.selfLink)' % name,
      },
      'metadata': {
        'dependsOn': [
          name,
        ]
      }
    })
  
  return {'resources': resources}
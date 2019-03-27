from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.gcp.resources.projects import Projects
from ScoutSuite.providers.gcp.resources.gce.regions import Regions

class RegionSubnetworks(Resources):
    def __init__(self, gcp_facade, project_id, region):
        self.gcp_facade = gcp_facade
        self.project_id = project_id
        self.region = region

    async def fetch_all(self):
        raw_subnetworks = await self.gcp_facade.gce.get_subnetworks(self.project_id, self.region)
        for raw_subnetwork in raw_subnetworks:
            subnetwork_id, subnetwork = self._parse_subnetwork(raw_subnetwork)
            self[nasubnetwork_idme] = subnetwork

    def _parse_subnetwork(self, raw_subnetwork):
        subnetwork_dict = {}
        subnetwork_dict['id'] = raw_subnetwork['id']
        subnetwork_dict['project_id'] = raw_subnetwork['selfLink'].split('/')[-5]
        subnetwork_dict['region'] = raw_subnetwork['region'].split('/')[-1]
        subnetwork_dict['name'] = "%s-%s" % (raw_subnetwork['name'], subnetwork_dict['region'])
        subnetwork_dict['subnetwork'] = raw_subnetwork['network'].split('/')[-1]
        subnetwork_dict['gateway_address'] = raw_subnetwork['gatewayAddress']
        subnetwork_dict['ip_range'] = raw_subnetwork['ipCidrRange']
        subnetwork_dict['creation_timestamp'] = raw_subnetwork['creationTimestamp']
        subnetwork_dict['private_ip_google_access'] = raw_subnetwork['privateIpGoogleAccess']
        return subnetwork_dict['id'], subnetwork_dict


class Subnetworks(Regions):
    async def fetch_all(self):
        super(Subnetworks, self).fetch_all()
        for project_id in self['projects'].keys():
            for region in self['projects'][project_id]['regions'].keys():
                region_subnetworks = RegionSubnetworks(self.gcp_facade, project_id, region)
                await region_subnetworks.fetch_all()
                self['projects'][project_id]['regions'][region]['subnetworks'] = region_subnetworks
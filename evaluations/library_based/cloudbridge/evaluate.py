from evaluations import system
from evaluations.decorator import Decorators
from cloudbridge.cloud.factory import CloudProviderFactory, ProviderList
import os
from cloudbridge.cloud.interfaces.resources import TrafficDirection
from cloudbridge.cloud.interfaces import InstanceState

class Evaluation:
    def __init__(self, cloudbridge_aws_access_key, cloudbridge_aws_secret_key,cloudbridge_azure_subscription_id, cloudbridge_azure_client_id, cloudbridge_azure_secret, cloudbridge_azure_tenant):
        
        self.cloudbridge_aws_access_key = cloudbridge_aws_access_key
        self.cloudbridge_aws_secret_key = cloudbridge_aws_secret_key
	self.cloudbridge_azure_subscription_id=cloudbridge_azure_subscription_id
	self.cloudbridge_azure_client_id=cloudbridge_azure_client_id
	self.cloudbridge_azure_secret=cloudbridge_azure_secret
	self.cloudbridge_azure_tenant=cloudbridge_azure_tenant
        self.providers=[]
        self.image_id=None
	self.keypair=None
	self.net=None
	self.subnet=None
	self.router=None
	self.gateway=None
	self.firewall=None
	self.instance=None
	self.floating_ip=None

   

    @Decorators.tagging('AWS:Provider:Create')
    @Decorators.python_consumption()
    @Decorators.timing()
    def create_aws_client(self, aws_access_key=None, aws_secret_key=None):
        if not aws_access_key:
            aws_access_key = self.cloudbridge_aws_access_key
        if not aws_secret_key:
            aws_secret_key = self.cloudbridge_aws_secret_key
        config = {'aws_access_key': aws_access_key,
          'aws_secret_key': aws_secret_key}
	self.providers.append(CloudProviderFactory().create_provider(ProviderList.AWS, config))
	self.image_id = 'ami-aa2ea6d0'  # Ubuntu 16.04 (HVM)


    @Decorators.tagging('AZURE:Provider:Create')
    @Decorators.python_consumption()
    @Decorators.timing()
    def create_azure_provider(self):
	config = {'azure_subscription_id': self.cloudbridge_azure_subscription_id,
          'azure_client_id': self.cloudbridge_azure_client_id,
          'azure_secret': self.cloudbridge_azure_secret,
          'azure_tenant': self.cloudbridge_azure_tenant}
	self.providers.append(CloudProviderFactory().create_provider(ProviderList.AZURE, config))
	self.image_id = 'Canonical:UbuntuServer:16.04.0-LTS:latest'  # Ubuntu 16.04
	print 'azure'
   
    @Decorators.tagging('*:Provider:List')
    @Decorators.python_consumption()
    @Decorators.timing()
    def list_provider_resources(self):
	#self.provider.security.firewalls.list()
	self.providers[0].compute.vm_types.list()
	self.providers[0].storage.snapshots.list()
	self.providers[0].storage.buckets.list()

    @Decorators.tagging('*:Provider:Delete')
    @Decorators.python_consumption()
    @Decorators.timing()
    def delete_provider(self):
        del self.providers[0]

    @Decorators.tagging('*:KeyPair:Create')
    @Decorators.python_consumption()
    @Decorators.timing()
    def create_key_pair(self):
	self.keypair = self.providers[0].security.key_pairs.create('cloudbridge-intro')
	with open('cloudbridge_intro.pem', 'w') as f:
            f.write(self.keypair.material)
	os.chmod('cloudbridge_intro.pem', 0o400)

    @Decorators.tagging('*:KeyPair:Retrieve')
    @Decorators.python_consumption()
    @Decorators.timing()
    def retrieve_keypair(self,keypair_id):
	self.keypair = self.providers[0].security.key_pairs.get(keypair_id)
	
    @Decorators.tagging('*:KeyPair:Find')
    @Decorators.python_consumption()
    @Decorators.timing()
    def find_keypair(self,name,kp_list=[]):
	kp_list = self.providers[0].security.key_pairs.find(name=name)
	self.keypair = kp_list[0]

    @Decorators.tagging('*:KeyPair:Delete')
    @Decorators.python_consumption()
    @Decorators.timing()
    def delete_keypair(self):
	self.keypair.delete()
	os.remove('cloudbridge_intro.pem')

    @Decorators.tagging('*:Network:Create')
    @Decorators.python_consumption()
    @Decorators.timing()
    def create_network(self):
	self.net = self.providers[0].networking.networks.create(cidr_block='10.0.0.0/16',
                                          label='my-network')
	self.subnet = self.net.create_subnet(cidr_block='10.0.0.0/28', label='my-subnet')
	self.router = self.providers[0].networking.routers.create(network=self.net, label='my-router')
	self.router.attach_subnet(self.subnet)
	self.gateway = self.net.gateways.get_or_create_inet_gateway()
	self.router.attach_gateway(self.gateway)

    @Decorators.tagging('*:Network:Retrieve')
    @Decorators.python_consumption()
    @Decorators.timing()
    def retrieve_network(self,net_id,net_list=[]):
	self.net = self.providers[0].networking.networks.get(net_id)
	
    @Decorators.tagging('*:Network:Findbyname')
    @Decorators.python_consumption()
    @Decorators.timing()
    def find_network_by_name(self,name,net_list=[]):
	net_list = self.providers[0].networking.networks.find(name=name)
	self.net = net_list[0]

    @Decorators.tagging('*:Network:Findbylabel')
    @Decorators.python_consumption()
    @Decorators.timing()
    def find_network_by_label(self,label,net_list=[]):
	net_list = self.providers[0].networking.networks.find(label=label)
	self.net = net_list[0]

    @Decorators.tagging('*:Network:RetrieveSubnet')
    @Decorators.python_consumption()
    @Decorators.timing()
    def retrieve_subnet(self,subnet_id):
	self.subnet = self.providers[0].networking.subnets.get(subnet_id)
	
    @Decorators.tagging('*:Network:FindsubnetUN')
    @Decorators.python_consumption()
    @Decorators.timing()
    def find_subnet_un(self,name,sn_list=[]):
	sn_list = self.providers[0].networking.subnets.find(name=name)
	self.subnet = sn_list[0]

    @Decorators.tagging('*:Network:FindsubnetUL')
    @Decorators.python_consumption()
    @Decorators.timing()
    def find_subnet_ul(self,label,sn_list=[]):
	sn_list = self.providers[0].networking.subnets.find(label=label)
	self.subnet = sn_list[0]

    @Decorators.tagging('*:Network:FindsubnetKN')
    @Decorators.python_consumption()
    @Decorators.timing()
    def find_subnet_kn(self,name,sn_list=[]):
	sn_list = self.providers[0].networking.subnets.find(network=self.net.id,name=name)
	self.subnet = sn_list[0]

    @Decorators.tagging('*:Network:FindsubnetKL')
    @Decorators.python_consumption()
    @Decorators.timing()
    def find_subnet_kl(self,label,sn_list=[]):
	sn_list = self.providers[0].networking.subnets.find(network=self.net.id,label=label)
	self.subnet = sn_list[0]

    @Decorators.tagging('*:Network:RetrieveRouter')
    @Decorators.python_consumption()
    @Decorators.timing()
    def retrieve_router(self,router_id):
	self.router = self.providers[0].networking.routers.get(router_id)
	
    @Decorators.tagging('*:Network:Findrouterbyname')
    @Decorators.python_consumption()
    @Decorators.timing()
    def find_routerbyname(self,name, router_list=[]):
	router_list = self.providers[0].networking.routers.find(name=name)
	self.router = router_list[0]

    @Decorators.tagging('*:Network:Findrouterbylabel')
    @Decorators.python_consumption()
    @Decorators.timing()
    def find_routerbylabel(self,label, router_list=[]):
	router_list = self.providers[0].networking.routers.find(label=label)
	self.router = router_list[0]

    @Decorators.tagging('*:Network:RetrieveGateway')
    @Decorators.python_consumption()
    @Decorators.timing()
    def retrieve_gateway(self):
	self.gateway = self.net.gateways.get_or_create_inet_gateway()


    @Decorators.tagging('*:Network:CreateFirewall')
    @Decorators.python_consumption()
    @Decorators.timing()
    def create_firewall(self):
	self.firewall = self.providers[0].security.vm_firewalls.create(
    label='cloudbridge-intro', description='A VM firewall used by CloudBridge', network_id=self.net.id)
	self.firewall.rules.create(TrafficDirection.INBOUND, 'tcp', 22, 22, '0.0.0.0/0')

    @Decorators.tagging('*:Network:RetrieveFirewall')
    @Decorators.python_consumption()
    @Decorators.timing()
    def retrieve_firewall(self,firewall_id):
	self.firewall = self.providers[0].security.vm_firewalls.get(firewall_id)
	
    @Decorators.tagging('*:Network:Findfirewallbyname')
    @Decorators.python_consumption()
    @Decorators.timing()
    def find_firewallbyname(self,name,fw_list=[]):
	fw_list = self.providers[0].security.vm_firewalls.find(name=name)
	self.firewall = fw_list[0]

    @Decorators.tagging('*:Network:Findfirewallbylabel')
    @Decorators.python_consumption()
    @Decorators.timing()
    def find_firewallbylabel(self,label,fw_list=[]):
	fw_list = self.providers[0].security.vm_firewalls.find(name=name)
	self.firewall = fw_list[0]

    @Decorators.tagging('*:Network:DeleteFirewall')
    @Decorators.python_consumption()
    @Decorators.timing()
    def delete_firewall(self):
	self.firewall.delete()

    @Decorators.tagging('*:Instance:Launch')
    @Decorators.python_consumption()
    @Decorators.timing()
    def launch_instance(self,img=None,zone=None,vm_type=None):
	img = self.providers[0].compute.images.get(self.image_id)
	zone = self.providers[0].compute.regions.get(self.provider.region_name).zones[0]
	vm_type = sorted([t for t in self.providers[0].compute.vm_types
                  if t.vcpus >= 2 and t.ram >= 4],
                  key=lambda x: x.vcpus*x.ram)[0]
	self.instance = self.providers[0].compute.instances.create(
    image=img, vm_type=vm_type, label='cloudbridge-intro',
    subnet=self.subnet, zone=zone, key_pair=self.keypair, vm_firewalls=[self.firewall])
	# Wait until ready
	self.instance.wait_till_ready()  # This is a blocking call
	# Show instance state
	self.instance.state
	# 'running'

    @Decorators.tagging('*:Instance:Retrieve')
    @Decorators.python_consumption()
    @Decorators.timing()
    def retrieve_instance(self, instance_id):
	self.instance = self.providers[0].compute.instances.get(instance_id)
	
    @Decorators.tagging('*:Instance:Findbyname')
    @Decorators.python_consumption()
    @Decorators.timing()
    def find_instancebyname(self,name,inst_list=[]):
	inst_list = self.providers[0].compute.instances.list(name=name)
	self.instance = inst_list[0]

    @Decorators.tagging('*:Instance:Findbylabel')
    @Decorators.python_consumption()
    @Decorators.timing()
    def find_instancebylabel(self,label,inst_list=[]):
	inst_list = self.providers[0].compute.instances.list(label=label)
	self.instance = inst_list[0]

    @Decorators.tagging('*:Instnce:AssignIP')
    @Decorators.python_consumption()
    @Decorators.timing()
    def assign_public_ip(self):
	self.floating_ip= self.gateway.floating_ips.create()
	self.instance.add_floating_ip(self.floating_ip)
	self.instance.refresh()
	self.instance.public_ips

    @Decorators.tagging('*:Instnce:Delete')
    @Decorators.python_consumption()
    @Decorators.timing()
    def delete_instance(self):
	self.instance.delete()
	self.instance.wait_for([InstanceState.DELETED, InstanceState.UNKNOWN],
               terminal_states=[InstanceState.ERROR])  # Blocking call	
    
    @Decorators.tagging('*:Network:RetrieveIP')
    @Decorators.python_consumption()
    @Decorators.timing()
    def retrieve_ip(self, flotingip_id):
	self.floating_ip = self.gateway.floating_ips.get(flotingip_id)
	
    @Decorators.tagging('*:Network:Findfipbyip')
    @Decorators.python_consumption()
    @Decorators.timing()
    def findfipbyip(self,ip,fip_list=[]):
	fip_list = self.gateway.floating_ips.find(public_ip=ip)
	self.floating_ip = fip_list[0]

    @Decorators.tagging('*:Network:Findfipbyname')
    @Decorators.python_consumption()
    @Decorators.timing()
    def findfipbyname(self,name,fip_list=[]):
	fip_list = self.net.gateways.floating_ips.find(name=name)
	self.floating_ip = fip_list[0]

    @Decorators.tagging('*:Network:Findfipbylabel')
    @Decorators.python_consumption()
    @Decorators.timing()
    def findfipbylabel(self,label,fip_list=[]):
	fip_list = self.net.gateways.floating_ips.find(label=label)
	self.floating_ip = fip_list[0]

    @Decorators.tagging('*:Network:Deleteip')
    @Decorators.python_consumption()
    @Decorators.timing()
    def delete_ip(self):
	self.floating_ip.delete()

    @Decorators.tagging('*:Network:Delete')
    @Decorators.python_consumption()
    @Decorators.timing()
    def delete_network(self):
	self.router.detach_gateway(self.gateway)
	self.router.detach_subnet(self.subnet)
	self.gateway.delete()
	self.router.delete()
	self.subnet.delete()
	self.net.delete()
    
	

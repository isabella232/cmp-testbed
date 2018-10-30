import os
from evaluations import system
from evaluations.decorator import Decorators

class Evaluation:
    def __init__(self,cloudify_aws_access_key,cloudify_aws_secret_key):
	self.cloudify_aws_access_key=cloudify_aws_access_key
	self.cloudify_aws_secret_key=cloudify_aws_secret_key
       
    @Decorators.tagging('*:System:Start')
    @Decorators.timing()
    def start_system(self):
    	os.system('sudo docker run --name cfy_manager_local -d --restart unless-stopped -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --security-opt seccomp:unconfined --cap-add SYS_ADMIN -p 80:80 -p 8000:8000 cloudifyplatform/community:18.10.4')


    @Decorators.tagging('*:System:Stop')
    @Decorators.timing()
    def stop_system(self):
    	os.system('sudo docker stop cfy_manager_local')

    @Decorators.tagging('*:System:Remove')
    @Decorators.timing()
    def remove_system(self):
    	os.system('sudo docker rm cfy_manager_local')

    
        

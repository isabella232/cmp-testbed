from evaluations.docker_based.manageiq.evaluate import Evaluation as ManageIQ
from evaluations.docker_compose_based.mistio.evaluate import Evaluation as MistIO
from evaluations.library_based.libcloud.evaluate import Evaluation as Libcloud
from evaluations.website.cloudcheckr.evaluate import Evaluation as CloudCheckR
from evaluations.library_based.boto_aws.evaluate import Evaluation as BotoAWS
from evaluations.library_based.cloudbridge.evaluate import Evaluation as cloudbridge
from evaluations.docker_based.cloudify.evaluate import Evaluation as cloudify
from evaluations import system


system_folder = system.config_validation('System_Configuration', 'system_folder')
aws_access_key = system.config_validation('AWS_Configuration', 'aws_access_key')
aws_secret_key = system.config_validation('AWS_Configuration', 'aws_secret_key')
azure_subscription_id=system.config_validation('Azure_Configuration', 'azure_subscription_id')
azure_client_id=system.config_validation('Azure_Configuration', 'azure_client_id')
azure_secret=system.config_validation('Azure_Configuration', 'azure_secret')
azure_tenant=system.config_validation('Azure_Configuration', 'azure_tenant')
mistio_token = system.config_validation('Mist_Configuration', 'mist_token')
cloudcheckr_access_key = system.config_validation('CloudcheckR_Configuration', 'cloudcheckr_admin_token')

registered_clients = {
    'mistio': MistIO(mist_aws_access_key=aws_access_key,
                     mist_aws_secret_key=aws_secret_key,
                     mist_token=mistio_token,
                     mist_home_directory=system_folder+'mistio'),
    'libcloud': Libcloud(libcloud_aws_access_key=aws_access_key,
                         libcloud_aws_secret_key=aws_secret_key,
                         libcloud_home_directory=system_folder + 'libcloud'),
    'boto_aws': BotoAWS(aws_access_key=aws_access_key,
                        aws_secret_key=aws_secret_key),
    'cloudcheckr': CloudCheckR(cloudcheckr_aws_access_key=aws_access_key,
                               cloudcheckr_aws_secret_key=aws_secret_key,
                               cloudcheckr_admin_access_key=cloudcheckr_access_key),
    'manageiq': ManageIQ(manageiq_aws_access_key=aws_access_key,
                         manageiq_aws_secret_key=aws_secret_key,
                         manageiq_home_directory=system_folder+'manageiq'),
    'cloudbridge': cloudbridge(cloudbridge_aws_access_key=aws_access_key,
                         cloudbridge_aws_secret_key=aws_secret_key, cloudbridge_azure_subscription_id=azure_subscription_id, cloudbridge_azure_client_id=azure_client_id, cloudbridge_azure_secret=azure_secret, cloudbridge_azure_tenant=azure_tenant),
    'cloudify': cloudify(cloudify_aws_access_key=aws_access_key, cloudify_aws_secret_key=aws_secret_key)
}

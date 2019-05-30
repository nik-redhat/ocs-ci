"""
Defaults module
"""
import os
from getpass import getuser

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TOP_DIR = os.path.dirname(THIS_DIR)
TEMPLATE_DIR = os.path.join(TOP_DIR, "templates/ocs-deployment/")

# This module is automatically loaded with variables defined in
# conf/ocsci/default_config.yaml in its DEFAULTS section.
# If the variable can be used in some config file sections from ocsci/config.py
# module, plese put your defaults rather to mentioned default_config.yaml file!

# See the documentation in conf/README.md file to understand this config file.

# Those variables are duplicate at the moment from default_config.yaml and once
# we drop support for old runner we will remove those variables from here and
# will have them defined only on one place.

# Be aware that variables defined below are not used anywhere in th config
# files and their sections when we rendering config!

INSTALLER_VERSION = '4.1.0-rc.3'
CLIENT_VERSION = INSTALLER_VERSION
AWS_REGION = 'us-east-2'
ROOK_CLUSTER_NAMESPACE = 'openshift-storage'
KUBECONFIG_LOCATION = 'auth/kubeconfig'  # relative from cluster_dir
CLUSTER_NAME = f"ocs-ci-cluster-{getuser()}"
API_VERSION = "v1"
CEPH_IMAGE = "ceph/ceph:v14.2.0-20190410"
ROOK_IMAGE = "rook/ceph:master"
DEPLOYMENT_PLATFORM = 'AWS'

# This section is suppose to be available just from ocsci/config.py module from
# ENV_DATA dictionary. Once we drop support of old runner we will delete this
# data from here as well.
ENV_DATA = {
    'platform': DEPLOYMENT_PLATFORM,
    'cluster_name': CLUSTER_NAME,
    'cluster_namespace': ROOK_CLUSTER_NAMESPACE,
    'region': AWS_REGION,
    'ceph_image': CEPH_IMAGE,
    'rook_image': ROOK_IMAGE,
}
STORAGE_API_VERSION = 'storage.k8s.io/v1'
ROOK_API_VERSION = 'ceph.rook.io/v1'
OCP_API_VERSION = 'project.openshift.io/v1'
OPENSHIFT_REST_CLIENT_API_VERSION = 'v1'

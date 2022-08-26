import logging

from ocs_ci.ocs import constants
from ocs_ci.framework.testlib import (
    ManageTest,
    tier1,
    polarion_id,
    ms_consumer_required,
)
from ocs_ci.ocs.resources.storageclassclaim import create_storageclassclaim
from ocs_ci.helpers.helpers import create_ocs_object_from_kind_and_name

log = logging.getLogger(__name__)


@tier1
@polarion_id("OCS-4628")
@ms_consumer_required
class TestStorageClassClaim(ManageTest):
    """
    Tests to verify storageclassclaim
    """

    def test_verify_storageclassclaim(
        self, project_factory, teardown_factory, create_pvcs_and_pods
    ):
        """
        Test case to verify storageclassclaim

        """
        # Create a project
        proj_obj = project_factory()
        sc_claim_obj_rbd = create_storageclassclaim(
            interface_type=constants.CEPHBLOCKPOOL, namespace=proj_obj.namespace
        )

        log.info("Creating storageclassclaims")
        sc_claim_obj_cephfs = create_storageclassclaim(
            interface_type=constants.CEPHBLOCKPOOL, namespace=proj_obj.namespace
        )
        teardown_factory(sc_claim_obj_rbd)
        teardown_factory(sc_claim_obj_cephfs)

        log.info(f"Waiting for storageclassclaim {sc_claim_obj_rbd.name} to be Ready")
        sc_claim_obj_rbd.ocp.wait_for_resource(
            condition=constants.STATUS_READY,
            resource_name=sc_claim_obj_rbd.name,
            column="PHASE",
            resource_count=1,
        )

        log.info(
            f"Waiting for storageclassclaim {sc_claim_obj_cephfs.name} to be Ready"
        )
        sc_claim_obj_cephfs.ocp.wait_for_resource(
            condition=constants.STATUS_READY,
            resource_name=sc_claim_obj_cephfs.name,
            column="PHASE",
            resource_count=1,
        )

        # Get OCS object of kind storageclass for both the storageclasses created by storageclassclaims
        sc_obj_rbd = create_ocs_object_from_kind_and_name(
            kind=constants.STORAGECLASS,
            resource_name=sc_claim_obj_rbd.name,
            namespace=proj_obj.namespace,
        )
        sc_obj_cephfs = create_ocs_object_from_kind_and_name(
            kind=constants.STORAGECLASS,
            resource_name=sc_claim_obj_cephfs.name,
            namespace=proj_obj.namespace,
        )

        log.info("Creating PVCs and pods")
        self.pvcs_rbd, self.pods_rbd = create_pvcs_and_pods(
            pvc_size=3, num_of_cephfs_pvc=0, sc_rbd=sc_obj_rbd
        )
        self.pvcs_cephfs, self.pods_cephfs = create_pvcs_and_pods(
            pvc_size=3, num_of_rbd_pvc=0, sc_rbd=sc_obj_cephfs
        )
        log.info("Created PVCs and pods")

        # Start IO
        log.info("Starting IO on all pods")
        for pod_obj in self.pods_rbd + self.pods_cephfs:
            storage_type = (
                "block"
                if pod_obj.pvc.volume_mode == constants.VOLUME_MODE_BLOCK
                else "fs"
            )
            pod_obj.run_io(
                storage_type=storage_type,
                size="1G",
                runtime=20,
                fio_filename="file1",
                end_fsync=1,
            )
            log.info(f"IO started on pod {pod_obj.name}")
        log.info("Started IO on all pods")

        # Wait for IO to finish
        log.info("Wait for IO to finish on pods")
        for pod_obj in self.pods_rbd + self.pods_cephfs:
            pod_obj.get_fio_results()
            log.info(f"IO finished on pod {pod_obj.name}")
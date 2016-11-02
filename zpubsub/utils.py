import logging
import os
import shutil
import zmq.auth

LOG = logging.getLogger(__name__)


def load_key_pair(keys_dir, name, generate_on_fail=False):
    """
    keys live at {keys_dir}/{name}.secret|public.key
    """
    public_file = os.path.join(keys_dir, '{}.public.key'.format(name))
    secret_file = os.path.join(keys_dir, '{}.secret.key'.format(name))

    if not os.path.isfile(secret_file):
        if generate_on_fail:
            LOG.info("Generating key pair at {}".format(public_file))
            pub_tmp, sec_tmp = zmq.auth.create_certificates(
                keys_dir, name
            )
            shutil.move(pub_tmp, public_file)
            shutil.move(sec_tmp, secret_file)
        else:
            raise RuntimeError('No secret key at {}'.format(secret_file))

    public, secret = zmq.auth.load_certificate(secret_file)
    return public, secret

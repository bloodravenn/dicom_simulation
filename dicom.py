import os
from pydicom import dcmread
from pydicom.uid import JPEGBaseline
from pynetdicom import AE, StoragePresentationContexts
from pynetdicom.sop_class import CTImageStorage

def send_dicom_to_pacs(dicom_folder, pacs_ip, pacs_port, pacs_ae_title):
    # Create an Application Entity
    ae = AE(ae_title='MODALITY')
    ae.supported_contexts = StoragePresentationContexts

    # Add the requested transfer syntax for the X-Ray Angiographic Image Storage context
    ae.add_requested_context('1.2.840.10008.5.1.4.1.1.12.1', [JPEGBaseline])


 # Add TLS layer for encryption
    # tls_context = build_context('TLS')
    # tls_context.load_cert_chain(pacs_certificate, private_key)
    # ae.add_supported_context(CTImageStorage, tls_context)

    # Connect to the PACS server
    assoc = ae.associate(pacs_ip, pacs_port, ae_title=pacs_ae_title)
    if assoc.is_established:
        print('Connected to the PACS server.')

        # Iterate over DICOM files in the folder
        for filename in os.listdir(dicom_folder):
            if filename.endswith('.DCM'):
                dicom_file = os.path.join(dicom_folder, filename)

                # Read the DICOM file
                dataset = dcmread(dicom_file)

                # Send the DICOM image to the PACS server
                status = assoc.send_c_store(dataset)

                # Check the status of the storage request
                if status:
                    print(f'Successfully sent {dicom_file} to the PACS server.')
                else:
                    print(f'Failed to send {dicom_file} to the PACS server.')

        # Release the association
        assoc.release()
        print('Disconnected from the PACS server.')
    else:
        print('Failed to connect to the PACS server.')

# Usage example
dicom_folder = r'C:\Users\bloodraven\Desktop\02_Projects\DT\dicom'
pacs_ip = '192.168.0.162'  # Replace with the actual IP address
pacs_port = 4242  # Replace with the actual port number
pacs_ae_title = 'ORTHANC'  # Replace with the actual AE title

# pacs_certificate = '/path/to/certificate.pem'  # Replace with the path to your certificate
# private_key = '/path/to/private_key.pem'  # Replace with the path to your private key


send_dicom_to_pacs(dicom_folder, pacs_ip, pacs_port, pacs_ae_title)
#send_dicom_to_pacs(dicom_folder, pacs_ip, pacs_port, pacs_ae_title, pacs_certificate, private_key)

# Sealed Cargo

Forensics, Medium · [Polski](README.md)

I converted the qcow2 image to raw and went through the partition with Sleuth Kit (`fls`, `icat`). From the scripts in the podman container layers I learned that the manifest is encrypted with AES-256-CBC and the AES key and IV are encrypted with RSA-OAEP. The private key had been "deleted" in a later overlayfs layer but was still in a lower one, so I extracted it with `icat` and used it to decrypt the manifest with `openssl`.

Scripts: [solve.sh](solve.sh)

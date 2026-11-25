# Sealed Cargo

Forensics, Medium · [English](README.en.md)

Obraz qcow2 przekonwertowałem na raw i przejrzałem partycję narzędziami Sleuth Kit (`fls`, `icat`). Ze skryptów w warstwach kontenera podmana wyczytałem, że manifest jest zaszyfrowany AES-256-CBC, a klucz AES i IV są zaszyfrowane RSA-OAEP. Klucz prywatny był „usunięty” w późniejszej warstwie overlayfs, ale nadal leżał w niższej, więc wyciągnąłem go przez `icat` i odszyfrowałem nim manifest w `openssl`.

Skrypty: [solve.sh](solve.sh)

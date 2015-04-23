# flaming-skunk
Flaming lights for Fleet Admiral Skunk's ship, USB Cloudbuster (http://www.scul.org/skynet2.0/public/ship/view/entity_id/1370)

### Installation ###

1. Copy libpruio-0.2 binary from compilation of `src/examples/1.bas` to `/usr/local/bin/read-adc` and mark as executable.

2. `git clone git@github.com:rascalmicro/flaming-skunk.git`

3. Add file to `/etc/supervisor/conf.d` to start `flames.py` at boot.

4. Get libpruio initialized properly.

5. Put `fcserver.json` at `/etc/fcserver.json` and update the Fadecandy serial in the file to the correct one, which you can get from `dmesg`.

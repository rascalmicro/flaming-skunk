Flaming lights for Fleet Admiral Skunk's ship, USB Cloudbuster (http://www.scul.org/skynet2.0/public/ship/view/entity_id/1370)

Works on the Rascal 2, available at http://rascalmicro.com

### Installation ###

1. `git clone git@github.com:rascalmicro/flaming-skunk.git`

2. Move `sternoslomo.conf` to `/etc/supervisor/conf.d/sternoslomo.conf` to start `flames.py` at boot.

3. Put `fcserver.json` at `/etc/fcserver.json` and update the Fadecandy serial in the file to the correct one, which you can get from `dmesg`.

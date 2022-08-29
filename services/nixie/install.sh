#!/bin/bash
sudo cp services/nixie/nixie_clock.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/nixie_clock.service
sudo systemctl daemon-reload
sudo systemctl enable nixie_clock.service
sudo systemctl restart nixie_clock.service
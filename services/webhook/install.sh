#!/bin/bash
sudo cp services/webhook/nixie_webhook_clock.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/nixie_webhook_clock.service
sudo systemctl daemon-reload
sudo systemctl enable nixie_webhook_clock.service
sudo systemctl restart nixie_webhook_clock.service
# Kiasu Cybersecurity Masterplan Setup Guide 🇸🇬🛡️

Welcome to the ultra-paranoid Linux setup guide. Since these commands require `sudo` access, review them carefully and execute them into your SSH terminal one-by-one.

## Phase 4: OS-Level Autopilot (Unattended Upgrades)
This ensures the Linux kernel and SSH firewall are silently patched every night at 3 AM against Zero-Day CVE vulnerabilities, using built-in Ubuntu mechanisms.

```bash
# 1. Install & Enable Ubuntu Unattended Upgrades
sudo apt-get update
sudo apt-get install unattended-upgrades apt-listchanges -y
sudo dpkg-reconfigure -plow unattended-upgrades

# Answer "Yes" to automatically download and install stable updates.

# 2. Verify the configuration
sudo cat /etc/apt/apt.conf.d/20auto-upgrades
# It should output:
# APT::Periodic::Update-Package-Lists "1";
# APT::Periodic::Unattended-Upgrade "1";
```

---

## Phase 3: Zero-Bandwidth CVE Auto-Patcher
Instead of looping and wasting server bandwidth, this starts a lightweight Webhook listener on Port 8080. When GitHub detects a CVE or a new code push, it triggers the payload flawlessly.

### Step 1: Grant Passwordless Bot Restart
To allow the auto-updater webhook to intelligently restart the bot without prompting for your `sudo password` over HTTP:
```bash
echo "be1987r ALL=(ALL) NOPASSWD: /bin/systemctl restart berry-brain-bot" | sudo tee /etc/sudoers.d/berry-brain-bot
```

### Step 2: Test the Webhook Live
Run the python script we pushed:
```bash
cd ~/kiasu_security
python3 auto_updater.py
```

### Step 3: Setup GitHub Automation
1. Go to your GitHub Repository -> **Settings** -> **Webhooks** -> **Add Webhook**
2. Payload URL: `http://89.127.232.133:8080/` (OR your cloudflare tunnel endpoint)
3. Content Type: `application/json`
4. Secret: `super_kiasu_secret` (Change this in `.env` or hardcode it in `auto_updater.py` later).
5. Let me select individual events: **Tick "Pull requests" and "Pushes"**. Wait for Dependabot to automatically open PRs when a CVE is found!

## Phase 2: Tailscale VPN (The Ghost Protocol) 👻
*To be executed later to prevent SSH lockout as discussed.*

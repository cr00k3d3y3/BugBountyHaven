# Bug Bounty Haven

**A Complete Training Lab for Aspiring Bug Bounty Hunters**

---

Bug Bounty Haven is a self-hosted, intentionally vulnerable web application suite designed for hands-on practice in web security testing, exploit development, and real-world bug bounty methodologies.

Built to simulate authentic attack surfaces with training wheels, this lab is ideal for beginners looking to sharpen their skills and move confidently toward paid bug bounty work.

---

## 🎯 Key Features

* **SQLi Playground** – Classic, Union, Blind, Time-based, and Stacked SQL Injections.
* **XSS Playground** – Reflected, Stored, and DOM-based XSS scenarios.
* **LFI WebApp** – File upload exploitation, LFI chaining, and reverse shell triggering.
* **Recon Modules** – Simulates `.git/config`, `.env`, `robots.txt`, and `.DS_Store` leakages.
* **Campaign Mode** – Track progress, hints, flag submissions, and scoreboard.
* **Moderation Engine** – Feedback injection moderation, review panel, and flagging system.

---

## 🚀 Quick Start

```bash
git clone https://[github.com/yourusername/bug-bounty-haven.git](https://github.com/cr00k3d3y3/BugBountyHaven)
cd bug-bounty-haven
docker-compose up --build
```

Then navigate to:

* SQLi Playground → [http://localhost:8081](http://localhost:8081)
* XSS Playground → [http://localhost:8082/stored](http://localhost:8082/stored)
* LFI Playground → [http://localhost:8083](http://localhost:8083)

---

## 📚 Learning Focus

* Real-world exploit simulation with guided hints
* Logging, analysis, and campaign-style challenges
* Ethical hacking techniques mapped to OWASP Top 10
* Safe, local, private testing environment

---

## 💡 Freemium & Future Versions

* **Free Version:** Full SQLi/XSS/LFI lab with campaign tracking.
* **Premium Add-on (Coming Soon):**

  * Multi-user scoring + challenge flags
  * Reverse shell command analysis + payload detectors
  * Additional modules (RCE, SSRF, Auth Bypass, etc)
  * Community CTF mode

---

## 🤝 Contributing

Pull requests are welcome! Submit bug fixes, new challenges, or UI improvements.

---

## 🛡️ Disclaimer

This application is intended for **ethical learning purposes only**. Do not deploy to public-facing environments.

---

## 📫 Contact

For questions, feedback, or to collaborate: \[[ded3y3@proton.me](mailto:ded3y3@proton.me)]

---

Happy hunting! 🐞🏴

> "Train like it's real. Then go make it real."

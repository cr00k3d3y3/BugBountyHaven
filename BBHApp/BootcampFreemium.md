# 🛡️ Bug Bounty Bootcamp Lab

### Learn to Hack. Capture Flags. Build Real-World Skills.

> A hands-on playground for aspiring bug bounty hunters, CTF competitors, and OSCP candidates. Built by hackers, for hackers.

---

## 🚀 What Is It?

An intentionally vulnerable lab environment built with Flask and Docker, simulating real-world web app vulnerabilities:

- ✅ Classic SQL Injection
- ✅ Union-based SQLi
- ✅ Blind SQLi & Time-based
- ✅ Stored & Reflected XSS
- ✅ Recon Challenges (robots.txt, .env, .git, DS_Store)
- ✅ Flag capture system with scoreboard
- ✅ Campaign mode to track your progress

No registration. No internet required. Just clone, build, and hack.

---

## 🧩 Lab Modes

### 🎓 Free Version (Freemium)
- Core SQLi/XSS labs
- Recon: robots.txt only
- Basic scoreboard
- Full flag walkthrough for classic SQLi

### 💼 Pro Unlock ($15 one-time)
- 10+ Additional Labs
  - LFI → Reverse Shell
  - JWT Theft via DOM XSS
  - .env and .git leaks
  - Admin Panel Enumeration
- Full Markdown walkthroughs (PDF)
- Hints system + flag validator
- Campaign stars + certificate generator

---

## 🔧 Setup

```bash
git clone https://github.com/yourusername/bug-bounty-bootcamp-lab.git
cd bug-bounty-bootcamp-lab
docker compose up --build
```

Then open:
- SQLi Lab → [http://localhost:8081](http://localhost:8081)
- XSS Lab → [http://localhost:8082](http://localhost:8082)
- LFI Lab → [http://localhost:8083](http://localhost:8083)

---

## 🏁 Start Hacking

Each lab includes:
- 🧪 Input fields
- 💬 Feedback forms
- 🧩 Hidden logic flaws
- 🔓 Admin/flag endpoints

Use Burp, curl, sqlmap or just your browser to explore and exploit.

---

## 🏆 Flag System

Visit `/campaign` in SQLiPlayground to track:
- Captured flags
- Challenge difficulty
- Star rating (🟢 Easy → 🔴 Hard)

Submit flags via `/submit_flag`

---

## 🛒 Upgrade to Pro

Want more? Grab the Pro Pack:

> https://yourstore.gumroad.com/l/bugbounty-lab-pro

---

## 📚 Why This Lab?

Unlike other labs:
- ✅ No login, cloud, or dependencies
- ✅ 100% offline
- ✅ Realistic, chainable bugs
- ✅ Beginner-friendly and fully extensible

---

## 👨‍🏫 Who Made This?

Built by a full-time bug bounty hunter and security researcher to help others level up.

Pull requests, feedback, and suggestions welcome!

---

## 📜 License

MIT License. Use, fork, and share freely.

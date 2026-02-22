# 🛡️ Sentinel-Vault: Zero-Trust JIT IAM Architecture

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103.0-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791.svg)](https://www.postgresql.org/)
[![Security](https://img.shields.io/badge/Security-Zero%20Trust-red.svg)]()

> **Sentinel-Vault is a high-assurance Identity and Access Management (IAM) engine designed to neutralize social engineering and VoIP spoofing. It enforces mutual authentication and the "Four-Eyes Principle" using application-layer cryptography and Just-in-Time (JIT) session logic.**

🎥 **[Watch the Demo Video](https://www.youtube.com/watch?v=A0GDtUEdfQE)**

---

## 🔐 The Problem: Social Engineering
Standard MFA can be bypassed by sophisticated social engineering and caller ID spoofing. Sentinel-Vault solves this by moving the trust boundary from the "voice" to the "handshake."

### The Sentinel Solution:
1. **The Circuit Breaker:** High-risk actions (e.g., password resets, wire transfers) trigger an immediate system lock.
2. **Mutual Authentication:** An authorized agent must initiate a JIT session. 
3. **Cryptographic Handshake:** Both parties exchange system-generated, time-sensitive verification tokens.
4. **Zero-Trust Validation:** Access is only granted when the backend mathematically verifies both tokens, rendering remote spoofing attempts useless.

---

## 🏗️ Technical Architecture & SIEM Pipeline
Sentinel-Vault isn't just a login page; it’s an enterprise-ready data ecosystem designed for SOC (Security Operations Center) visibility.

* **API Framework:** Built on **FastAPI** for high-concurrency, asynchronous handling of IAM events.
* **Database:** Utilizing **PostgreSQL** via **SQLAlchemy ORM** for persistent storage of public keys and RBAC (Role-Based Access Control) policies.
* **Audit Logging:** Every handshake generates a high-fidelity JSON webhook for ingestion into simulated SIEM pipelines.
* **Security Protections:** Implements modular logic to prevent credential harvesting and unauthorized elevation of privilege.
Example>>>>>
<img width="100%" alt="Sentinel-Vault Architecture Diagram" src="https://github.com/user-attachments/assets/703e8efa-6fec-43ac-aee8-02feb75fcd92" />

---

## 🛠️ The Tech Stack
* **Backend:** Python 3.10+, FastAPI, Uvicorn
* **Database:** PostgreSQL (Relational Data & Audit Trails)
* **Logic:** Pydantic (Data Validation), ECDSA Cryptography
* **Frontend:** Vanilla JS / Tailwind CSS (Security Dashboard)

---

## 💻 Local Deployment

**1. Clone the repository**
git clone [https://github.com/padiengweb/sentinel-vault.git](https://github.com/padiengweb/sentinel-vault.git)
cd sentinel-vault
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
open attack-demo in your url and click the arrow



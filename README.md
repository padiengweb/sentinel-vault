# 🛡️ Sentinel-Vault: Zero-Trust JIT IAM Architecture

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Security](https://img.shields.io/badge/Security-Zero%20Trust-red.svg)]()

> **Sentinel-Vault is a custom Identity and Access Management (IAM) application that defeats social engineering and VoIP caller ID spoofing by enforcing mutual authentication and the Four-Eyes Principle via application-layer cryptography.**

🎥 **[Watch the Video](https://www.youtube.com/watch?v=A0GDtUEdfQE)**

---

## 🔐 The Solution: Sentinel-Vault
1. **The Circuit Breaker:** When a user initiates a high-risk request, the system locks the action. 
2. **Mutual Authentication:** A live IAM Admin (or Bank Fraud Agent) must generate a secure Just-in-Time (JIT) session. 
3. **The Handshake:** Both the user and the admin exchange distinct, system-generated codes.
4. **Zero-Trust Validation:** The system only releases the lock when both parties successfully verify the other's identity, completely neutralizing remote spoofing attacks.

---

## 🏗️ Enterprise Audit Pipeline
Security requires strict observability. Sentinel-Vault is built with a simulated enterprise DevSecOps data pipeline. Every event—whether a successful handshake or a blocked spoofing attempt—emits a high-fidelity JSON webhook.

* **API Backend:** FastAPI generates the structured JSON logs.
* **Event Routing:** Simulated **Apache NiFi** ingestion.
* **Data Masking:** Simulated **Cribl Stream** pipeline for PII redaction.
* **Data Warehouse:** Simulated **Snowflake** integration for immutable SOC audit trails.

<img width="100%" alt="Sentinel-Vault Architecture Diagram" src="https://github.com/user-attachments/assets/703e8efa-6fec-43ac-aee8-02feb75fcd92" />

---

## 💻 How to Run Locally

If you want to run the Sentinel-Vault API and UI on your local machine:

**1. Clone the repository**
```bash
git clone [https://github.com/padiengweb/sentinel-vault.git](https://github.com/padiengweb/sentinel-vault.git)
cd sentinel-vault
pip install fastapi uvicorn pydantic
uvicorn main:app --reload
open attack-demo in your url and click the arrow

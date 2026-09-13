# 🏫 Madrasa & Student Management System (Enterprise Edition)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2%2B-092E20.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-2FA%20%7C%20Audit--Logged-red.svg)](#-security--compliance)

A robust, enterprise-grade, multi-tenant capable **Madrasa & Student Management System** built with **Django**. Designed to streamline administrative tasks, student admissions, academic progress tracking, staff HR management, and high-precision accounting with complete auditability.

---

## 🌟 Key Highlights & Architecture

* **Modular Architecture**: Built with loosely-coupled Django apps (`accounts`, `core`, `students`, `academics`, `staff`, `accounting`) for extreme scalability and easy maintainability.
* **Priority Financial Management**: Features a complete double-entry style accounting system, automated cash books, fee management, staff payroll, and instant WeasyPrint PDF receipt generation.
* **Role-Based Security**: Rigid server-side enforcement (RBAC) ensuring appropriate dashboard, data, and action permissions per user level.
* **Enterprise Security Checklist**: Integrated 2FA (TOTP), Math/Image CAPTCHA, Brute-force protection, strong password policies, and full system-wide audit logging[cite: 1].

---

## 👥 Role-Based Access Control (RBAC)

| Role | Access Level & Permissions |
| :--- | :--- |
| **Super Admin** | Full system control, system-level configurations, role assignments, audit log viewing[cite: 1]. |
| **Admin** | Management across all operational modules (Students, Academics, HR, Accounting) except global system settings[cite: 1]. |
| **Accountant** | Full access to Financial/Accounting modules; read-only access to Student profiles[cite: 1]. |
| **Teacher** | Access to assigned Class/Section, attendance tracking, and marks/result entry[cite: 1]. |
| **Student** | Read-only access to personal profile, academic results, attendance, and fee status[cite: 1]. |
| **Parent / Guardian** | Read-only dashboard access monitoring linked child's results, attendance, and dues[cite: 1]. |

---

## 🧩 Core Modules & Features

### 🔐 1. Accounts & Security (`apps/accounts`)
- Custom User Model with role-based extensions[cite: 1].
- **Two-Factor Authentication (2FA / TOTP)** via Google Authenticator / Authy[cite: 1].
- **Brute-Force Lockout**: Powered by `django-axes` (5 failed login attempts trigger a 30-minute lockout)[cite: 1].
- **CAPTCHA Enforcement**: Login protection against automated bot attempts[cite: 1].
- **Audit Trails**: Logs all successful/failed authentication attempts along with IP address & timestamp[cite: 1].
- Automatic session timeout (30-minute inactivity auto-logout) and enforced initial password change[cite: 1].

### 💰 2. Accounting & Financial Management (`apps/accounting`)
- **Fee Management**: Categorized fee structures (Tuition, Admission, Exams) with automated invoice generation[cite: 1].
- **Automated PDF Receipts**: Instant PDF receipt generation embedded with dynamic QR verification codes[cite: 1].
- **Cash Book**: Real-time tracking of income/expense transactions with daily, monthly, and yearly reports[cite: 1].
- **Payroll**: Staff salary structures, monthly payslip PDF generation, and expense integration[cite: 1].
- **Accounting Integrity**: Non-destructive payment record system (Void-only transactions to preserve ledger history)[cite: 1].
- **Automated Dues Reminders**: Background tasks via Celery for SMS/Email notifications on unpaid invoices[cite: 1].

### 🎓 3. Student Management (`apps/students`)
- Automated unique Student ID generation upon admission[cite: 1].
- Guardian profile linking (multiple guardians supported per student)[cite: 1].
- Secure document storage (Birth Certificates, Photos, Identification)[cite: 1].
- Dynamic Student ID Card generation (PDF format)[cite: 1].
- Bulk class-promotion engine for academic session roll-over[cite: 1].

### 📚 4. Academics & Examination (`apps/academics`)
- Management of Classes, Sections, and Subject assignments[cite: 1].
- Daily digital attendance (QR/Biometric integration ready)[cite: 1].
- Exam configuration with customizable grading scales[cite: 1].
- Dynamic Result & Marksheet/Report Card generation (PDF export)[cite: 1].
- Routine and Timetable distribution system[cite: 1].

### 👔 5. Staff & HR Management (`apps/staff`)
- Comprehensive Teacher and Staff profile management[cite: 1].
- Staff attendance tracking & leave management workflow[cite: 1].
- Direct linkage to the payroll module for automatic monthly salary calculations[cite: 1].

---

## 🔒 Security & Compliance

- [x] **2FA (TOTP)** enforced for Admin & Accountant roles[cite: 1].
- [x] **CAPTCHA** integrated into public/login portals[cite: 1].
- [x] **Brute-Force Lockout** via IP + Username monitoring[cite: 1].
- [x] **Strict Server-Side Middleware Enforcement** (Zero reliance on client-side hiding)[cite: 1].
- [x] **CSRF Protection**, `HttpOnly` and `Secure` session cookies[cite: 1].
- [x] **Full Audit Logging** across financial transactions & authorization attempts[cite: 1].

---

## 🛠 Project Structure

```text
madrasa_management/
├── config/                  # Project configuration & settings
│   ├── settings/
│   │   ├── base.py          # Shared baseline configuration
│   │   ├── development.py   # Development settings
│   │   └── production.py    # Hardened production settings (HSTS, SSL, etc.)
├── apps/                    # Decoupled Django applications
│   ├── accounts/            # Users, RBAC, 2FA, Security logs
│   ├── core/                # System dashboard, middleware, audit logs
│   ├── students/            # Admissions, Student profiles, Guardians
│   ├── academics/           # Class, Attendance, Exams, Results
│   ├── staff/               # Teacher/Staff HR & Leaves
│   └── accounting/          # Fees, Salaries, Receipts, Cash Book
├── templates/               # Shared HTML templates (Bootstrap/Tailwind)
├── static/                  # Static assets (CSS, JS, Images)
├── media/                   # Media assets & generated PDF outputs
├── .env.example             # Environment variables blueprint
└── requirements.txt         # Project dependencies

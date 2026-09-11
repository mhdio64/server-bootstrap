[English](README.md) | [فارسی](README.fa.md)

# سرور بوت‌استرپ (server-bootstrap)

> آماده‌سازی امن، خودکار و استاندارد سرورهای Ubuntu Server (نسخه‌های 22.04 و 24.04 LTS)، Debian 13 (Trixie) و Enterprise Linux (AlmaLinux 9 و 10) به یک بیس‌لاین امن، قابل مدیریت و آماده‌ی داکر با Ansible.

پروژه `server-bootstrap` اولین جزء از مجموعه ابزار DevOps Toolkit است. این پروژه یک بستر عملیاتی، استاندارد و چندتوزیعی برای سرورهای واقعی فراهم می‌کند:

- تنظیمات پایه سیستم‌عامل، ابزارهای ضروری و همگام‌سازی زمان (`systemd-timesyncd` یا `chrony`)
- ایجاد حساب کاربری ادمین با کلید عمومی SSH و ارتقای دسترسی بدون رمز (`sudo` در دبیان/اوبونتو یا `wheel` در انترپرایز لینوکس)
- امن‌سازی SSH (Hardening) از طریق فایل drop-in اختصاصی پروژه همراه با اعتبارسنجی اولیه سینتکس و بازگشت خودکار در صورت خطا
- فایروال محلی سرور با رول‌های اختصاصی پروژه (`iptables-nft` در دبیان/اوبونتو و `firewalld` در انترپرایز لینوکس) همراه با تایمر بازیابی اضطراری (Watchdog)
- فعال‌سازی خودکار به‌روزرسانی‌های امنیتی (`unattended-upgrades` در دبیان/اوبونتو و `dnf-automatic` در انترپرایز لینوکس)
- نصب موتور رسمی Docker CE و پلاگین Docker Compose از مخازن بالادستی رسمی

## پلتفرم‌های پشتیبانی‌شده

| بخش | پشتیبانی‌شده |
|---|---|
| سیستم‌عامل‌های سرور هدف | Ubuntu Server 24.04 LTS (Noble)<br>Ubuntu Server 22.04 LTS (Jammy)<br>Debian 13.x (Trixie)<br>AlmaLinux 9.x<br>AlmaLinux 10.x |
| معماری پردازنده سرور | amd64 / x86_64 |
| سیستم‌عامل سیستم کنترل (کنترل‌نود) | لینوکس (Linux)، پایتون 3.12 تا 3.14 |
| نسخه انسیبل | `ansible-core` نسخه 2.21.x |

> جزئیات کامل و نتایج آزمون‌های واقعی در [docs/15-RELEASE-EVIDENCE.md](docs/15-RELEASE-EVIDENCE.md) و [docs/16-MULTI-DISTRO-ROADMAP.md](docs/16-MULTI-DISTRO-ROADMAP.md) درج شده است.

## راهنمای شروع سریع (Quick Start)

### ۱. آماده‌سازی محیط محلی

ابتدا مخزن را کلون کرده و وابستگی‌ها را درون یک محیط مجازی پایتون نصب کنید:

<div dir="ltr">

```bash
git clone https://github.com/mhdio64/server-bootstrap.git
cd server-bootstrap

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

</div>

### ۲. ساخت فایل‌های پیکربندی سرور

پیکربندی سرور هدف را در یک مسیر خارج از پوشه اصلی سورس پروژه بسازید:

<div dir="ltr">

```text
my-server/
├── inventory.yml
└── bootstrap.yml
```

</div>

توضیحات فایل‌ها:
- `inventory.yml`: مشخصات اتصال SSH به سرور هدف.
- `bootstrap.yml`: مقادیر تنظیمی و متغیرهای دلخواه پروژه (`bootstrap_*`).

می‌توانید از نمونه‌های آماده در [examples/minimal/](examples/minimal/) الگوبرداری کنید:

**نمونه `inventory.yml`:**

<div dir="ltr">

```yaml
---
all:
  hosts:
    bootstrap-target:
      ansible_host: 203.0.113.10
      ansible_user: root
```

</div>

**نمونه `bootstrap.yml`:**

<div dir="ltr">

```yaml
---
# New admin user (cannot be root)
bootstrap_admin_user: deploy

# Public SSH keys for admin user (at least one key is required)
bootstrap_admin_authorized_keys:
  - "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... user@example.com"

# Optional: extra inbound firewall TCP ports (SSH is always allowed)
# bootstrap_firewall_allowed_tcp_ports:
#   - 80
#   - 443

# Optional: users to add to docker group
# bootstrap_docker_users:
#   - deploy
```

</div>

### ۳. پیش‌نمایش، اعمال و اعتبارسنجی

اسکریپت رپر پایتون اختصاصی (`./bootstrap`) با اجرای کنترل‌شده و اعتبارسنجی هویت SSH میزبان اجرا می‌شود:

<div dir="ltr">

```bash
# مرحله پیش‌نمایش (بدون اعمال تغییر و بدون آسیب)
./bootstrap check -i /path/to/inventory.yml

# مرحله اعمال تغییرات (نیاز به تایید اینتراکتیو دارد، مگر با فلگ --yes)
./bootstrap apply -i /path/to/inventory.yml

# مرحله اعتبارسنجی مستقل پس از راه‌اندازی
./bootstrap verify -i /path/to/inventory.yml
```

</div>

### ۴. بررسی و آزمایش نهایی

تست دسترسی‌ها روی سرور:

<div dir="ltr">

```bash
sudo whoami
docker ps
docker compose version
```

</div>

- دستور `sudo whoami`: بررسی دسترسی ادمین بدون رمز (خروجی باید `root` باشد).
- دستورات `docker ps` و `docker compose version`: بررسی صحت اجرای سرویس داکر.

---

## متغیرهای پیکربندی عمومی

تمام متغیرهای عمومی با پیشوند `bootstrap_*` مشخص می‌شوند. مهم‌ترین متغیرها عبارتند از:

| متغیر | مقدار پیش‌فرض | توضیحات |
|---|---|---|
| `bootstrap_admin_user` | اجباری | نام حساب ادمین جدید (نباید `root` باشد) |
| `bootstrap_admin_authorized_keys` | اجباری | فهرست کلیدهای عمومی SSH ادمین |
| `bootstrap_timezone` | `UTC` | منطقه زمانی سرور (از طریق `timedatectl`) |
| `bootstrap_firewall_allowed_tcp_ports` | `[]` | پورت‌های باز TCP در فایروال (علاوه بر پورت SSH) |
| `bootstrap_firewall_allowed_udp_ports` | `[]` | پورت‌های باز UDP در فایروال |
| `bootstrap_docker_enabled` | `true` | فعال یا غیرفعال‌سازی نصب داکر |
| `bootstrap_docker_version` | `latest` | نصب آخرین نسخه رسمی یا نسخه مشخص از مخازن بالادستی |
| `bootstrap_docker_users` | `[]` | کاربرانی که عضو گروه `docker` می‌شوند |
| `bootstrap_upgrade_packages` | `false` | به‌روزرسانی کامل پکیج‌های سیستم‌عامل (`apt dist-upgrade` یا `dnf upgrade`) |
| `bootstrap_reboot_if_required` | `false` | ریبوت خودکار سرور در صورت نیاز پکیج‌ها |

مرجع کامل تمامی متغیرها: [docs/13-CONFIGURATION-REFERENCE.md](docs/13-CONFIGURATION-REFERENCE.md).

---

## استانداردهای کیفیت و ایمنی پروژه

- **پایداری تکرار (Idempotency):** دومین اجرای متوالی روی سرور، در تمامی ۵ پلتفرم باید دقیقاً `changed=0` برگرداند.
- **بررسی ایمن (Check Mode):** امکان پیش‌نمایش تغییرات بدون دستکاری ناخواسته سرور به صورت واقع‌گرایانه.
- **عدم قطعی SSH و سیستم Rollback فایروال:**
  - کانفیگ SSH با فایل drop-in در `/etc/ssh/sshd_config.d/` اعمال شده و قبل از فعال‌سازی تست سینتکس می‌شود.
  - پس از بارگذاری مجدد، اتصال زنده ادمین اعتبارسنجی می‌شود و در صورت بروز خطا به طور خودکار بازگردانی می‌شود (Rollback).
  - رول‌های فایروال در دبیان/اوبونتو با تایمر اضطراری `systemd-run` مراقبت می‌شوند تا در صورت قطعی اتصال، رول‌های پیشین احیا شوند.
- **امنیت داکر:** نصب تنها از مخازن رسمی داکر انجام شده و از اسکریپت‌های مخاطره‌آمیز `curl | sh` استفاده نمی‌شود.
- **آزمون کامل ماتریس ۵ پلتفرم روی ماشین‌های مجازی واقعی:** اعتبارسنجی جامع در قالب ۱۴ گیت آزمون برای هر توزیع (مجموعاً ۷۰ از ۷۰ گیت قبولی) در محیط وگرنت ([tests/vagrant/](tests/vagrant/)).

---

## نکات مهم و محدودیت‌ها (Important Caveats)

### فایروال

- **Debian / Ubuntu:** از زنجیره‌های اختصاصی `iptables-nft` استفاده می‌کند و هرگز رول‌ها را به صورت سراسری پاک نمی‌کند (Flush). در صورت مواجهه با پالیسی‌های ناآشنا یا مغایر (نظیر سرویس فعال UFW) متوقف می‌شود.
- **Enterprise Linux (AlmaLinux 9 / 10):** از رول‌های دائمی (permanent) و غنی (rich rules) در `firewalld` بهره می‌برد و تغییری در زون‌های فعال متفرقه ایجاد نمی‌کند.
- زنجیره‌ها و رول‌های داخلی پورت‌های منتشرشده کانتینرهای داکر توسط این ابزار دستکاری نمی‌شوند.

### داکر

- پکیج‌ها مستقیماً از مخزن رسمی داکر (APT برای دبیان/اوبونتو و DNF/RPM برای انترپرایز لینوکس) نصب می‌شوند.
- وضعیت داکر موجود بررسی می‌شود؛ نصب‌های ناسازگار پیشین بدون هماهنگی بازنویسی نمی‌شوند.
- عضویت در گروه `docker` به دلیل دسترسی معادل root به صورت پیش‌فرض غیرفعال است و از طریق `bootstrap_docker_users` کنترل می‌شود.

### انترپرایز لینوکس و SELinux

- سازگاری کامل با اجرای لینوکس سازمانی در حالت استاندارد و فعال `SELinux Enforcing`.
- مدیریت خودکار ماژول‌های مورد نیاز هسته (نظیر `kernel-modules-extra` در آلما لینوکس ۱۰) برای شبکه‌سازی bridge داکر.

### حیطه تمرکز ابزار (Scope & Focus)

- **مدیریت تک‌هاست در هر اجرا:** برای دقت و شفافیت کامل اپراتور در بررسی هویت SSH و سلامت سرور.
- **ایمنی متمرکز بر نقاط بحرانی:** دارای مکانیزم‌های بازگشت خودکار (Rollback) در بخش‌های حیاتی اتصال (SSH و فایروال)؛ سایر همگرایی‌ها بر پایه اجرای مجدد ایمن (Idempotent) انجام می‌گیرد.
- **تمرکز بر زیرساخت پایه:** سرویس‌های لایه کاربردی، وب‌سرورها، گواهی SSL، کوبرنتیز و مانیتورینگ در مراحل بعدی بر بستر داکر یا لایه‌های بالاتر دیپلوی می‌شوند.

---

## ساختار دایرکتوری‌ها

<div dir="ltr">

```text
server-bootstrap/
├── bootstrap
├── bootstrap_wrapper/
├── site.yml
├── verify.yml
├── roles/
├── tasks/
├── tests/
├── examples/minimal/
└── docs/
```

</div>

---

## اسناد تکمیلی پروژه

| سند | موضوع |
|---|---|
| [docs/13-CONFIGURATION-REFERENCE.md](docs/13-CONFIGURATION-REFERENCE.md) | راهنمای کامل متغیرهای کانفیگ |
| [docs/14-TROUBLESHOOTING.md](docs/14-TROUBLESHOOTING.md) | راهنمای رفع اشکال و خطاهای متداول |
| [docs/15-RELEASE-EVIDENCE.md](docs/15-RELEASE-EVIDENCE.md) | شواهد و گیت‌های انتشار نسخه |
| [docs/16-MULTI-DISTRO-ROADMAP.md](docs/16-MULTI-DISTRO-ROADMAP.md) | معماری و نقشه راه پشتیبانی چندتوزیعی |
| [docs/03-SECURITY-SAFETY.md](docs/03-SECURITY-SAFETY.md) | مدل ایمنی و اصول امنیتی |
| [docs/05-TESTING-RELEASE.md](docs/05-TESTING-RELEASE.md) | راهبرد آزمون و انتشار |
| [AGENTS.md](AGENTS.md) | دستورالعمل‌ها و مرزهای کاری توسعه‌دهندگان و ایجنت‌ها |

---

## توسعه و تست محلی

<div dir="ltr">

```bash
yamllint .
ansible-lint
ansible-playbook site.yml --syntax-check
ansible-playbook verify.yml --syntax-check
python -m unittest discover -s tests/unit -p 'test_*.py'
ansible-playbook tests/synthetic/playbooks/test_platform_vars_resolution.yml -i localhost, -c local
./tests/synthetic/run-phase1-preflight-tests.sh
./scripts/secret-scan.sh
./scripts/test-secret-gate-negative.sh
git diff --check
```

</div>

---

## لایسنس و سلب مسئولیت

این پروژه تحت مجوز [MIT](LICENSE) منتشر شده و به صورت «همان‌گونه که هست (AS-IS)»، بدون هیچ‌گونه ضمانت صریح یا ضمنی ارائه می‌شود.

همانند تمامی ابزارهای خودکارسازی زیرساخت که تنظیمات سطح سیستم (SSH، فایروال و پکیج‌ها) را مدیریت می‌کنند، توصیه می‌شود پیش از اعمال روی سرورهای حساس عملیاتی، ابتدا رفتار ابزار را با دستور `./bootstrap check` روی یک محیط آزمایشی بررسی فرمایید.

[English](README.md) | [فارسی](README.fa.md)

# سرور بوت‌استرپ (server-bootstrap)

> آماده‌سازی امن، خودکار و استاندارد سرورهای Ubuntu Server 24.04 LTS (معماری amd64) به یک بیس‌لاین امن، قابل مدیریت و آماده‌ی داکر با Ansible.

پروژه `server-bootstrap` اولین جزء از مجموعه ابزار DevOps Toolkit است. نسخه v0.1.0 یک بسته اولیه (MVP) عملیاتی، سبک و آماده استفاده در پروداکشن را فراهم می‌کند:

- تنظیمات پایه سیستم‌عامل و همگام‌سازی زمان (systemd-timesyncd)
- ایجاد حساب ادمین با کلید عمومی SSH و دسترسی بدون رمز به sudo
- امن‌سازی SSH (Hardening) از طریق فایل drop-in اختصاصی پروژه
- فایروال محلی سرور بر پایه `iptables-nft` همراه با سیستم بازیابی اضطراری (Watchdog)
- فعال‌سازی خودکار به‌روزرسانی‌های امنیتی (unattended-upgrades)
- نصب موتور رسمی Docker CE و پلاگین Docker Compose

## پلتفرم‌های پشتیبانی‌شده

| بخش | پشتیبانی‌شده |
|---|---|
| سیستم‌عامل سرور هدف | Ubuntu Server 24.04 LTS |
| معماری پردازنده سرور | amd64 / x86_64 |
| سیستم‌عامل سیستم کنترل (کنترل‌نود) | لینوکس (Linux)، پایتون 3.12 تا 3.14 |
| نسخه انسیبل | `ansible-core` نسخه 2.21.x |

> جزئیات کامل و محدودیت‌ها در [docs/15-RELEASE-EVIDENCE.md](docs/15-RELEASE-EVIDENCE.md) درج شده است.

## راهنمای شروع سریع (Quick Start)

### ۱. آماده‌سازی محیط محلی

ابتدا مخزن را دریافت کرده و ابزارهای مورد نیاز را درون یک محیط مجازی پایتون نصب کنید:

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

پیکربندی سرور هدف را در یک مسیر خارج از پوشه اصلی سورس پروژه بسازید (مثلاً در یک پوشه جداگانه):

<div dir="ltr">

```text
my-server/
├── inventory.yml    # مشخصات اتصال SSH به سرور
└── bootstrap.yml    # متغیرهای تنظیمی دلخواه (bootstrap_*)
```

</div>

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
# کاربر ادمین جدید
bootstrap_admin_user: deploy

# کلیدهای عمومی معتبر برای ورود ادمین (حداقل یک کلید الزامی است)
bootstrap_admin_authorized_keys:
  - "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... user@example.com"

# پورت‌های اضافی فایروال (پورت SSH به طور خودکار باز است)
# bootstrap_firewall_allowed_tcp_ports:
#   - 80
#   - 443

# کاربرانی که باید به گروه docker اضافه شوند (اختیاری)
# bootstrap_docker_users:
#   - deploy
```

</div>

### ۳. چرخه ۳ مرحله‌ای اجرا (Check ➜ Apply ➜ Verify)

دستورات را از پوشه اصلی پروژه اجرا کنید:

<div dir="ltr">

```bash
# ۱. شبیه‌سازی و بررسی بدون تغییر روی سرور (Dry Run)
./bootstrap check -i /path/to/my-server/inventory.yml

# ۲. اعمال واقعی تنظیمات
./bootstrap apply -i /path/to/my-server/inventory.yml

# ۳. راستی‌آزمایی صحت کارکرد سرویس‌ها و فایروال و تست داکر
./bootstrap verify -i /path/to/my-server/inventory.yml
```

</div>

> **نکته ایمنی Wrapper:**
> - در اولین اتصال، اثرانگشت SSH سرور (Host Fingerprint) به صورت تعاملی از شما تأیید می‌گیرد (یا می‌توانید با فلگ `--expected-host-fingerprint` آن را در محیط‌های اتوماسیون پاس دهید).
> - اجرای `apply` نیاز به تأییدیه کاربر دارد؛ برای اسکریپت‌ها یا CI می‌توانید از فلگ `--yes` استفاده کنید.
> - لاگ‌های تفصیلی اجرا در مسیر `${XDG_STATE_HOME:-~/.local/state}/server-bootstrap/logs` ذخیره می‌شوند.

---

## ورود به سرور پس از بوت‌استرپ

پس از اعمال موفقیت‌آمیز، احراز هویت با رمز عبور در SSH غیرفعال شده و باید با کاربر ادمین جدید و کلید خصوصی SSH وارد شوید:

<div dir="ltr">

```bash
ssh -i ~/.ssh/id_ed25519 deploy@203.0.113.10
```

</div>

تست دسترسی‌ها روی سرور:

<div dir="ltr">

```bash
# تست دسترسی ادمین (sudo بدون رمز)
sudo whoami

# تست دسترسی داکر
docker ps
docker compose version
```

</div>

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
| `bootstrap_docker_version` | `latest` | نصب آخرین نسخه رسمی یا نسخه مشخص |
| `bootstrap_docker_users` | `[]` | کاربرانی که عضو گروه `docker` می‌شوند |
| `bootstrap_upgrade_packages` | `false` | به‌روزرسانی کامل پکیج‌های سیستم‌عامل (`apt dist-upgrade`) |
| `bootstrap_reboot_if_required` | `false` | ریبوت خودکار سرور در صورت نیاز پکیج‌ها |

مرجع کامل تمامی متغیرها: [docs/13-CONFIGURATION-REFERENCE.md](docs/13-CONFIGURATION-REFERENCE.md).

---

## استانداردهای کیفیت و ایمنی پروژه

- **پایداری تکرار (Idempotency):** دومین اجرای متوالی روی سرور دست‌نخورده، باید دقیقاً `changed=0` برگرداند.
- **بررسی ایمن (Check Mode):** امکان پیش‌نمایش تغییرات بدون دستکاری ناخواسته سرور.
- **عدم قطعی SSH و سیستم Rollback فایروال:**
  - کانفیگ SSH با فایل drop-in در `/etc/ssh/sshd_config.d/` اعمال شده و قبل از فعال‌سازی تست سینتکس می‌شود.
  - پس از بارگذاری مجدد، اتصال زنده ادمین اعتبارسنجی می‌شود و در صورت خطا خودکار برگشت می‌خورد (Rollback).
  - رول‌های فایروال با تایمر اضطراری `systemd-run` مراقبت می‌شوند تا در صورت قطعی اتصال، رول‌های پیشین احیا شوند.
- **امنیت داکر:** نصب تنها از مخزن رسمی داکر انجام شده و از اسکریپت‌های مخاطره‌آمیز `curl | sh` استفاده نمی‌شود.
- **تست شده در محیط واقعی:** سناریوی راه‌اندازی سرور روی ماشین مجازی واقعی تست و تأیید شده است ([tests/scenario1/](tests/scenario1/)).

---

## حیطه تمرکز ابزار (Scope & Focus)

- **مدیریت تک‌هاست در هر اجرا:** برای دقت و شفافیت کامل اپراتور در بررسی هویت SSH و سلامت سرور.
- **ایمنی متمرکز بر نقاط بحرانی:** دارای مکانیزم‌های بازگشت خودکار (Rollback) در بخش‌های حیاتی اتصال (SSH و فایروال)؛ سایر همگرایی‌ها بر پایه اجرای مجدد ایمن (Idempotent) انجام می‌گیرد.
- **تمرکز بر زیرساخت پایه:** سرویس‌های لایه کاربردی، وب‌سرورها، گواهی SSL، کوبرنتیز و مانیتورینگ در مراحل بعدی بر بستر داکر یا لایه‌های بالاتر دیپلوی می‌شوند.
- اعتبارسنجی سرورهای از پیش پیکربندی‌شده (سناریو ۲) در برنامه‌های پس از نسخه MVP قرار دارد.

---

## ساختار دایرکتوری‌ها

<div dir="ltr">

```text
server-bootstrap/
├── bootstrap                  # اسکریپت رابط کاربر (Python CLI wrapper)
├── bootstrap_wrapper/         # کدهای پایتونی هندلرها و لاگین
├── site.yml                   # پلی‌بوک اصلی برای اجرای Preflight و Apply
├── verify.yml                 # پلی‌بوک تست سلامت و راستی‌آزمایی
├── roles/                     # رول‌های ماژولار (common, users, ssh, firewall, security, docker)
├── examples/minimal/          # نمونه حداقل کانفیگ‌های inventory و bootstrap
├── tests/                     # تست‌های واحد، synthetic و تست ماشین مجازی سناریو ۱
└── docs/                      # مستندات کامل معماری، ایمنی، تصمیمات و عیب‌یابی
```

</div>

---

## اسناد تکمیلی پروژه

| سند | موضوع |
|---|---|
| [docs/13-CONFIGURATION-REFERENCE.md](docs/13-CONFIGURATION-REFERENCE.md) | راهنمای کامل متغیرهای کانفیگ |
| [docs/14-TROUBLESHOOTING.md](docs/14-TROUBLESHOOTING.md) | راهنمای رفع اشکال و خطاهای متداول |
| [docs/03-SECURITY-SAFETY.md](docs/03-SECURITY-SAFETY.md) | مدل ایمنی و اصول امنیتی |
| [docs/15-RELEASE-EVIDENCE.md](docs/15-RELEASE-EVIDENCE.md) | شواهد و گیت‌های انتشار نسخه |
| [AGENTS.md](AGENTS.md) | دستورالعمل‌ها و مرزهای کاری توسعه‌دهندگان و ایجنت‌ها |

---

## لایسنس و سلب مسئولیت

این پروژه تحت مجوز [MIT](LICENSE) منتشر شده و به صورت «همان‌گونه که هست (AS-IS)»، بدون هیچ‌گونه ضمانت صریح یا ضمنی ارائه می‌شود.

همانند تمامی ابزارهای خودکارسازی زیرساخت که تنظیمات سطح سیستم (SSH، فایروال و پکیج‌ها) را مدیریت می‌کنند، توصیه حرفه‌ای این است که پیش از اعمال روی سرورهای حساس عملیاتی، ابتدا رفتار ابزار را با دستور `./bootstrap check` روی سرور یا یک محیط آزمایشی بررسی فرمایید.

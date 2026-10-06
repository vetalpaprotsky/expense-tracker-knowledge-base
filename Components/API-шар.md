---
type: component
created: 2026-09-18
updated: 2026-09-28
tags: [component, api]
module: src/api/main.py
status: implemented
source: git:50682ec
depends_on: ["[[Валідація даних]]", "[[Сховище даних]]", "[[Модуль звітності]]"]
implements: ["[[Витрата]]"]
decided_by: ["[[ADR-001 Вибір FastAPI]]"]
---
# API-шар

**API-шар** — HTTP-інтерфейс застосунку на FastAPI: маршрути `/expenses`, `/categories`, `/reports/monthly`, `/budgets`.
Не містить бізнес-логіки: приймає запит, перевіряє схеми Pydantic ([[Pydantic-модель]]), викликає функції ядра й повертає JSON.
Залежить від [[Валідація даних]], [[Сховище даних]] та [[Модуль звітності]]. Вибір фреймворку — [[ADR-001 Вибір FastAPI]].

## Історія змін
- 2026-09-28: Реалізовано маршрути /expenses, /categories, /reports/monthly; 4 інтеграційні тести (коміт 50682ec).

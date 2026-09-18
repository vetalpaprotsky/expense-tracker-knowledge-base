---
type: component
created: 2026-09-18
tags: [component, api]
module: src/api/main.py
status: planned
---
# API-шар

**API-шар** — HTTP-інтерфейс застосунку на FastAPI: маршрути `/expenses`, `/categories`, `/reports/monthly`, `/budgets`.
Не містить бізнес-логіки: приймає запит, перевіряє схеми Pydantic ([[Pydantic-модель]]), викликає функції ядра й повертає JSON.
Залежить від [[Валідація даних]], [[Сховище даних]] та [[Модуль звітності]]. Вибір фреймворку — [[ADR-001 Вибір FastAPI]].

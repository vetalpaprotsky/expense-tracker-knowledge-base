# Expense Tracker — база знань (Obsidian vault)

Окремий git-репозиторій, що є knowledge layer для agent harness проєкту `expense-tracker-api`.
Відкривається в Obsidian як vault; для агента доступний **лише** через MCP-сервер конектора.

## Структура
- `Concepts/` — поняття предметної області
- `Components/` — модулі застосунку
- `Decisions/` — ADR (нотатки не видаляються)
- `Glossary/` — глосарій
- `_templates/` — шаблони frontmatter
- `MOC-Застосунок.md` — Map of Content, точка входу

## Конвенції
1. Назва файлу = заголовок нотатки, без скорочень; кирилиця дозволена.
2. Обов'язковий frontmatter: `type` (`concept|component|decision|glossary|moc`), `created`, `tags`.
3. Додаткові поля: component — `module`, `status`; decision — `status`, `date`; glossary — `aliases`.
4. Зв'язки лише через `[[wiki-посилання]]`, а не просте згадування.
5. Кожна нотатка має бути досяжна з `MOC-Застосунок`.

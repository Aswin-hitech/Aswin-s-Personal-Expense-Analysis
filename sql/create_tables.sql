-- =====================================
-- Personal Expense Analytics System
-- =====================================

CREATE TABLE IF NOT EXISTS expense_records (
    expense_id SERIAL PRIMARY KEY,

    entry_date DATE,
    category TEXT,
    description TEXT,
    amount INTEGER,

    location TEXT,
    balance INTEGER,

    wallet_recharge TEXT,
    payment_mode TEXT,

    day_type TEXT,
    day_name TEXT,
    month TEXT,

    week_no INTEGER,

    priority TEXT,
    necessity TEXT,

    expense_level TEXT,

    running_expense INTEGER,
    daily_expense INTEGER,

    savings_opportunity INTEGER,

    expense_bucket TEXT,

    remaining_budget INTEGER,

    budget_used_percent NUMERIC(10,2),

    daily_average_spend NUMERIC(10,2),

    food_type TEXT,

    expense_group TEXT
);
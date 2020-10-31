
def payment_calculator(type, interest_rate, total_cost, term, down_payment):
    res = []
    total_cost -= down_payment

    if type == 0:
        # 等额本金 = (贷款本金 / 还款月数) + (本金 — 已归还累计额) × 月利率
        monthly_fix = total_cost / term
        for i in range(term):
            res.append(round(monthly_fix + interest_rate / 12 * (total_cost - i * monthly_fix), 2))
        return res, sum(res) + down_payment
    else:
        # 等额本息 = 本金 * 月利率 * （1 + 月利率）^ 月数 / ((1 + 月利率）^ 月数 - 1))
        return [round(total_cost * interest_rate / 12 * ((1 + interest_rate / 12) ** term) / ((1 + interest_rate / 12) ** term - 1), 2) for i in range(term)], \
               round((total_cost * interest_rate / 12 * ((1 + interest_rate / 12) ** term) / ((1 + interest_rate / 12) ** term - 1)) * term + down_payment, 2)

month = [36, 48, 60]
i_rate = 0.04

# 表达评分规则（rubric）

> B 维护。本文件定义 `score_expression()` 的具体打分逻辑。
> 阈值是初版猜测，后续用真实数据回归调整。

## speech_rate_score（0~100）

基于整场平均 `wpm`（字/分钟）：

| wpm 区间 | 分数 |
|---|---|
| 180 ~ 260 | 100 |
| 150 ~ 180 / 260 ~ 290 | 80 |
| 120 ~ 150 / 290 ~ 320 | 60 |
| < 120 或 > 320 | 40 |

## clarity_score（0~100）

加权：`pause_ratio (40%) + filler_density (40%) + long_pause_count (20%)`

- `pause_ratio < 0.15` → 满分；每超 0.05 扣 10
- `filler_density = filler_total / total_seconds * 60`
  - < 1 次/分 → 满分
  - 1~3 → 80
  - 3~5 → 60
  - \> 5 → 40
- `long_pause_count` 平均每分 < 1 → 满分；每多 1 扣 10

## confidence_score（0~100）

加权：`pitch_stability (50%) + volume_stability (30%) + LLM_sentiment (20%)`

- `pitch_stability = 1 - pitch_std / pitch_mean`，归一到 0~100
- `volume_stability = 1 - volume_std / volume_mean`，归一到 0~100
- `LLM_sentiment`：用 LLM 对 transcript 判断"自信/中性/犹豫"，分别给 100/70/40

## expression_score（覆盖原 evaluation.expression_score）

`expression_score = 0.3 * speech_rate + 0.4 * clarity + 0.3 * confidence`

## 岗位差异（role 参数，可选）

- 算法/后端：语速期待略慢（思考型），160~240 给满分
- 前端/产品：语速期待略快，200~280 给满分

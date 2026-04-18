"""
表达评分聚合 - B 负责实现。

入参：A 产出的 VoiceMetrics 列表（一场面试所有用户语音回答）
出参：ExpressionScore dict（参见 docs/expression_module_contract.md §2.2）

约定：
- 评分 rubric 写在 expression_rubric.md
- 填充词清单从 filler_words 模块 import，禁止硬编码
- metrics_list 为空 → 返回 None
- 单条 metrics 缺字段 → 跳过该条，不抛错
"""

from typing import Optional


def score_expression(
    metrics_list: list[dict],
    role: Optional[str] = None,
) -> Optional[dict]:
    """
    Args:
        metrics_list: A 的 analyze_audio() 返回值列表
        role: 岗位名（可选，不同岗位语速期待不同）

    Returns:
        ExpressionScore dict 或 None（无语音输入）
    """
    raise NotImplementedError("B: 实现 score_expression")

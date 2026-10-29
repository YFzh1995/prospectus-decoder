# 数据约定（2.0）

所有阶段输出合法JSON；示例中的null表示待核实/不可得，不以“必须填满”迫使编造。统一使用事实ID、观点ID、来源ID连接。数值保留原始字符串，派生数另存公式。以下是最小结构，可按主题扩展；它是数据约定，不是已实现的自动抽取引擎。

## 事实（分块与Master共用）

```json
{
  "issuer": {"legal_name": "示例公司", "markets": [], "identifiers": {}},
  "facts": [
    {
      "fact_id": "F001",
      "topic": "financials",
      "metric": "revenue",
      "value": "123.45",
      "unit": "million",
      "currency": "USD",
      "period": "2025年度",
      "scope": "合并",
      "definition": "营业收入",
      "evidence_type": "reported_financial",
      "entity_namespace": null,
      "evidence": [{"source_id": "D001", "section": "财务资料", "pdf_page": null, "printed_page": null, "table_or_paragraph": "合并利润表", "short_quote": ""}]
    }
  ],
  "entities": [],
  "coverage": {"processed": [], "missing_blocks": [], "limitations": []},
  "conflicts": [],
  "missing_info": []
}
```

非数值事实的value也是字符串，unit/currency等不适用时null。证据类型可用reported_financial/company_claim/industry_adviser_estimate/risk_disclosure。实体记录原名、类型、is_anonymized布尔值、识别线索、source_id和版本命名空间。

## 商业推理

```json
{
  "one_liner": "示例公司做什么",
  "business_essence": {"customer_budget": "", "use_case": "", "product_function": "", "pricing_model": "", "geography": "", "value_chain_position": "", "substitutes": []},
  "conclusions": [
    {"id": "C001", "topic": "revenue_logic", "claim": "", "kind": "inference", "fact_ids": ["F001"], "rationale": "", "alternative_explanations": [], "confidence": "low", "limitations": []}
  ],
  "entity_identifications": [],
  "industry_perspective": {"nominal_ranking": null, "modifiers": [], "stripped_ranking": "无法确定", "comparable_dimensions": []},
  "financial_analysis": {"periods": [], "derived_metrics": [], "limitations": []},
  "investment_thesis": {"bull_case": null, "base_case": null, "bear_case": null, "key_indicators": []},
  "open_questions": []
}
```

conclusions覆盖customer_profile/value_creation/revenue_logic/industry_chain/competition/risks/opportunities等主题。kind为disclosure/calculation/inference/forecast；计算保存公式、输入fact_ids及假设。匿名识别每项保存anonymized_name/candidates/confidence/evidence_urls/confirmed与限制，搜索不能自动把confirmed设为true。

## 外部研究

```json
{
  "search_scope": {"cutoff_date": "YYYY-MM-DD", "queries": [], "languages": [], "time_window": "", "limitations": []},
  "articles": [
    {"source_id": "A001", "title": "", "author": null, "publisher": "", "published_at": null, "url": "", "access": "full_text", "read_scope": "", "independent_origin": "", "selection_reason": "", "summary": "", "claims": ["M001"]}
  ],
  "claims": [
    {"claim_id": "M001", "claim": "", "claim_kind": "fact", "article_ids": ["A001"], "consensus_scope": "单篇观点", "period": null, "disclosure_fact_ids": [], "verification_result": "证据不足", "rationale": "", "counter_evidence": [], "limitations": []}
  ],
  "competitors": [
    {"name": "", "market_and_ticker": null, "comparison_type": "direct", "comparability": "", "business_overview": "", "customers_and_geography": "", "revenue_model": "", "metrics": [], "strengths_and_limits": "", "source_ids": []}
  ],
  "contrarian_findings": [],
  "unresolved_questions": []
}
```

来源清单顶层为 `{"issuer": {}, "sources": []}`，每项字段见下载指南。文章access为full_text/partial/snippet_only/unavailable；只有实际阅读的范围才能用于论证。每项竞争指标保存period/value/unit/currency/scope/definition/source_id及定位。

## 量化与定语分析（2.1）

`work/calculations.json` 以 `calculations` 数组保存 `id, metric, formula, inputs`（含fact_ids与值）, `result, unit, period, scope, assumptions, business_meaning`。计算数与原始披露分开。现金流桥、费用分项应可加总回主表；近似回款、合同拆分等保留假设、四舍五入和重叠口径。

`work/modifier-analysis.json` 以 `claims` 数组保存 `id, source_fact_ids, original_meaning, modifiers, included_scope, excluded_scope, expanded_comparison, surviving_advantage, unresolved_evidence`。若无可靠综合名次，用文字说明能判断的具体位置。两类记录应汇入business-reasoning或提供可追溯索引。

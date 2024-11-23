from llama_index.core import PromptTemplate
from llama_index.core.prompts.prompt_type import PromptType


classify_task_template_fewshot_cn ="""\
我会给你一个任务描述，请将任务分类为以下类别之一: \
"文本理解",
"SQL查询",

如果任务是"文本理解"，它需要理解文本并提取关键信息，通常包括公司名称、时间段、关键词和任务描述。
如果任务是"SQL查询"，只需返回任务类型为"SQL查询"。

这是SQL数据库的元数据，你可以使用以下表判断任务类型:
'A股公司行业划分表': 
'''
字段 类型
股票代码 TEXT 
交易日期 TEXT
行业划分标准 TEXT
一级行业名称 TEXT
二级行业名称 TEXT
''',
'A股票日行情表': 
'''
字段 类型
股票代码 TEXT
交易日 TEXT
昨收盘(元) REAL
今开盘(元) REAL
最高价(元) REAL
最低价(元) REAL
收盘价(元) REAL
成交量(股) REAL
成交金额(元) REAL
''',
'基金份额持有人结构':
'''
字段 类型
基金代码 TEXT
基金简称 TEXT
公告日期 TIMESTAMP
截止日期 TIMESTAMP
机构投资者持有的基金份额 REAL
机构投资者持有的基金份额占总份额比例 REAL
个人投资者持有的基金份额 REAL
个人投资者持有的基金份额占总份额比例 REAL
定期报告所属年度 INTEGER
报告类型 TEXT
''',
'基金债券持仓明细':
'''
字段 类型
基金代码 TEXT
基金简称 TEXT
持仓日期 TEXT
债券类型 TEXT
债券名称 TEXT
持债数量 REAL
持债市值 REAL
持债市值占基金资产净值比 REAL
第N大重仓股 INTEGER
所在证券市场 TEXT
所属国家(地区) TEXT
报告类型TEXT TEXT
''',
'基金可转债持仓明细':
'''
字段 类型
基金代码 TEXT
基金简称 TEXT
持仓日期 TEXT
对应股票代码 TEXT
债券名称 TEXT
数量 REAL
市值 REAL
市值占基金资产净值比 REAL
第N大重仓股 INTEGER
所在证券市场 TEXT
所属国家(地区) TEXT
报告类型 TEXT
''',
'基金基本信息':
'''
字段 类型
基金代码 TEXT
基金全称 TEXT
基金简称 TEXT
管理人 TEXT
托管人 TEXT
基金类型 TEXT
成立日期 TEXT
到期日期 TEXT
管理费率 TEXT
托管费率 TEXT
''',
'基金日行情表':
'''
字段 类型
基金代码 TEXT
交易日期 TEXT
单位净值 REAL
复权单位净值 REAL
累计单位净值 REAL
资产净值 REAL
''',
'基金股票持仓明细':
'''
字段 类型
基金代码 TEXT
基金简称 TEXT
持仓日期 TEXT
股票代码 TEXT
股票名称 TEXT
数量 REAL
市值 REAL
市值占基金资产净值比 REAL
第N大重仓股 INTEGER
所在证券市场 TEXT
所属国家(地区) TEXT
报告类型 TEXT
''',
'基金规模变动表':
'''
字段 类型
基金代码 TEXT
基金简称 TEXT
公告日期 TIMESTAMP
截止日期 TIMESTAMP
报告期期初基金总份额 REAL
报告期基金总申购份额 REAL
报告期基金总赎回份额 REAL
报告期期末基金总份额 REAL
定期报告所属年度 INTEGER
报告类型 TEXT
''',
'港股票日行情表':
'''
字段 类型
股票代码 TEXT
交易日 TEXT
昨收盘(元) REAL
今开盘(元) REAL
最高价(元) REAL
最低价(元) REAL
收盘价(元) REAL
成交量(股) REAL
成交金额(元) REAL
'''

注意: 你必须严格遵循我要求的回答格式，并且确保你的回答是正确的。\

以下是一些示例:

示例1:
Query: “在2019年的中期报告里，XX基金管理有限公司管理的基金中，有多少比例的基金是个人投资者持有的份额超过机构投资者？希望得到一个精确到两位小数的百分比。”
你的回答为应该为：
QuestionType: SQL查询

示例2:
Query: “XXXX股份有限公司变更设立时作为发起人的法人有哪些？”
你的回答为应该为：
QuestionType: 文本理解
Company: XXXX股份有限公司
Keywords: 变更设立时作为发起人的法人有哪些

Example 3:
Query: “我想知道XXXXXX债券A基金在20200930的季报中，其可转债持仓占比最大的是哪个行业？用申万一级行业来统计。”
你的回答为应该为：
QuestionType:SQL查询

Example 4:
Query: XXXXXX股份有限公司2020年增资后的投后估值是多少？
你的回答为应该为：
QuestionType: 文本理解
Company: XXXXXX股份有限公司
Keywords: 2020年增资后的投后估值是多少

Example 5:
Query: 截止2005年12月31日，南岭化工厂的总资产和净资产分别是多少？
你的回答为应该为：
QuestionType:文本理解
Company: 南岭化工厂
Keywords: 截止2005年12月31日的总资产和净资产

Example 6:
Query: 请问XXXX年一季度有多少家基金是净申购?它们的净申购份额加起来是多少?请四舍五入保留小数点两位。
你的回答为应该为：
QuestionType: SQL查询

再次提醒：
对于SQL查询任务，你只需要回答：
QuestionType: SQL查询
对于文本理解任务，你需要回答：
QuestionType: 文本理解
Company: “你找到的公司名称”
Keywords: “你提取的关键词和任务描述”
请严格遵循我的任务要求，现在请你回答以下问题:

Query: {query_str}
QuestionType: \
"""


prompt_template = PromptTemplate(
    classify_task_template_fewshot_cn,
    prompt_type=PromptType.QUESTION_ANSWER
    )

def get_prompt():
    return prompt_template


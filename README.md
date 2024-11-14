# FinanceRAG

[toc]



## Model Download

Can download from huggingface

1. embedding: BAAI/bge-large-zh-v1.5
2. reranker: BAAI/bge-reranker-large
3. Lora base model: Qwen/Qwen2.5-7B-Instruct

## PDF Extracting

Convert pdf to markdown, which is more easy for chunking and LLM's understanding

**Script to Run**

```{shell}
python script/pdf_parser.py
```

**Problem pdf:**

> 54c7b3ab01ad11d37835a4464c9e4d68dfe6306f.PDF
> e6ff749bb533a47173aaca91fe5d44080d9d37b3.PDF
> 8c130bea710816d5ef9a8bd7b2df7ee46e9f40dd.PDF
> 72103a0ef6299585cdd09751682534d873f8e64e.PDF

**Check MD**

Check whether each markdown is well-formatted (the title contains company name or not)

```{shell}
python script/check_mardown.py
```

Find 7 files need to do a slight adjustment, which is caused by additional '\n' at the title
> e774a06e6b4db734424f7d9181b9515a08bea6cc.md
> 9dca16666143beb8c15a6a4ba6ec2b19b2ffb8fb.md
> 398c8e64f18a13e695b5956122ef2f6a6fd3b274.md
> d336d607e1d431cbfe1f313e2234a13fcf49a16e.md
> 50b2823371fe1699d260f67cadac3d38af0672e3.md
> 91b4426b075560a1a45247f9cfa9fa73d56c945c.md
> d6c70c04287ff6aba75b0565bef375469aaa68c3.md

extracting these 4 pdf use [llamaparse](https://cloud.llamaindex.ai/)

## Data Preprocessing

The biggest problem is that extracted documents **do not have the right recursive structure**, for example:

The **Headr_1: should be a company name** instead of something else, so we'd better to do some preprocessing

<img src="./README.assets/image-20241114001838721.png" alt="image-20241114001838721" style="zoom:50%;" />

```shell
python scripts/pdf_preprocessing.py
```



Here we did 2 thins:

	1. Added company_name as header1 for those absent
	1. Removed header1 that not company_name

After preprocessing, we now make sure company_name is the **only header1**

<img src="./README.assets/image-20241114130231977.png" alt="image-20241114130231977" style="zoom:50%;" />

## RAG Demo

use llama3.2 3B as base model:

### without RAG:

```markdown
>>> 介绍一下武汉力源信息技术股份有限公司
**关于武汉力源信息技术股份有限公司**

武汉力源信息技术股份有限公司是一家中国 headquartered 的信息技术公司，主要从
事软件开发、销售和服务。公司成立于1999年，总部位于中国湖北省武汉市。

**业务范围**

力源信息技术股份有限公司的业务范围广泛，包括：

* **软件开发和研究**:  Force Source 主要提供各类软件产品，例如办公管理系统、
人工智能等。
* **销售和服务**:  Force Source 在全国范围内提供软件销售和支持服务。
* **外部服务**:  Force Source 也为其他公司提供技术咨询和应用service。

**主要产品**

Force Source 的主要产品包括：

* **ForceOS**：是一种办公管理系统，用于提高企业的 productivity 和效率。
* **Fusion**：是一种人工智能解决方案，用于帮助企业做出数据驱动决策。
* **Mosaic**：是一种智能硬件平台，用于为 IoT 设备提供智能服务。

**合作伙伴**

Force Source 以其强大的技术能力和广泛的合作伙伴网络而著名。公司已经与许多国
内外知名企业合作，包括中国百联、中国电信、中国 Telecom等。

**发展目标**

Force Source 的长期发展目标是成为全球领先的信息技术服务提供商，通过创新和高
效的运营，为客户提供高质量的软件产品和服务
```



### With RAG

```markdown
>>> 介绍一下武汉力源信息技术股份有限公司

武汉力源信息技术股份有限公司是一家专注于半导体集成电路和电子元器件的公司，注册资本为人民币5,000 万元。公司由赵马克担任法定代表人，主要运营范围包括电子产品、电子元器件、信息技术及相关成套产品方案的开发、研制、生产、销售及技术服务。公司的主营业务是推广、销售和应用服务于半导体集成电路等电子元器件。
```



## Some Interesting Problems Met in Data Preprocessing

- This kind of PDF shadow-style format can cause errors when extracting text

  <figure class="half">
    <img src="./README.assets/image-20241111232401793.png" alt="image-20241111232401793" style="zoom:25%;" />
    <img src="./README.assets/image-20241111232625978.png" alt="image-20241111232625978" style="zoom:25%;" />
  </figure>
  <figure class="half">
    <img src="./README.assets/image-20241111233949605.png" alt="image-20241111233949605" style="zoom:25%;" />
    <img src="./README.assets/image-20241111234118592.png" alt="image-20241111234118592" style="zoom:25%;" />
  </figure>
  
  
- Head title missing because title contained in Image

  <figure class="half">
    <img src="./README.assets/image-20241111233256138.png" alt="image-20241111233256138" style="zoom:25%;" />
    <img src="./README.assets/image-20241111233215573.png" alt="image-20241111233215573" style="zoom:25%;" />
  </figure>
  
  
  
  
  
  




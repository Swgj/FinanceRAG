# FinanceRAG

## Model Download

Can download from huggingface

1. embedding:BAAI/bge-large-zh-v1.5

## PDF Extracting

Convert pdf to markdown, which is more easy for chunking and LLM's understanding

**Script to Run**

```{shell}
python script/test_pdf_parser.py
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

  

  

  




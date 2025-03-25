上期讲解了通过zerox 解析pdf格式文件，并且给了如何将pdf解析为图片的办法

但是使用zerox将pdf文件变成md格式文档会遇到图片丢失的情况（至少我是这样的，而且zerox的代码复杂。最近正好又碰到了pdf解析的场景，所以我将介绍一种新的pdf解析办法  gptpdf）

gptpdf：开源可用（github地址：[CosmosShadow/gptpdf：使用 GPT 解析 PDF --- CosmosShadow/gptpdf: Using GPT to parse PDF](https://github.com/CosmosShadow/gptpdf)）

原理：有机会再出下期原理解析！

简短来讲，他就是使用PyMuPDF库，解析PDF文件来查找所有非文本区域并且标记他们

然后再将处理好的结果丢给大模型进行解析

首先 Installation 安装

直接pip install gptpdf 导包即可

示例代码：

```python
from gptpdf import parse_pdf
api_key = 'Your OpenAI API Key'
content, image_paths = parse_pdf(pdf_path, api_key=api_key)
print(content)
```

可以看到代码非常简单，主要的方法就是parse_pdf

这个函数定义了多种参数

```python
def parse_pdf(
        pdf_path: str,
        output_dir: str = './',
        prompt: Optional[Dict] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = 'gpt-4o',
        verbose: bool = False,
        gpt_worker: int = 1
) -> Tuple[str, List[str]]:
```

包括pdf路径  输出md文档路径 为大模型配置的提示词 apikey endpoint 模型名称等配置项

不仅是OpenAI  他还支持Qwen-vl-max、Azure OpenAI 等其他大模型

本次我主要是用的Azure OpenAI  在使用中我们需要注意一下

如果你用的是其他的大模型，请找到gptpdf官网给的test文件[gptpdf/test/test.py at main · CosmosShadow/gptpdf](https://github.com/CosmosShadow/gptpdf/blob/main/test/test.py)

这个py文件给出了Azure、Qwen等模型是如何对接，希望可以帮到你



我是Harry，一个刚毕业的小白，对于代码有着十足的热爱，热衷于把自己学习的知识和内容分享出来
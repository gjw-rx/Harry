碰到了需要解析富文本、PDF、图片的项目。需要使用OCR（光学文本识别技术）。并且解析后的文本需要转换成md格式文档

通过翻找github项目找到了zerox

![image-20250313152625846](D:\github博客_harry杂谈\zerox实现PDF文档OCR解析\zerox.png)

在现在Zerox前，需要安装poppler

poppler：一个呈现PDF文档的实用软件，提供了PDF转换、渲染、页面操作等多个功能

下载地址：[Installation — pdf2image latest documentation](https://pdf2image.readthedocs.io/en/latest/installation.html)

根据要求，下载好poppler并配置到环境变量path中，不会配置path的请出门右转

安装之后需要下载两个python包

pip install pdf2image   pip install py-zerox 两个包 

由于python包管理默认工具pip不具备处理版本冲突问题，那么pip我推荐anaconda工具

有关anaconda的使用我打算放到下期来介绍。

言归正传，现在我们pip好了对应的包就可以调用zerox来实现md格式文档的输出啦

```python
from pyzerox import zerox
import os
import json
import asyncio
kwargs = {}
custom_system_prompt = ""

###################### Example for Azure OpenAI ######################
model = "azure/gpt-4o-mini" ## "azure/<your_deployment_name>" -> format <provider>/<model>
os.environ["AZURE_API_KEY"] = "14a69ae5020b48ffb2da64cc6ca065d0" # "your-azure-api-key"
os.environ["AZURE_API_BASE"] = "https://sean-aoai-gpt4.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-10-21" # "https://example-endpoint.openai.azure.com"
os.environ["AZURE_API_VERSION"] = "2024-10-21"
async def main():
    file_path = "D:\\Capagemini\\PGmini\\capgemini-poc\\OCR\\test.pdf"

    ## process only some pages or all
    select_pages = 10 ## None for all, but could be int or list(int) page numbers (1 indexed)

    output_dir = "./output_test" ## directory to save the consolidated markdown file
    result = await zerox(file_path=file_path, model=model, output_dir=output_dir,
                        custom_system_prompt=custom_system_prompt,select_pages=select_pages, **kwargs)
    return result


# run the main function:
result = asyncio.run(main())

# print markdown result
print(result)
```

python代码如上：

那么我简单介绍一下配置文件都是干什么的

```python
result = await zerox(file_path=file_path, model=model, output_dir=output_dir,
                     custom_system_prompt=custom_system_prompt,select_pages=select_pages, **kwargs)
```

看到这段代码，这个就是调用了zerox的核心代码

初始必须的参数有

file_path : 上传的pdf文件

model：本次用到的大语言模型（没错，zerox本身并不具备任何解析功能，他需要用到带有视觉的大预言模型，可以理解zerox本身就是一个辅助的工具而已，如果有时间的话我打算专门出一个板块，详细讲解zerox的源码）

output_dir：输出md格式文档存储的路径

custom_system_prompt：提供给大语言模型的提示词，可以让大模型按照你的要求来生成内容

select_pages：这里是选择每次调用解析几页pdf，看到这里相信你会提问，什么叫每次调用解析几页

这里不就调用了一次嘛？肯定是作者水平太差误导我。实则不然！

那么问题的关键肯定是关键的问题，await可以更好的解决我们的疑惑。也就是说，其实这个zerox方法，他是一个异步协程的方法。

```python
# run the main function:
result = asyncio.run(main())

# print markdown result
print(result)
```

最后的输出也可以看到asyncio的字样。那么至于为什么zerox是一个协程办法，请追我可能会撰写的zerox源码分析系列，我将带你分析。

我是Harry，一个刚毕业的小白，对于代码有着十足的热爱，热衷于把自己学习的知识和内容分享出来
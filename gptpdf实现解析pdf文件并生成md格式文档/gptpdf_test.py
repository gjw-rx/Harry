from gptpdf import parse_pdf

base_url = "https://sean-aoai-gpt4.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview"
api_key = "14a69ae5020b48ffb2da64cc6ca065d0"
model="azure_gpt-4o"
content, image_path = parse_pdf("D:\\Capagemini\\PGmini\\capgemini-poc\\takeda_Functional_Validation\\5500220_A1B331AA_CoC_V1_CofA.pdf", output_dir='./',base_url=base_url, api_key=api_key,model=model)

print(content)